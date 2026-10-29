import { useMemo, useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { adminPanelUrl } from '../../../shared/config/runtime'
import { getErrorMessage } from '../../../shared/api/httpClient'
import { useAuth } from '../context/AuthContext'
import { validateLogin } from '../loginValidation'
import { PasswordInput } from '../components/PasswordInput'

export function LoginPage() {
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [showErrors, setShowErrors] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()
  const fieldErrors = useMemo(
    () => validateLogin({ identifier, password }),
    [identifier, password],
  )

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setShowErrors(true)
    setError('')
    if (Object.keys(fieldErrors).length) return
    setSubmitting(true)
    try {
      await login(identifier.trim().toLowerCase(), password)
      navigate('/inicio', { replace: true })
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-story" aria-labelledby="story-title">
        <div>
          <div className="brand auth-brand">
            <span className="brand-mark" aria-hidden="true">CS</span>
            <span>CiberSegura</span>
          </div>
          <p className="eyebrow light">Prevención y orientación digital</p>
          <h1 id="story-title">Lo que pasa en línea también importa.</h1>
          <p className="auth-lead">
            Aprende a reconocer señales, fortalece tu seguridad y encuentra una ruta clara para pedir ayuda.
          </p>
        </div>
        <div className="trust-note">
          <span className="trust-number">01</span>
          <p>
            Tu resultado es privado y orientativo. Si existe peligro inmediato en Ecuador, llama al <strong>9-1-1</strong>.
          </p>
        </div>
      </section>

      <section className="auth-form-panel" aria-labelledby="login-title">
        <div className="auth-form-wrap">
          <span className="eyebrow">Qué bueno verte</span>
          <h2 id="login-title">Inicia sesión</h2>
          <p>Continúa tu recorrido de aprendizaje y prevención.</p>

          {error && <div className="alert alert-danger" role="alert">{error}</div>}

          <form onSubmit={handleSubmit} noValidate>
            <div className="mb-3">
              <label className="form-label" htmlFor="identifier">Correo institucional</label>
              <input
                className={`form-control form-control-lg ${showErrors && fieldErrors.identifier ? 'is-invalid' : ''}`}
                id="identifier"
                autoComplete="username"
                placeholder="usuario@universidad.edu"
                value={identifier}
                onChange={(event) => setIdentifier(event.target.value)}
                required
              />
              {showErrors && fieldErrors.identifier && <div className="invalid-feedback">{fieldErrors.identifier}</div>}
              <div className="form-text">La cuenta de prueba también puede ingresar como demo.</div>
            </div>
            <div className="mb-4">
              <label className="form-label" htmlFor="password">Contraseña</label>
              <PasswordInput
                className={`form-control form-control-lg ${showErrors && fieldErrors.password ? 'is-invalid' : ''}`}
                id="password"
                autoComplete="current-password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
              {showErrors && fieldErrors.password && <div className="invalid-feedback d-block">{fieldErrors.password}</div>}
            </div>
            <button className="btn btn-primary btn-lg w-100" disabled={submitting} type="submit">
              {submitting ? 'Ingresando…' : 'Entrar a mi espacio'}
            </button>
          </form>

          <p className="auth-switch">
            ¿Aún no tienes cuenta? <Link to="/registro">Crear una cuenta</Link>
          </p>

          <div className="admin-access">
            <span>Acceso separado por rol</span>
            <p>La cuenta demo utiliza este formulario. La cuenta admin gestiona el sistema desde su panel exclusivo.</p>
            <a className="btn btn-outline-primary w-100" href={adminPanelUrl}>Ir al panel de administración</a>
          </div>
        </div>
      </section>
    </main>
  )
}
