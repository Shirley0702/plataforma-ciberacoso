import { useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { getErrorMessage } from '../../../shared/api/httpClient'
import { useAuth } from '../context/AuthContext'
import { verificationStorage } from '../verificationStorage'


export function VerifyEmailPage() {
  const email = verificationStorage.get()
  const [code, setCode] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const { user, verifyEmail, resendVerification } = useAuth()
  const navigate = useNavigate()

  if (user) return <Navigate to="/inicio" replace />
  if (!email) return <Navigate to="/registro" replace />

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setMessage('')
    if (!/^\d{6}$/.test(code)) {
      setError('Ingresa el código de 6 dígitos enviado a tu correo.')
      return
    }
    setSubmitting(true)
    setError('')
    try {
      await verifyEmail(email, code)
      verificationStorage.clear()
      navigate('/inicio', { replace: true })
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  const resend = async () => {
    setSubmitting(true)
    setError('')
    setMessage('')
    try {
      await resendVerification(email)
      setMessage('Enviamos un código nuevo. Revisa también tu carpeta de spam.')
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="verification-page">
      <section className="verification-card" aria-labelledby="verification-title">
        <span className="brand-mark" aria-hidden="true">CS</span>
        <span className="eyebrow">Verificación institucional</span>
        <h1 id="verification-title">Revisa tu correo</h1>
        <p>Enviamos un código de 6 dígitos a <strong>{email}</strong>. Caduca en 10 minutos.</p>
        {error && <div className="alert alert-danger" role="alert">{error}</div>}
        {message && <div className="alert alert-success" role="status">{message}</div>}
        <form onSubmit={handleSubmit}>
          <label className="form-label" htmlFor="verification-code">Código de verificación</label>
          <input
            className="form-control verification-code"
            id="verification-code"
            inputMode="numeric"
            autoComplete="one-time-code"
            pattern="[0-9]{6}"
            maxLength={6}
            value={code}
            onChange={(event) => setCode(event.target.value.replace(/\D/g, '').slice(0, 6))}
            autoFocus
            required
          />
          <button className="btn btn-primary btn-lg w-100 mt-3" disabled={submitting} type="submit">
            {submitting ? 'Verificando…' : 'Verificar y activar cuenta'}
          </button>
        </form>
        <button className="verification-resend" disabled={submitting} type="button" onClick={() => void resend()}>
          Enviar un código nuevo
        </button>
        <Link to="/registro" onClick={() => verificationStorage.clear()}>Cambiar correo</Link>
      </section>
    </main>
  )
}
