import { useEffect, useState, type FormEvent } from 'react'
import { Link } from 'react-router-dom'

import { api, getErrorMessage } from '../../../shared/api/httpClient'
import type { ProductFeedback, ProductFeedbackForm } from '../types'


type RatingKey = Exclude<keyof ProductFeedbackForm, 'open_comment' | 'informed_consent'>

const ratingQuestions: Array<{ key: RatingKey; label: string }> = [
  { key: 'ease_of_use', label: '¿Qué tan fácil fue utilizar la plataforma?' },
  { key: 'content_clarity', label: '¿Qué tan claros fueron los textos y las instrucciones?' },
  { key: 'educational_usefulness', label: '¿Qué tan útil fue el contenido para tu aprendizaje?' },
  { key: 'satisfaction', label: '¿Qué tan satisfecho estás con tu experiencia general?' },
  { key: 'accessibility', label: '¿Qué tan fácil fue percibir y operar los controles?' },
]

const emptyForm: ProductFeedbackForm = {
  ease_of_use: 0,
  content_clarity: 0,
  educational_usefulness: 0,
  satisfaction: 0,
  accessibility: 0,
  open_comment: '',
  informed_consent: false,
}

export function ProductFeedbackPage() {
  const [form, setForm] = useState<ProductFeedbackForm>(emptyForm)
  const [version, setVersion] = useState('')
  const [loading, setLoading] = useState(true)
  const [canEvaluate, setCanEvaluate] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    api.get<ProductFeedback | null>('/product-validation/feedback/')
      .then(({ data }) => {
        setCanEvaluate(true)
        if (!data) return
        setVersion(data.app_version)
        setForm({
          ease_of_use: data.ease_of_use,
          content_clarity: data.content_clarity,
          educational_usefulness: data.educational_usefulness,
          satisfaction: data.satisfaction,
          accessibility: data.accessibility,
          open_comment: data.open_comment,
          informed_consent: data.informed_consent,
        })
      })
      .catch((requestError) => setError(getErrorMessage(requestError)))
      .finally(() => setLoading(false))
  }, [])

  const update = <Key extends keyof ProductFeedbackForm>(
    field: Key,
    value: ProductFeedbackForm[Key],
  ) => {
    setForm((current) => ({ ...current, [field]: value }))
    setError('')
    setMessage('')
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    if (ratingQuestions.some(({ key }) => form[key] < 1) || !form.informed_consent) {
      setError('Responde las cinco preguntas y confirma el consentimiento antes de guardar.')
      return
    }
    setSubmitting(true)
    setError('')
    setMessage('')
    try {
      const { data } = await api.post<ProductFeedback>('/product-validation/feedback/', form)
      setVersion(data.app_version)
      setMessage('Tu evaluación quedó guardada. Puedes actualizarla mientras se revise esta versión.')
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="page-wrap feedback-page">
      <header className="page-header">
        <div>
          <span className="eyebrow">{canEvaluate ? 'Curso completado' : 'Evaluación de la plataforma'}</span>
          <h1>Evalúa la plataforma</h1>
          <p>Esta encuesta breve permite evaluar la facilidad de uso, claridad, utilidad educativa, satisfacción y accesibilidad de la plataforma.</p>
        </div>
      </header>

      {canEvaluate && (
        <aside className="privacy-banner" role="note">
          <span className="privacy-icon" aria-hidden="true">i</span>
          <p><strong>No incluyas información sensible.</strong> Describe únicamente tu experiencia con la plataforma. Tu respuesta se analizará de forma agrupada.</p>
        </aside>
      )}

      {loading && <div className="skeleton-block" aria-label="Cargando encuesta" />}
      {error && <div className="alert alert-danger" role="alert">{error}</div>}
      {error && !canEvaluate && <p><Link to="/curso">Volver al curso</Link></p>}
      {message && <div className="alert alert-success" role="status">{message}</div>}

      {!loading && canEvaluate && (
        <form className="feedback-form" onSubmit={handleSubmit} noValidate>
          {version && <p className="feedback-version">Respuesta registrada para la versión {version}</p>}
          <p className="feedback-instructions" id="rating-help">Selecciona una opción entre 1 (muy bajo) y 5 (muy alto).</p>

          {ratingQuestions.map(({ key, label }) => (
            <fieldset className="feedback-question" key={key} aria-describedby="rating-help">
              <legend>{label}</legend>
              <div className="rating-scale">
                {[1, 2, 3, 4, 5].map((score) => (
                  <label className={form[key] === score ? 'selected' : ''} key={score}>
                    <input
                      type="radio"
                      name={key}
                      value={score}
                      checked={form[key] === score}
                      onChange={() => update(key, score)}
                      aria-label={`${label}: ${score} de 5`}
                      required
                    />
                    <span>{score}</span>
                  </label>
                ))}
              </div>
              <div className="rating-anchors" aria-hidden="true"><span>Muy bajo</span><span>Muy alto</span></div>
            </fieldset>
          ))}

          <div className="feedback-comment">
            <label className="form-label" htmlFor="feedback-comment">Comentario opcional</label>
            <textarea
              className="form-control"
              id="feedback-comment"
              rows={4}
              maxLength={1000}
              value={form.open_comment}
              onChange={(event) => update('open_comment', event.target.value)}
              aria-describedby="comment-help"
            />
            <div className="form-text" id="comment-help">No escribas nombres, correos, mensajes privados ni detalles que permitan identificar a una persona.</div>
          </div>

          <div className="form-check consent-check">
            <input
              className="form-check-input"
              id="feedback-consent"
              type="checkbox"
              checked={form.informed_consent}
              onChange={(event) => update('informed_consent', event.target.checked)}
              required
            />
            <label className="form-check-label" htmlFor="feedback-consent">Acepto que estas respuestas se utilicen para evaluar y mejorar CiberSegura.</label>
          </div>

          <button className="btn btn-primary btn-lg" type="submit" disabled={submitting}>
            {submitting ? 'Guardando…' : 'Guardar Evaluación'}
          </button>
        </form>
      )}
    </div>
  )
}
