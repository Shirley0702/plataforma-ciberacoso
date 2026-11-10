import type { LearningItem } from '../types'

interface CourseStepNavigatorProps {
  lessons: LearningItem[]
  activeStep: number
  quizUnlocked: boolean
  onSelect: (index: number) => void
}

export function CourseStepNavigator({
  lessons,
  activeStep,
  quizUnlocked,
  onSelect,
}: CourseStepNavigatorProps) {
  const firstIncomplete = lessons.findIndex((lesson) => !lesson.completed)
  const lastAvailableLesson = firstIncomplete === -1 ? lessons.length - 1 : firstIncomplete

  return (
    <nav className="experience-progress" aria-label="Progreso de la unidad">
      <span className="experience-progress-label">Paso {activeStep + 1} de {lessons.length + 1}</span>
      <div className="experience-steps">
        {lessons.map((lesson, index) => {
          const available = index <= lastAvailableLesson
          return (
            <button
              className={`experience-step ${activeStep === index ? 'active' : ''} ${lesson.completed ? 'completed' : ''}`}
              type="button"
              disabled={!available}
              aria-current={activeStep === index ? 'step' : undefined}
              onClick={() => onSelect(index)}
              key={lesson.id}
            >
              <span className="experience-step-marker" aria-hidden="true">{lesson.completed ? '✓' : index + 1}</span>
              <span className="experience-step-copy">
                <strong>Experiencia {index + 1}</strong>
                <small>{lesson.title}</small>
                {lesson.completed && <span className="visually-hidden">, completada</span>}
              </span>
            </button>
          )
        })}
        <button
          className={`experience-step quiz-step ${activeStep === lessons.length ? 'active' : ''}`}
          type="button"
          disabled={!quizUnlocked}
          aria-current={activeStep === lessons.length ? 'step' : undefined}
          onClick={() => onSelect(lessons.length)}
        >
          <span className="experience-step-marker" aria-hidden="true">★</span>
          <span className="experience-step-copy">
            <strong>Reto final</strong>
            <small>Comprueba lo aprendido</small>
          </span>
        </button>
      </div>
    </nav>
  )
}
