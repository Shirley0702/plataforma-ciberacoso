import type { Dispatch, SetStateAction } from 'react'
import { Link } from 'react-router-dom'
import type { CourseUnit, QuizResult } from '../types'

interface ModuleAssessmentProps {
  unit: CourseUnit
  answers: Record<number, number>
  setAnswers: Dispatch<SetStateAction<Record<number, number>>>
  result: QuizResult | null
  submitting: boolean
  onSubmit: (unit: CourseUnit) => Promise<void>
  onDownload: (unit: CourseUnit) => Promise<void>
}

export function ModuleAssessment({
  unit,
  answers,
  setAnswers,
  result,
  submitting,
  onSubmit,
  onDownload,
}: ModuleAssessmentProps) {
  const latestResult = result ?? unit.latest_quiz
  const quizTitleId = `quiz-title-${unit.id}`

  return (
    <>
      <section className={`module-quiz ${unit.quiz_unlocked ? '' : 'locked'}`} aria-labelledby={quizTitleId}>
        <span className="eyebrow">Evaluación final del módulo</span>
        <h2 id={quizTitleId}>Cuestionario obligatorio · aprobación mínima 80%</h2>
        {!unit.quiz_unlocked ? (
          <p>Completa todos los microcontenidos y la actividad interactiva para desbloquearlo.</p>
        ) : (
          <>
            {unit.quiz_questions.map((question, index) => (
              <fieldset className="quiz-question" key={question.id}>
                <legend>{index + 1}. {question.text}</legend>
                {question.options.map((option) => (
                  <label className={answers[question.id] === option.id ? 'selected' : ''} key={option.id}>
                    <input
                      type="radio"
                      name={`quiz-${question.id}`}
                      checked={answers[question.id] === option.id}
                      onChange={() => setAnswers((current) => ({ ...current, [question.id]: option.id }))}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </fieldset>
            ))}
            <button
              className="btn btn-primary btn-lg"
              disabled={submitting}
              onClick={() => void onSubmit(unit)}
            >
              {submitting ? 'Calificando…' : 'Enviar cuestionario'}
            </button>
          </>
        )}
      </section>

      {latestResult && (
        <section id={`resultado-cuestionario-${unit.id}`} className={`quiz-result ${latestResult.passed ? 'passed' : 'pending'}`}>
          <span className="eyebrow">Último resultado</span>
          <h2>{latestResult.score_percentage}%</h2>
          <p>{latestResult.passed ? 'Aprobaste el módulo. Tu certificado ya está disponible.' : 'Necesitas al menos 80 %. Revisa las lecciones y vuelve a intentarlo.'}</p>
        </section>
      )}

      {unit.certificate && (
        <section className="certificate-card">
          <div>
            <span className="eyebrow light">Certificación emitida</span>
            <h2>¡Completaste esta unidad de aprendizaje!</h2>
            <p>Código verificable: <strong>{unit.certificate.verification_code}</strong></p>
          </div>
          <div className="certificate-actions">
            <button className="btn btn-light" onClick={() => void onDownload(unit)}>
              Descargar certificado PDF
            </button>
            <Link className="btn btn-outline-light" to="/evaluar-plataforma">
              Evaluar la plataforma
            </Link>
          </div>
        </section>
      )}
    </>
  )
}
