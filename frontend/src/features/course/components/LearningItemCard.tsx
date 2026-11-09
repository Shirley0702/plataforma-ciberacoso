import type { InteractionResponse, InteractionType, LearningItem } from '../types'
import { InteractionPanel } from './interactions/InteractionPanel'

const INTERACTION_LABELS: Record<InteractionType, string> = {
  guided: 'Exploración guiada',
  decision: 'Decisión con consecuencias',
  checklist: 'Lista interactiva',
  practice: 'Práctica segura',
  safety_plan: 'Plan personal seguro',
}

interface LearningItemCardProps {
  lesson: LearningItem
  position: number
  isOpen: boolean
  saving: boolean
  response: InteractionResponse
  feedback?: string
  onToggle: () => void
  onResponseChange: (response: InteractionResponse) => void
  onCompletion: (lesson: LearningItem, completed: boolean) => Promise<void>
}

export function LearningItemCard({
  lesson,
  position,
  isOpen,
  saving,
  response,
  feedback,
  onToggle,
  onResponseChange,
  onCompletion,
}: LearningItemCardProps) {
  const status = lesson.completed ? '✓' : position

  return (
    <article className={`lesson-card interaction-${lesson.interaction_type} ${lesson.completed ? 'completed' : ''}`}>
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
          <small>
            {INTERACTION_LABELS[lesson.interaction_type]} · {lesson.duration_minutes} min · {lesson.summary}
          </small>
        </span>
        <span className="chevron" aria-hidden="true">⌄</span>
      </button>

      {isOpen && (
        <div className="lesson-body" id={`lesson-body-${lesson.id}`}>
          <p>{lesson.content}</p>
          <section className="interactive-activity" aria-label={INTERACTION_LABELS[lesson.interaction_type]}>
            <h3>{lesson.interaction_prompt}</h3>
            <InteractionPanel
              lesson={lesson}
              response={response}
              feedback={feedback}
              saving={saving}
              onResponseChange={onResponseChange}
              onCompletion={(completed) => onCompletion(lesson, completed)}
            />
          </section>
        </div>
      )}
    </article>
  )
}
