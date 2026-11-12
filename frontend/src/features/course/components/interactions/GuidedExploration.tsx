import { useState } from 'react'
import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionCard } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

interface GuidedExplorationProps {
  cards: InteractionCard[]
  prompt: string
  visual: CoursePuzzleVisual
  completed: boolean
  feedback?: string
  saving: boolean
  onCompletion: (completed: boolean) => Promise<void>
}

const SOLVED_ORDER = [0, 1, 2, 3, 4, 5]
const SCRAMBLED_ORDER = [4, 0, 5, 2, 1, 3]

function isSolved(order: number[]) {
  return order.every((tile, position) => tile === position)
}

export function GuidedExploration({
  cards,
  prompt,
  visual,
  completed,
  feedback,
  saving,
  onCompletion,
}: GuidedExplorationProps) {
  const [tileOrder, setTileOrder] = useState(() => completed ? SOLVED_ORDER : SCRAMBLED_ORDER)
  const [selectedPosition, setSelectedPosition] = useState<number | null>(null)
  const visibleOrder = completed ? SOLVED_ORDER : tileOrder
  const misplacedTiles = visibleOrder.filter((tile, position) => tile !== position).length

  const selectTile = (position: number) => {
    if (completed || saving) return
    if (selectedPosition === null) {
      setSelectedPosition(position)
      return
    }
    if (selectedPosition === position) {
      setSelectedPosition(null)
      return
    }

    const nextOrder = [...visibleOrder]
    ;[nextOrder[selectedPosition], nextOrder[position]] = [
      nextOrder[position],
      nextOrder[selectedPosition],
    ]
    setTileOrder(nextOrder)
    setSelectedPosition(null)
    if (isSolved(nextOrder)) void onCompletion(true)
  }

  return (
    <div className="guided-exploration mosaic-puzzle">
      <header className="puzzle-instruction">
        <span><PuzzleIcon name="mosaic" size={26} /></span>
        <div>
          <strong>Reconstruye la escena</strong>
          <p>{prompt} Selecciona dos piezas para intercambiarlas.</p>
        </div>
      </header>

      <div className="mosaic-layout">
        <div className="mosaic-board" role="group" aria-label="Mosaico de seis piezas">
          {visibleOrder.map((tile, position) => {
            const column = tile % 3
            const row = Math.floor(tile / 3)
            return (
              <button
                className={`mosaic-tile ${selectedPosition === position ? 'selected' : ''} ${tile === position ? 'correct' : ''}`}
                type="button"
                aria-label={`Pieza en la posición ${position + 1}${selectedPosition === position ? ', seleccionada' : ''}`}
                aria-pressed={selectedPosition === position}
                disabled={completed || saving}
                onClick={() => selectTile(position)}
                style={{
                  backgroundImage: `url(${visual.src})`,
                  backgroundPosition: `${column * 50}% ${row * 100}%`,
                }}
                key={`${position}-${tile}`}
              >
                <span>{position + 1}</span>
              </button>
            )
          })}
        </div>

        <aside className="mosaic-clues">
          <figure>
            <img src={visual.src} alt={visual.alt} />
            <figcaption><PuzzleIcon name="play" size={16} /> Pista visual del video</figcaption>
          </figure>
          <p>{visual.videoCue}</p>
          <div className="mosaic-status" aria-live="polite">
            <span>{completed || misplacedTiles === 0 ? 'Imagen reconstruida' : 'Piezas por ubicar'}</span>
            <strong>{completed ? 0 : misplacedTiles}</strong>
          </div>
        </aside>
      </div>

      <section className={`discovery-strip ${completed ? 'unlocked' : ''}`} aria-label="Pistas de aprendizaje">
        <h4>{completed ? 'Lo que revela la escena' : 'Completa la imagen para revelar las pistas'}</h4>
        <div>
          {cards.map((card, index) => (
            <article key={card.title}>
              <PuzzleIcon name={['observe', 'boundary', 'support'][index] ?? 'clue'} size={22} />
              <span><strong>{card.title}</strong><small>{completed ? card.body : 'Pista bloqueada'}</small></span>
            </article>
          ))}
        </div>
      </section>

      {selectedPosition !== null && !completed && (
        <p className="interaction-hint" role="status">Ahora selecciona la pieza con la que quieres intercambiarla.</p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed && (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Mosaico resuelto</p>
      )}
    </div>
  )
}
