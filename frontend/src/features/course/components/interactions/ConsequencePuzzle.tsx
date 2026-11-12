import type { InteractionOption, InteractionResponse } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

interface ConsequencePuzzleProps {
  options: InteractionOption[]
  exploredOptionIds: string[]
  chosenOptionId?: string
  completed: boolean
  feedback?: string
  saving: boolean
  variant: 'decision' | 'practice'
  onChange: (optionIds: string[], chosenOptionId?: string) => void
  onCompletion: (completed: boolean, response?: InteractionResponse) => Promise<void>
}

export function ConsequencePuzzle({
  options,
  exploredOptionIds,
  chosenOptionId,
  completed,
  feedback,
  saving,
  variant,
  onChange,
  onCompletion,
}: ConsequencePuzzleProps) {
  const visibleOptionIds = completed
    ? options.map((option) => option.id)
    : exploredOptionIds
  const exploredAll = options.length > 0 && visibleOptionIds.length === options.length
  const chosenOption = options.find((option) => option.id === chosenOptionId)

  const revealConsequence = (optionId: string) => {
    if (completed || visibleOptionIds.includes(optionId)) return
    onChange([...visibleOptionIds, optionId], chosenOptionId)
  }

  const choosePath = (option: InteractionOption) => {
    if (completed || !exploredAll) return
    onChange(visibleOptionIds, option.id)
    if (option.recommended) {
      void onCompletion(true, {
        selected_items: visibleOptionIds,
        chosen_option: option.id,
      })
    }
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
              className={`consequence-card ${revealed ? 'revealed' : ''} ${chosenOptionId === option.id ? 'chosen' : ''}`}
              type="button"
              aria-expanded={revealed}
              aria-pressed={chosenOptionId === option.id}
              disabled={completed}
              onClick={() => (revealed && exploredAll
                ? choosePath(option)
                : revealConsequence(option.id))}
              key={option.id}
            >
              <span className="consequence-route-visual" aria-hidden="true">
                <PuzzleIcon name={variant === 'practice' ? 'chat' : 'route'} size={34} />
                <small>Ruta {index + 1}</small>
              </span>
              <span className="consequence-copy">
                <strong>{option.label}</strong>
                <em>
                  {revealed
                    ? exploredAll ? 'Seleccionar este camino' : 'Consecuencia descubierta'
                    : 'Descubrir qué ocurre'}
                </em>
                {revealed && <small>{option.feedback}</small>}
              </span>
            </button>
          )
        })}
      </div>
      {!exploredAll && !completed && (
        <p className="interaction-hint">
          Primero abre los tres caminos. Después podrás elegir usando lo aprendido en el video.
        </p>
      )}
      {exploredAll && !completed && (
        <div className="consequence-choice" aria-live="polite">
          <PuzzleIcon name="route" size={22} />
          <span>
            <strong>Ahora resuelve el puzzle</strong>
            Elige el camino que protege a la persona, conserva opciones y evita aumentar el riesgo.
          </span>
        </div>
      )}
      {chosenOption && !chosenOption.recommended && !completed && (
        <p className="consequence-review" role="alert">
          Esa ruta puede aumentar el riesgo o reducir opciones. Revisa las consecuencias y prueba otro camino.
        </p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Camino resuelto</p>
      ) : saving ? <p className="interaction-hint" role="status">Guardando tu solución…</p> : null}
    </div>
  )
}
