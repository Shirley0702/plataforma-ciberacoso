import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, getErrorMessage, tokenStorage } from '../../../shared/api/httpClient'
import type { DiagnosticQuestion } from '../types'
import { diagnosticDraftStorage } from '../diagnosticDraftStorage'

export function DiagnosticPage() {
  const navigate = useNavigate()
  const [initialDraft] = useState(() => diagnosticDraftStorage.load())
  const [questions, setQuestions] = useState<DiagnosticQuestion[]>([])
  const [answers, setAnswers] = useState<Record<number, number>>(initialDraft.answers)
  const [currentIndex, setCurrentIndex] = useState(initialDraft.currentIndex)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    api.get<DiagnosticQuestion[]>('/diagnostics/questions/')
      .then(({ data }) => {
        setQuestions(data)
        setCurrentIndex((index) => Math.min(index, Math.max(data.length - 1, 0)))
      })
      .catch((requestError) => setError(getErrorMessage(requestError)))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    diagnosticDraftStorage.save({ answers, currentIndex })
  }, [answers, currentIndex])

  useEffect(() => {
    const handleQuickExit = (event: KeyboardEvent) => {
      if (event.key === 'Escape') quickExit()
    }
    window.addEventListener('keydown', handleQuickExit)
    return () => window.removeEventListener('keydown', handleQuickExit)
  }, [])

  const question = questions[currentIndex]
  const answered = questions.filter((item) => Boolean(answers[item.id])).length
  const percentage = questions.length
    ? Math.round((currentIndex + 1) / questions.length * 100)
    : 0
  const isLast = currentIndex === questions.length - 1

  const submit = async () => {
    setError('')
    if (answered !== questions.length) {
      setError('Responde todos los escenarios antes de generar tu ruta.')
      return
    }
    setSubmitting(true)
    try {
      await api.post('/diagnostics/submit/', {
        answers: questions.map((item) => ({
          question_id: item.id,
          option_id: answers[item.id],
        })),
      })
      diagnosticDraftStorage.clear()
      navigate('/panel', { replace: true, state: { diagnosticCompleted: true } })
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  const quickExit = () => {
    diagnosticDraftStorage.clear()
    tokenStorage.clear()
    window.location.replace('https://www.google.com/')
  }

  const continueFlow = () => {
    if (!question || !answers[question.id]) {
      setError('Selecciona la opción que más se aproxima a tu experiencia.')
      return
    }
    setError('')
    if (isLast) void submit()
    else setCurrentIndex((index) => index + 1)
  }

  return (
    <div className="page-wrap scenario-page">
      <header className="page-header scenario-header">
        <div>
          <span className="eyebrow">Situaciones Cotidianas</span>
          <h1>¿Qué suele pasar en estas situaciones?</h1>
          <p>Elige la opción que más se parece a lo que has visto o vivido en la universidad. No hay respuestas correctas o incorrectas.</p>
        </div>
        <div className="progress-summary" aria-label={`Escenario ${questions.length ? currentIndex + 1 : 0} de ${questions.length}`}>
          <strong>{questions.length ? currentIndex + 1 : 0} de {questions.length}</strong>
          <span>escenarios</span>
        </div>
      </header>

      <div className="privacy-banner" role="note">
        <span className="privacy-icon" aria-hidden="true">i</span>
        <p><strong>Tu espacio es privado.</strong> Tus respuestas organizan un recorrido educativo; el resultado es orientativo y no constituye un diagnóstico profesional.</p>
      </div>

      {error && <div className="alert alert-danger" role="alert">{error}</div>}
      {loading && <div className="skeleton-block" aria-label="Cargando escenarios" />}

      {!loading && question && (
        <section key={question.id} className="scenario-card scenario-enter" aria-labelledby={`scenario-${question.id}`}>
          <div className="scenario-card-top">
            <span>Escenario {currentIndex + 1}</span>
            <div className="scenario-card-actions">
              <span>Respuesta confidencial</span>
              <button className="quick-exit-button" type="button" onClick={quickExit}>× Salir Rápido (Esc)</button>
            </div>
          </div>
          <h2 id={`scenario-${question.id}`}>{question.text}</h2>
          <div className="scenario-options" role="radiogroup" aria-label="Opciones del escenario">
            {question.options.map((option, index) => {
              const selected = answers[question.id] === option.id
              return (
                <label className={`scenario-option ${selected ? 'selected' : ''}`} key={option.id}>
                  <input
                    type="radio"
                    name={`question-${question.id}`}
                    checked={selected}
                    onChange={() => {
                      setAnswers((current) => ({ ...current, [question.id]: option.id }))
                      setError('')
                    }}
                  />
                  <span className="option-letter" aria-hidden="true">{String.fromCharCode(65 + index)}</span>
                  <span>{option.label}</span>
                </label>
              )
            })}
          </div>
        </section>
      )}

      {!loading && question && (
        <div className="scenario-controls">
          <button
            className="btn btn-outline-primary"
            type="button"
            disabled={currentIndex === 0 || submitting}
            onClick={() => setCurrentIndex((index) => index - 1)}
          >
            Anterior
          </button>
          <div className="scenario-progress-wrap">
            <span className="scenario-progress-text">Escenario {currentIndex + 1} de {questions.length}</span>
            <div className="scenario-progress" role="progressbar" aria-label="Progreso de situaciones" aria-valuenow={currentIndex + 1} aria-valuemin={1} aria-valuemax={questions.length}>
              <span style={{ width: `${percentage}%` }} />
            </div>
          </div>
          <button
            className="btn btn-primary btn-lg"
            type="button"
            disabled={submitting}
            onClick={continueFlow}
          >
            {submitting ? 'Generando tu ruta…' : isLast ? 'Generar mi curso personalizado' : 'Siguiente escenario'}
          </button>
        </div>
      )}
    </div>
  )
}
