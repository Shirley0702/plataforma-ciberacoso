import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionOption, InteractionResponse } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'
import { PuzzleGuide } from './PuzzleGuide'

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
  const exploredIds = completed ? options.map((option) => option.id) : exploredOptionIds
  const exploredAll = options.length > 0 && exploredIds.length === options.length
  const chosenOption = options.find((option) => option.id === chosenOptionId)

  const explorePath = (optionId: string) => {
    if (completed || saving || exploredIds.includes(optionId)) return
    onChange([...exploredIds, optionId], chosenOptionId)
  }

  const choosePath = (option: InteractionOption) => {
    if (completed || saving || !exploredAll) return
    onChange(exploredIds, option.id)
    if (option.recommended) {
      void onCompletion(true, {
        selected_items: exploredIds,
        chosen_option: option.id,
      })
    }
  }

  return (
    <div className="decision-map-puzzle">
      <PuzzleGuide
        icon="route"
        title="Abre los caminos y compara qué ocurre"
        summary={prompt}
        steps={[
          'Abre cada camino del tablero.',
          'Lee la consecuencia que produce esa acción.',
          'Cuando conozcas las tres, elige la que conserva más control y opciones.',
        ]}
        completion="explores todos los caminos y elijas el más protector."
      />

      <figure className="decision-panorama">
        <img src={visual.src} alt={visual.alt} />
        <figcaption><PuzzleIcon name="play" size={16} /> Recuerda el video: {visual.videoCue}</figcaption>
      </figure>

      <section className="decision-board" aria-label="Tablero de caminos y consecuencias">
        <div className="decision-start">
          <PuzzleIcon name="compass" size={21} />
          <span>Situación</span>
        </div>
        <div className="decision-route-line" aria-hidden="true" />
        <div className="decision-paths">
          {options.map((option, index) => {
            const revealed = exploredIds.includes(option.id)
            return (
              <article className={`decision-card ${revealed ? 'revealed' : ''}`} key={option.id}>
                <span className="decision-card-number">Camino {index + 1}</span>
                <span className="decision-card-icon"><PuzzleIcon name={PATH_ICONS[index] ?? 'route'} size={25} /></span>
                <h4>{option.label}</h4>
                {revealed ? (
                  <div className="decision-consequence">
                    <PuzzleIcon name="outcome" size={19} />
                    <p><strong>Qué produciría:</strong> {option.feedback}</p>
                  </div>
                ) : (
                  <button
                    type="button"
                    disabled={saving}
                    aria-label={`Explorar camino ${index + 1}: ${option.label}`}
                    onClick={() => explorePath(option.id)}
                  >
                    Ver qué ocurre <PuzzleIcon name="arrow" size={17} />
                  </button>
                )}
              </article>
            )
          })}
        </div>
      </section>

      <div className="decision-progress" aria-live="polite">
        <span>{exploredAll ? 'Ya conoces las consecuencias. Elige un camino.' : 'Caminos explorados'}</span>
        <strong>{exploredIds.length}/{options.length}</strong>
      </div>

      {exploredAll && !completed && (
        <section className="decision-final-choice" aria-label="Elección final">
          <div>
            <span>Decisión final</span>
            <strong>¿Cuál mantiene más control y deja abiertas más opciones?</strong>
          </div>
          <div>
            {options.map((option, index) => (
              <button
                className={chosenOptionId === option.id ? 'selected' : ''}
                type="button"
                disabled={saving}
                aria-label={`Elegir camino ${index + 1}: ${option.label}`}
                onClick={() => choosePath(option)}
                key={option.id}
              >
                Camino {index + 1}
              </button>
            ))}
          </div>
        </section>
      )}

      {chosenOption && !chosenOption.recommended && !completed && (
        <p className="consequence-review" role="alert">
          Ese camino reduce opciones o aumenta el riesgo. Compara nuevamente las consecuencias y prueba otro.
        </p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed && <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Camino protector identificado</p>}
    </div>
  )
}
