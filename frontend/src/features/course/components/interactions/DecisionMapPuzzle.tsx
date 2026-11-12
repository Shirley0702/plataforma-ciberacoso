import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionOption, InteractionResponse } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

interface DecisionMapPuzzleProps {
  options: InteractionOption[]
  exploredOptionIds: string[]
  chosenOptionId?: string
  completed: boolean
  feedback?: string
  saving: boolean
  prompt: string
  visual: CoursePuzzleVisual
  onChange: (optionIds: string[], chosenOptionId?: string) => void
  onCompletion: (completed: boolean, response?: InteractionResponse) => Promise<void>
}

const PATH_ICONS = ['broadcast', 'shield', 'escalate']

export function DecisionMapPuzzle({
  options,
  exploredOptionIds,
  chosenOptionId,
  completed,
  feedback,
  saving,
  prompt,
  visual,
  onChange,
  onCompletion,
}: DecisionMapPuzzleProps) {
  const visibleOptionIds = completed ? options.map((option) => option.id) : exploredOptionIds
  const exploredAll = options.length > 0 && visibleOptionIds.length === options.length
  const chosenOption = options.find((option) => option.id === chosenOptionId)

  const activatePath = (option: InteractionOption) => {
    if (completed || saving) return
    if (!visibleOptionIds.includes(option.id)) {
      onChange([...visibleOptionIds, option.id], chosenOptionId)
      return
    }
    if (!exploredAll) return

    onChange(visibleOptionIds, option.id)
    if (option.recommended) {
      void onCompletion(true, {
        selected_items: visibleOptionIds,
        chosen_option: option.id,
      })
    }
  }

  return (
    <div className="decision-map-puzzle">
      <header className="puzzle-instruction">
        <span><PuzzleIcon name="route" size={26} /></span>
        <div><strong>Abre el mapa y compara las consecuencias</strong><p>{prompt}</p></div>
      </header>

      <div className="decision-map-layout">
        <figure className="puzzle-scene decision-scene">
          <img src={visual.src} alt={visual.alt} />
          <figcaption><PuzzleIcon name="play" size={16} /> {visual.videoCue}</figcaption>
        </figure>
        <div className="decision-tree">
          <div className="decision-origin"><PuzzleIcon name="compass" size={22} /><span>Situación inicial</span></div>
          <div className="decision-branches" role="group" aria-label="Caminos posibles">
            {options.map((option, index) => {
              const revealed = visibleOptionIds.includes(option.id)
              const chosen = chosenOptionId === option.id
              return (
                <button
                  className={`decision-path ${revealed ? 'revealed' : ''} ${chosen ? 'chosen' : ''}`}
                  type="button"
                  aria-expanded={revealed}
                  aria-pressed={chosen}
                  disabled={completed || saving}
                  onClick={() => activatePath(option)}
                  key={option.id}
                >
                  <span className="decision-path-icon"><PuzzleIcon name={option.recommended ? 'shield' : PATH_ICONS[index]} size={26} /></span>
                  <span className="decision-path-copy">
                    <small>Camino {index + 1}</small>
                    <strong>{option.label}</strong>
                    <em>{revealed ? option.feedback : 'Abrir este camino'}</em>
                  </span>
                </button>
              )
            })}
          </div>
        </div>
      </div>

      <div className="map-progress" aria-live="polite">
        <span>{exploredAll ? 'Mapa completo: ahora elige el camino que conserva más opciones.' : 'Explora cada camino antes de decidir.'}</span>
        <strong>{visibleOptionIds.length}/{options.length}</strong>
      </div>
      {chosenOption && !chosenOption.recommended && !completed && (
        <p className="consequence-review" role="alert">Esa ruta reduce opciones o aumenta el riesgo. Usa lo observado en el mapa y prueba otra.</p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed && <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Mapa resuelto</p>}
    </div>
  )
}
