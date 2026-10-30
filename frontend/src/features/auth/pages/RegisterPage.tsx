import { useMemo, useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { getErrorMessage } from '../../../shared/api/httpClient'
import { useAuth } from '../context/AuthContext'
import {
  sanitizeFullName,
  EARLIEST_BIRTH_DATE,
  TODAY_DATE,
  validateRegistration,
  type RegistrationForm,
} from '../registrationValidation'
import { verificationStorage } from '../verificationStorage'
import { PasswordInput } from '../components/PasswordInput'


const initialForm: RegistrationForm = {
  full_name: '',
  birth_date: '',
  email: '',
  password: '',
  confirm_password: '',
  accepted_terms: false,
}


export function RegisterPage() {
  const [form, setForm] = useState(initialForm)
  const [showErrors, setShowErrors] = useState(false)
  const [requestError, setRequestError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const { user, register } = useAuth()
  const navigate = useNavigate()
  const errors = useMemo(() => validateRegistration(form), [form])

  if (user) return <Navigate to="/inicio" replace />

  const update = (field: keyof RegistrationForm, value: string | boolean) => {
    setForm((current) => ({ ...current, [field]: value }))
    setRequestError('')
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setShowErrors(true)
    setRequestError('')
    if (Object.keys(errors).length) return

    setSubmitting(true)
    try {
      const email = await register({
        ...form,
        full_name: form.full_name.trim().replace(/\s+/g, ' '),
        email: form.email.trim().toLowerCase(),
      })
      verificationStorage.save(email)
      navigate('/verificar-correo', { replace: true })
    } catch (error) {
      setRequestError(getErrorMessage(error))
    } finally {
      setSubmitting(false)
    }
  }

  const fieldError = (field: keyof RegistrationForm) => (
    showErrors && errors[field]
      ? <div className="invalid-feedback d-block" id={`${field}-error`}>{errors[field]}</div>
      : null
  )

  const describedBy = (field: keyof RegistrationForm, helpId?: string) => {
    const references = [showErrors && errors[field] ? `${field}-error` : '', helpId ?? ''].filter(Boolean)
    return references.length ? references.join(' ') : undefined
  }

  return (
    <main className="auth-page register-page">
      <section className="auth-story" aria-labelledby="register-story-title">
        <div>
          <div className="brand auth-brand">
            <span className="brand-mark" aria-hidden="true">CS</span>
            <span>CiberSegura</span>
          </div>
          <p className="eyebrow light">Comunidad universitaria</p>
          <h1 id="register-story-title">Construye tu ruta de protección.</h1>
          <p className="auth-lead">El registro está disponible para correos institucionales de universidades reconocidas de distintos países.</p>
        </div>
        <ol className="mini-steps">
          <li><span>1</span> Completa y valida todos tus datos.</li>
          <li><span>2</span> Recibe un código en tu correo universitario.</li>
          <li><span>3</span> Confirma el código y comienza la evaluación.</li>
        </ol>
      </section>

      <section className="auth-form-panel" aria-labelledby="register-title">
        <div className="auth-form-wrap auth-form-wide">
          <span className="eyebrow">Registro institucional</span>
          <h2 id="register-title">Crea tu cuenta</h2>
          <p>La cuenta no se activará hasta comprobar el código enviado a tu correo.</p>

          {requestError && <div className="alert alert-danger" role="alert">{requestError}</div>}

          <form onSubmit={handleSubmit} noValidate>
            <div className="row g-3">
              <div className="col-12">
                <label className="form-label" htmlFor="full-name">Nombre Completo</label>
                <input
                  className={`form-control ${showErrors && errors.full_name ? 'is-invalid' : ''}`}
                  id="full-name"
                  type="text"
                  autoComplete="name"
                  inputMode="text"
                  maxLength={120}
                  pattern="[A-Za-zÁÉÍÓÚÜÑáéíóúüñÀÈÌÒÙàèìòù' -]+"
                  title="Escribe únicamente letras, espacios, apóstrofes o guiones."
                  value={form.full_name}
                  onChange={(event) => update('full_name', sanitizeFullName(event.target.value))}
                  aria-invalid={showErrors && Boolean(errors.full_name)}
                  aria-describedby={describedBy('full_name')}
                  required
                />
                {fieldError('full_name')}
              </div>
              <div className="col-12">
                <label className="form-label" htmlFor="birth-date">Fecha de Nacimiento</label>
                <input className={`form-control ${showErrors && errors.birth_date ? 'is-invalid' : ''}`} id="birth-date" type="date" min={EARLIEST_BIRTH_DATE} max={TODAY_DATE} value={form.birth_date} onChange={(event) => update('birth_date', event.target.value)} aria-invalid={showErrors && Boolean(errors.birth_date)} aria-describedby={describedBy('birth_date')} required />
                {fieldError('birth_date')}
              </div>
              <div className="col-12">
                <label className="form-label" htmlFor="email">Correo Institucional</label>
                <input className={`form-control ${showErrors && errors.email ? 'is-invalid' : ''}`} id="email" type="email" autoComplete="email" placeholder="usuario@universidad.edu" value={form.email} onChange={(event) => update('email', event.target.value)} aria-invalid={showErrors && Boolean(errors.email)} aria-describedby={describedBy('email')} required />
                {fieldError('email')}
              </div>
              <div className="col-12 col-md-6">
                <label className="form-label" htmlFor="register-password">Contraseña</label>
                <PasswordInput className={`form-control ${showErrors && errors.password ? 'is-invalid' : ''}`} id="register-password" autoComplete="new-password" minLength={10} maxLength={128} value={form.password} onChange={(event) => update('password', event.target.value)} required aria-invalid={showErrors && Boolean(errors.password)} aria-describedby={describedBy('password', 'password-help')} />
                {fieldError('password')}
              </div>
              <div className="col-12 col-md-6">
                <label className="form-label" htmlFor="confirm-password">Confirmar Contraseña</label>
                <PasswordInput className={`form-control ${showErrors && errors.confirm_password ? 'is-invalid' : ''}`} id="confirm-password" autoComplete="new-password" value={form.confirm_password} onChange={(event) => update('confirm_password', event.target.value)} required aria-invalid={showErrors && Boolean(errors.confirm_password)} aria-describedby={describedBy('confirm_password')} />
                {fieldError('confirm_password')}
              </div>
              <div className="col-12">
                <div className="form-text" id="password-help">Mínimo 10 caracteres, con mayúscula, minúscula, número y símbolo.</div>
              </div>
              <div className="col-12">
                <div className="form-check consent-check">
                  <input className={`form-check-input ${showErrors && errors.accepted_terms ? 'is-invalid' : ''}`} id="terms" type="checkbox" checked={form.accepted_terms} onChange={(event) => update('accepted_terms', event.target.checked)} aria-invalid={showErrors && Boolean(errors.accepted_terms)} aria-describedby={describedBy('accepted_terms')} required />
                  <label className="form-check-label" htmlFor="terms">Comprendo que las evaluaciones son orientativas y no reemplazan ayuda profesional o una denuncia.</label>
                  {fieldError('accepted_terms')}
                </div>
              </div>
            </div>
            <button className="btn btn-primary btn-lg w-100 mt-4" disabled={submitting} type="submit">
              {submitting ? 'Enviando código…' : 'Validar correo y continuar'}
            </button>
          </form>
          <p className="auth-switch">¿Ya tienes cuenta? <Link to="/acceso">Iniciar sesión</Link></p>
        </div>
      </section>
    </main>
  )
}
