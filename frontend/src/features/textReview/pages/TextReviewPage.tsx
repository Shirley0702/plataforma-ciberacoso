import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, getErrorMessage, tokenStorage } from '../../../shared/api/httpClient'
import type { TextReviewResult } from '../types'

const MAX_LENGTH = 3000

export function TextReviewPage() {
  const [text, setText] = useState('')
  const [result, setResult] = useState<TextReviewResult | null>(null)
  const [error, setError] = useState('')
  const [loadingLatest, setLoadingLatest] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    api.get<TextReviewResult | null>('/text-reviews/latest/')
      .then(({ data }) => setResult(data))
      .catch((requestError) => setError(getErrorMessage(requestError)))
      .finally(() => setLoadingLatest(false))
  }, [])

  useEffect(() => {
    const handleQuickExit = (event: KeyboardEvent) => {
      if (event.key === 'Escape') quickExit()
    }
    window.addEventListener('keydown', handleQuickExit)
    return () => window.removeEventListener('keydown', handleQuickExit)
  }, [])

  const quickExit = () => {
    setText('')
    tokenStorage.clear()
    window.location.replace('https://www.google.com/')
  }

  const submit = async (event: React.FormEvent) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      const response = await api.post<TextReviewResult>('/text-reviews/review/', { text })
      setResult(response.data)
      setText('')
      document.getElementById('resultado-revision')?.focus()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="page-wrap text-review-page">
      <header className="page-header text-review-header">
        <div>
          <span className="eyebrow">Orientación Personalizada</span>
          <h1>Revisa una Situación Escrita</h1>
          <p>Describe lo ocurrido con tus propias palabras. Recibirás una orientación inicial y opciones para continuar.</p>
        </div>
        <button className="quick-exit-button" type="button" onClick={quickExit}>× Salir Rápido (Esc)</button>
      </header>

      <div className="privacy-banner" role="note">
        <span className="privacy-icon" aria-hidden="true">i</span>
        <p><strong>Protege tu privacidad.</strong> No escribas nombres, correos, teléfonos ni otros datos identificables. El texto no se guarda.</p>
      </div>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
          {error.includes('evaluación') && <div><Link to="/evaluacion">Ir a la Evaluación</Link></div>}
        </div>
      )}

      <section className="text-review-card" aria-labelledby="review-form-title">
        <div className="section-heading compact">
          <span className="eyebrow">Descripción</span>
          <h2 id="review-form-title">¿Qué ocurrió?</h2>
          <p>Incluye el contexto y si la situación ocurrió más de una vez, sin identificar a las personas.</p>
        </div>
        <form onSubmit={(event) => void submit(event)}>
          <label className="form-label" htmlFor="situation-text">Situación a Revisar</label>
          <textarea
            id="situation-text"
            className="form-control text-review-input"
            value={text}
            minLength={20}
            maxLength={MAX_LENGTH}
            required
            rows={8}
            placeholder="Ejemplo: En el grupo de clase ocurrió una situación que me hizo sentir incómodo…"
            onChange={(event) => setText(event.target.value)}
          />
          <div className="text-review-form-footer">
            <span aria-live="polite">{text.length} de {MAX_LENGTH} caracteres</span>
            <button className="btn btn-primary btn-lg" type="submit" disabled={submitting || text.trim().length < 20}>
              {submitting ? 'Revisando de Forma Segura…' : 'Obtener Orientación'}
            </button>
          </div>
        </form>
      </section>

      {!loadingLatest && result && (
        <section
          id="resultado-revision"
          className={`text-review-result ${result.possible_signals ? 'attention' : 'calm'}`}
          aria-labelledby="review-result-title"
          tabIndex={-1}
        >
          <span className="status-pill">Orientación Inicial</span>
          <h2 id="review-result-title">{result.title}</h2>
          <p>{result.guidance}</p>
          <h3>Pasos que Puedes Considerar</h3>
          <ul>
            {result.recommendations.map((recommendation) => <li key={recommendation}>{recommendation}</li>)}
          </ul>
          <div className="text-review-actions">
            {result.recommended_unit && <Link className="btn btn-primary" to="/curso">Continuar con Mi Curso</Link>}
            <Link className="btn btn-outline-primary" to="/recursos">Consultar Recursos</Link>
          </div>
          <p className="privacy-confirmation"><strong>Privacidad:</strong> {result.privacy_notice}</p>
        </section>
      )}

      <aside className="home-safety-note">
        <span aria-hidden="true">i</span>
        <p><strong>Importante:</strong> esta orientación no reemplaza el criterio profesional. Si existe peligro inmediato en Ecuador, llama al 9-1-1.</p>
      </aside>
    </div>
  )
}
