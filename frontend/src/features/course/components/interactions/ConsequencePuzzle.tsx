import type { InteractionOption } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

interface ConsequencePuzzleProps {
  options: InteractionOption[]
  exploredOptionIds: string[]
  completed: boolean
  feedback?: string
  saving: boolean
  actionLabel: string
  variant: 'decision' | 'practice'
  onChange: (optionIds: string[]) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function ConsequencePuzzle({
  options,
  exploredOptionIds,
  completed,
  feedback,
  saving,
  actionLabel,
  variant,
  onChange,
  onCompletion,
}: ConsequencePuzzleProps) {
  const visibleOptionIds = completed
    ? options.map((option) => option.id)
    : exploredOptionIds
  const exploredAll = options.length > 0 && visibleOptionIds.length === options.length

  const revealConsequence = (optionId: string) => {
    if (completed || visibleOptionIds.includes(optionId)) return
    onChange([...visibleOptionIds, optionId])
  }

  return (
    <div className={`consequence-puzzle consequence-${variant}`}>
      <div className="puzzle-progress" aria-live="polite">
        <span>Rutas descubiertas</span>
        <strong>{visibleOptionIds.length}/{options.length}</strong>
      </div>
      <div className="consequence-paths">
        {options.map((option, index) => {
          const revealed = visibleOptionIds.includes(option.id)
          return (
            <button
              className={`consequence-card ${revealed ? 'revealed' : ''}`}
              type="button"
              aria-expanded={revealed}
              disabled={completed}
              onClick={() => revealConsequence(option.id)}
              key={option.id}
            >
              <span className="consequence-route-visual" aria-hidden="true">
                <PuzzleIcon name={variant === 'practice' ? 'chat' : 'route'} size={34} />
                <small>Ruta {index + 1}</small>
              </span>
              <span className="consequence-copy">
                <strong>{option.label}</strong>
                <em>{revealed ? 'Consecuencia descubierta' : 'Explorar consecuencia'}</em>
                {revealed && <small>{option.feedback}</small>}
              </span>
            </button>
          )
        })}
      </div>
      {!exploredAll && !completed && (
        <p className="interaction-hint">
          Abre cada camino. Aquí no hay nota: el objetivo es descubrir qué puede ocurrir.
        </p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status">✓ Aprendizaje guardado</p>
      ) : (
        <button
          className="btn btn-primary"
          type="button"
          disabled={saving || !exploredAll}
          onClick={() => void onCompletion(true)}
        >
          {saving ? 'Guardando…' : actionLabel}
        </button>
      )}
    </div>
  )
}
