import type { CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import { CourseSafetyBanner } from '../components/CourseSafetyBanner'
import { LearningItemCard } from '../components/LearningItemCard'
import { ModuleAssessment } from '../components/ModuleAssessment'
import { useCourse } from '../hooks/useCourse'

export function CoursePage() {
  const course = useCourse()
  const primaryUnit = course.units[0]

  return (
    <div className="page-wrap">
      <header className="page-header course-header">
        <div>
          <span className="eyebrow">Recorrido de aprendizaje personalizado</span>
          <h1>{primaryUnit?.title ?? 'Ruta de aprendizaje personalizada'}</h1>
          <p>
            {primaryUnit
              ? 'Avanza por las unidades priorizadas a partir de tus respuestas.'
              : 'Completa primero la evaluación para generar tu ruta.'}
          </p>
        </div>
        <div
          className="course-progress-ring"
          style={{ '--course-progress': `${course.progress.percentage * 3.6}deg` } as CSSProperties}
        >
          <span>{course.progress.percentage}%</span>
          <small>experiencias</small>
        </div>
      </header>

      {course.error && <div className="alert alert-danger" role="alert">{course.error}</div>}
      {!course.units.length && !course.error && <div className="skeleton-block" aria-label="Cargando curso" />}
      {course.error && !course.units.length && <p><Link to="/evaluacion">Volver a la evaluación</Link></p>}

      {primaryUnit && (
        <>
          <CourseSafetyBanner />
          <section className="course-overview" aria-label="Resumen del curso">
            <div><strong>{course.units.length}</strong><span>{course.units.length === 1 ? 'unidad asignada' : 'unidades priorizadas'}</span></div>
            <div><strong>{course.progress.total}</strong><span>experiencias</span></div>
            <div><strong>{course.progress.completed}</strong><span>completados</span></div>
          </section>

          {course.units.map((unit, unitIndex) => (
            <section className="course-unit" aria-labelledby={`unit-${unit.id}`} key={unit.id}>
              <div className="unit-heading">
                <span className="unit-number">{String(unitIndex + 1).padStart(2, '0')}</span>
                <div>
                  <span className="eyebrow">
                    Prioridad {unit.priority} · {unit.duration_minutes} min
                  </span>
                  <h2 id={`unit-${unit.id}`}>{unit.title}</h2>
                  <p>{unit.description}</p>
                </div>
                <span className="unit-count">
                  {unit.lessons.filter((lesson) => lesson.completed).length}/{unit.lessons.length}
                </span>
              </div>

              <div className="lesson-list">
                {unit.lessons.map((lesson, index) => (
                  <LearningItemCard
                    key={lesson.id}
                    lesson={lesson}
                    position={index + 1}
                    isOpen={course.openLessonId === lesson.id}
                    saving={course.savingLessonId === lesson.id}
                    response={course.interactionResponses[lesson.id] ?? {}}
                    feedback={course.interactionFeedback[lesson.id]}
                    onToggle={() => course.setOpenLessonId(
                      course.openLessonId === lesson.id ? null : lesson.id,
                    )}
                    onResponseChange={(response) => course.setInteractionResponse(
                      lesson.id,
                      response,
                    )}
                    onCompletion={course.updateCompletion}
                  />
                ))}
              </div>

              <ModuleAssessment
                unit={unit}
                answers={course.quizAnswers}
                setAnswers={course.setQuizAnswers}
                result={course.quizResults[unit.id] ?? null}
                submitting={course.submittingUnitId === unit.id}
                onSubmit={course.submitQuiz}
                onDownload={course.downloadCertificate}
              />
            </section>
          ))}
        </>
      )}
    </div>
  )
}
