import type { CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import { LearningItemCard } from '../components/LearningItemCard'
import { ModuleAssessment } from '../components/ModuleAssessment'
import { useCourse } from '../hooks/useCourse'

export function CoursePage() {
  const course = useCourse()
  const currentUnit = course.units[0]

  return (
    <div className="page-wrap">
      <header className="page-header course-header">
        <div>
          <span className="eyebrow">Ruta adaptativa estricta</span>
          <h1>{currentUnit?.title ?? 'Ruta de aprendizaje personalizada'}</h1>
          <p>{currentUnit?.description ?? 'Completa primero la evaluación para generar tu ruta.'}</p>
        </div>
        <div
          className="course-progress-ring"
          style={{ '--course-progress': `${course.progress.percentage * 3.6}deg` } as CSSProperties}
        >
          <span>{course.progress.percentage}%</span>
          <small>microcontenidos</small>
        </div>
      </header>

      {course.error && <div className="alert alert-danger" role="alert">{course.error}</div>}
      {!course.units.length && !course.error && <div className="skeleton-block" aria-label="Cargando curso" />}
      {course.error && !course.units.length && <p><Link to="/evaluacion">Volver a la evaluación</Link></p>}

      {currentUnit && (
        <>
          <section className="course-overview" aria-label="Resumen del curso">
            <div><strong>1</strong><span>módulo asignado</span></div>
            <div><strong>{course.progress.total}</strong><span>microcontenidos</span></div>
            <div><strong>{course.progress.completed}</strong><span>completados</span></div>
          </section>

          <section className="course-unit" aria-labelledby={`unit-${currentUnit.id}`}>
            <div className="unit-heading">
              <span className="unit-number">01</span>
              <div>
                <span className="eyebrow">Especialidad · {currentUnit.duration_minutes} min</span>
                <h2 id={`unit-${currentUnit.id}`}>{currentUnit.title}</h2>
                <p>{currentUnit.description}</p>
              </div>
              <span className="unit-count">
                {currentUnit.lessons.filter((lesson) => lesson.completed).length}/{currentUnit.lessons.length}
              </span>
            </div>

            <div className="lesson-list">
              {currentUnit.lessons.map((lesson, index) => (
                <LearningItemCard
                  key={lesson.id}
                  lesson={lesson}
                  position={index + 1}
                  isOpen={course.openLessonId === lesson.id}
                  saving={course.savingLessonId === lesson.id}
                  selectedChoice={course.activityChoices[lesson.id]}
                  feedback={course.activityFeedback[lesson.id]}
                  onToggle={() => course.setOpenLessonId(
                    course.openLessonId === lesson.id ? null : lesson.id,
                  )}
                  onChoice={(choice) => course.setActivityChoices((current) => ({
                    ...current,
                    [lesson.id]: choice,
                  }))}
                  onCompletion={course.updateCompletion}
                />
              ))}
            </div>

            <ModuleAssessment
              unit={currentUnit}
              answers={course.quizAnswers}
              setAnswers={course.setQuizAnswers}
              result={course.quizResult}
              submitting={course.submittingQuiz}
              onSubmit={course.submitQuiz}
              onDownload={course.downloadCertificate}
            />
          </section>
        </>
      )}
    </div>
  )
}
