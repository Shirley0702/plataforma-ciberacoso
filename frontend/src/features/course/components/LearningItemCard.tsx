import type { LearningItem } from '../types'

interface LearningItemCardProps {
  lesson: LearningItem
  position: number
  isOpen: boolean
  saving: boolean
  selectedChoice?: string
  feedback?: string
  onToggle: () => void
  onChoice: (choice: string) => void
  onCompletion: (lesson: LearningItem, completed: boolean) => Promise<void>
}

export function LearningItemCard({
  lesson,
  position,
  isOpen,
  saving,
  selectedChoice,
  feedback,
  onToggle,
  onChoice,
  onCompletion,
}: LearningItemCardProps) {
  const isActivity = lesson.kind === 'activity'
  const status = lesson.completed ? '✓' : isActivity ? '◆' : position

  return (
    <article className={`lesson-card ${lesson.completed ? 'completed' : ''} ${isActivity ? 'activity-card' : ''}`}>
      <button
        className="lesson-toggle"
        type="button"
        aria-expanded={isOpen}
        aria-controls={`lesson-body-${lesson.id}`}
        onClick={onToggle}
      >
        <span className="lesson-status" aria-hidden="true">{status}</span>
        <span>
          <strong>{lesson.title}</strong>
          <small>{isActivity ? 'Actividad interactiva' : `Lección ${position}`} · {lesson.duration_minutes} min · {lesson.summary}</small>
        </span>
        <span className="chevron" aria-hidden="true">⌄</span>
      </button>

      {isOpen && (
        <div className="lesson-body" id={`lesson-body-${lesson.id}`}>
          <p>{lesson.content}</p>
          {isActivity ? (
            <div className="interactive-activity">
              <h3>{lesson.activity_prompt}</h3>
              <div className="activity-options">
                {lesson.activity_options.map((option) => (
                  <label className={selectedChoice === option.id ? 'selected' : ''} key={option.id}>
                    <input
                      type="radio"
                      name={`activity-${lesson.id}`}
                      checked={selectedChoice === option.id}
                      onChange={() => onChoice(option.id)}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
              {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
              <button
                className="btn btn-primary"
                disabled={saving || (!lesson.completed && !selectedChoice)}
                onClick={() => void onCompletion(lesson, !lesson.completed)}
              >
                {saving ? 'Guardando…' : lesson.completed ? 'Actividad completada' : 'Confirmar decisión'}
              </button>
            </div>
          ) : (
            <div className="lesson-action">
              <span>{lesson.completed ? 'Lección completada' : '¿Terminaste de leer y reflexionar?'}</span>
              <button
                className={`btn ${lesson.completed ? 'btn-outline-primary' : 'btn-primary'}`}
                disabled={saving}
                onClick={() => void onCompletion(lesson, !lesson.completed)}
              >
                {saving ? 'Guardando…' : lesson.completed ? 'Marcar como pendiente' : 'Marcar como completada'}
              </button>
            </div>
          )}
        </div>
      )}
    </article>
  )
}
