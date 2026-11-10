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
      <span className="experience-progress-label">
        Paso {activeStep + 1} de {lessons.length + 1}
      </span>
      <div className="experience-steps">
        {lessons.map((lesson, index) => {
          const available = index <= lastAvailableLesson
          return (
            <button
              className={`experience-step ${activeStep === index ? 'active' : ''} ${lesson.completed ? 'completed' : ''}`}
              type="button"
              disabled={!available}
              aria-current={activeStep === index ? 'step' : undefined}
              aria-label={`Experiencia ${index + 1}: ${lesson.title}${lesson.completed ? ', completada' : ''}`}
              onClick={() => onSelect(index)}
              key={lesson.id}
            >
              <span aria-hidden="true">{lesson.completed ? '✓' : index + 1}</span>
            </button>
          )
        })}
        <button
          className={`experience-step quiz-step ${activeStep === lessons.length ? 'active' : ''}`}
          type="button"
          disabled={!quizUnlocked}
          aria-current={activeStep === lessons.length ? 'step' : undefined}
          aria-label="Reto final de la unidad"
          onClick={() => onSelect(lessons.length)}
        >
          <span aria-hidden="true">★</span>
        </button>
      </div>
    </nav>
  )
}
