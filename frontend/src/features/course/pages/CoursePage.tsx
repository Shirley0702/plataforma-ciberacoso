import { useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { getCourseThemeClass } from '../config/courseThemes'
import { CourseProgressPanel } from '../components/CourseProgressPanel'
import { CourseSafetyBanner } from '../components/CourseSafetyBanner'
import { LearningExperience } from '../components/LearningExperience'
import { ModuleAssessment } from '../components/ModuleAssessment'
import { useCourse } from '../hooks/useCourse'
import type { InteractionResponse, LearningItem } from '../types'

function orderExperiences(lessons: LearningItem[]) {
  return [...lessons].sort((left, right) => {
    if (left.interaction_type === 'video') return -1
    if (right.interaction_type === 'video') return 1
    return 0
  })
}

export function CoursePage() {
  const course = useCourse()
  const [activeUnitIndex, setActiveUnitIndex] = useState(0)
  const [activeStep, setActiveStep] = useState(0)
  const initialized = useRef(false)
  const activeUnit = course.units[activeUnitIndex]
  const lessons = useMemo(
    () => orderExperiences(activeUnit?.lessons ?? []),
    [activeUnit],
  )
  const activeLesson = activeStep < lessons.length ? lessons[activeStep] : null

  useEffect(() => {
    if (initialized.current || !course.units.length) return
    const pendingUnitIndex = course.units.findIndex((unit) => !unit.certificate)
    const initialUnitIndex = pendingUnitIndex === -1 ? course.units.length - 1 : pendingUnitIndex
    setActiveUnitIndex(initialUnitIndex)
    setActiveStep(0)
    initialized.current = true
  }, [course.units])

  useEffect(() => {
    if (!activeUnit || activeStep <= lessons.length) return
    setActiveStep(0)
  }, [activeStep, activeUnit, lessons.length])

  const selectUnit = (index: number) => {
    const unit = course.units[index]
    if (!unit) return
    setActiveUnitIndex(index)
    setActiveStep(0)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const completeExperience = async (
    lesson: LearningItem,
    completed: boolean,
    responseOverride?: InteractionResponse,
    advance = true,
  ) => {
    const saved = await course.updateCompletion(lesson, completed, responseOverride)
    if (saved && completed && advance) {
      setActiveStep((current) => Math.min(current + 1, lessons.length))
      document.querySelector('.course-stage')?.scrollIntoView({ behavior: 'smooth' })
    }
  }

  const canMoveForward = Boolean(activeLesson?.completed)
  const nextUnitAvailable = Boolean(activeUnit?.certificate && course.units[activeUnitIndex + 1])

  return (
    <div className={`page-wrap course-page ${getCourseThemeClass(activeUnit?.slug)}`}>
      <header className="page-header course-header">
        <div>
          <span className="eyebrow">Curso interactivo · aprende, descubre y practica</span>
          <h1>{activeUnit?.title ?? 'Ruta de aprendizaje personalizada'}</h1>
          <p>
            {activeUnit
              ? activeUnit.description
              : 'Completa primero la evaluación para generar tu ruta.'}
          </p>
        </div>
      </header>

      {course.error && <div className="alert alert-danger" role="alert">{course.error}</div>}
      {!course.units.length && !course.error && <div className="skeleton-block" aria-label="Cargando curso" />}
      {course.error && !course.units.length && <p><Link to="/evaluacion">Volver a la evaluación</Link></p>}

      {activeUnit && (
        <div className="course-workspace">
          <main className="course-main-column">
            <CourseSafetyBanner />
            <section className="course-player" aria-labelledby={`unit-${activeUnit.id}`}>
              <div className="course-player-topbar">
                <div>
                  <span className="eyebrow">Unidad {activeUnitIndex + 1} de {course.units.length}</span>
                  <h2 id={`unit-${activeUnit.id}`}>{activeUnit.title}</h2>
                </div>
                <span className="unit-completion">
                  {lessons.filter((lesson) => lesson.completed).length}/{lessons.length} experiencias
                </span>
              </div>

              <div className="course-stage" key={`${activeUnit.id}-${activeStep}`}>
                {activeLesson ? (
                  <LearningExperience
                    lesson={activeLesson}
                    position={activeStep + 1}
                    total={lessons.length}
                    saving={course.savingLessonId === activeLesson.id}
                    response={course.interactionResponses[activeLesson.id] ?? {}}
                    feedback={course.interactionFeedback[activeLesson.id]}
                    onResponseChange={(response) => course.setInteractionResponse(
                      activeLesson.id,
                      response,
                    )}
                    onCompletion={completeExperience}
                  />
                ) : (
                  <ModuleAssessment
                    unit={activeUnit}
                    answers={course.quizAnswers}
                    setAnswers={course.setQuizAnswers}
                    result={course.quizResults[activeUnit.id] ?? null}
                    submitting={course.submittingUnitId === activeUnit.id}
                    onSubmit={course.submitQuiz}
                    onDownload={course.downloadCertificate}
                  />
                )}
              </div>

              <footer className="course-player-controls">
                <button
                  className="btn btn-outline-primary"
                  type="button"
                  disabled={activeStep === 0}
                  onClick={() => setActiveStep((current) => Math.max(0, current - 1))}
                >
                  ← Anterior
                </button>
                {nextUnitAvailable ? (
                  <button
                    className="btn btn-primary"
                    type="button"
                    onClick={() => selectUnit(activeUnitIndex + 1)}
                  >
                    Continuar a la unidad {activeUnitIndex + 2} →
                  </button>
                ) : (
                  <button
                    className="btn btn-primary"
                    type="button"
                    disabled={!canMoveForward || activeStep >= lessons.length}
                    onClick={() => setActiveStep((current) => Math.min(lessons.length, current + 1))}
                  >
                    Siguiente experiencia →
                  </button>
                )}
              </footer>
            </section>
          </main>

          <CourseProgressPanel
            units={course.units}
            activeUnitIndex={activeUnitIndex}
            lessons={lessons}
            activeStep={activeStep}
            progressPercentage={course.progressPercentage}
            onSelectUnit={selectUnit}
            onSelectStep={setActiveStep}
          />
        </div>
      )}
    </div>
  )
}
