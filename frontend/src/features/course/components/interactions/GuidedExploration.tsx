import { useEffect, useState } from 'react'
import type { InteractionCard } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

interface GuidedExplorationProps {
  cards: InteractionCard[]
  completed: boolean
  feedback?: string
  saving: boolean
  onCompletion: (completed: boolean) => Promise<void>
}

export function GuidedExploration({
  cards,
  completed,
  feedback,
  saving,
  onCompletion,
}: GuidedExplorationProps) {
  const [revealedCards, setRevealedCards] = useState<Set<number>>(
    () => new Set(completed ? cards.map((_, index) => index) : []),
  )

  useEffect(() => {
    if (completed) setRevealedCards(new Set(cards.map((_, index) => index)))
  }, [cards, completed])

  const revealCard = (index: number) => {
    setRevealedCards((current) => {
      if (current.has(index)) return current
      const next = new Set(current)
      next.add(index)
      return next
    })
  }
  const exploredAll = revealedCards.size === cards.length

  return (
    <div className="guided-exploration">
      <div className="puzzle-board-heading">
        <span><PuzzleIcon name="puzzle" size={28} /></span>
        <div>
          <strong>Arma el tablero de pistas</strong>
          <small>Abre cada pieza y relaciónala con la escena y el video.</small>
        </div>
      </div>
      <div className="puzzle-progress" aria-live="polite">
        <span>Piezas colocadas</span>
        <strong>{revealedCards.size}/{cards.length}</strong>
      </div>
      <div className="guided-cards">
        {cards.map((card, index) => {
          const revealed = revealedCards.has(index)
          return (
            <button
              className={`guided-card guided-piece ${revealed ? 'revealed' : ''}`}
              type="button"
              aria-expanded={revealed}
              disabled={completed}
              onClick={() => revealCard(index)}
              key={card.title}
            >
              <span className="guided-card-inner">
                <span className="guided-card-face guided-card-front">
                  <span className="guided-card-icon"><PuzzleIcon name="clue" /></span>
                  <small>Pieza {index + 1}</small>
                  <strong>{card.title}</strong>
                  <em>Girar la pieza</em>
                </span>
                <span className="guided-card-face guided-card-back">
                  <span className="guided-card-icon"><PuzzleIcon name="check" /></span>
                  <strong>{card.title}</strong>
                  <small>{card.body}</small>
                </span>
              </span>
            </button>
          )
        })}
      </div>
      {!exploredAll && !completed && (
        <p className="interaction-hint">
          Gira las {cards.length} piezas. Cuando estén visibles podrás guardar el tablero completo.
        </p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Tablero completado</p>
      ) : (
        <button
          className="btn btn-primary"
          type="button"
          disabled={saving || !exploredAll}
          onClick={() => void onCompletion(true)}
        >
          {saving ? 'Guardando…' : 'Guardar lo aprendido'}
        </button>
      )}
    </div>
  )
}
