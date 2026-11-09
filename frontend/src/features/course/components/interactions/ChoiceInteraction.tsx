import type { InteractionOption } from '../../types'

interface ChoiceInteractionProps {
  lessonId: number
  options: InteractionOption[]
  selectedOption?: string
  completed: boolean
  feedback?: string
  saving: boolean
  actionLabel: string
  onSelect: (optionId: string) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function ChoiceInteraction({
  lessonId,
  options,
  selectedOption,
  completed,
  feedback,
  saving,
  actionLabel,
  onSelect,
  onCompletion,
}: ChoiceInteractionProps) {
  return (
    <div className="choice-interaction">
      <div className="activity-options" role="radiogroup" aria-label="Alternativas">
        {options.map((option) => (
          <label className={selectedOption === option.id ? 'selected' : ''} key={option.id}>
            <input
              type="radio"
              name={`interaction-${lessonId}`}
              checked={selectedOption === option.id}
              disabled={completed}
              onChange={() => onSelect(option.id)}
            />
            <span>{option.label}</span>
          </label>
        ))}
      </div>
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      <button
        className={`btn ${completed ? 'btn-outline-primary' : 'btn-primary'}`}
        type="button"
        disabled={saving || (!completed && !selectedOption)}
        onClick={() => void onCompletion(!completed)}
      >
        {saving ? 'Guardando…' : completed ? 'Marcar como pendiente' : actionLabel}
      </button>
    </div>
  )
}
