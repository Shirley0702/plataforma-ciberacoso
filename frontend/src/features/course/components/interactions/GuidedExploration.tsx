import { useEffect, useState } from 'react'
import type { InteractionCard } from '../../types'

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
      <div className="puzzle-progress" aria-live="polite">
        <span>Pistas descubiertas</span>
        <strong>{revealedCards.size}/{cards.length}</strong>
      </div>
      <div className="guided-cards">
        {cards.map((card, index) => {
          const revealed = revealedCards.has(index)
          return (
            <button
              className={`guided-card ${revealed ? 'revealed' : ''}`}
              type="button"
              aria-expanded={revealed}
              disabled={completed}
              onClick={() => revealCard(index)}
              key={card.title}
            >
              <span>{revealed ? '✓' : index + 1}</span>
              <strong>{card.title}</strong>
              {revealed && <small>{card.body}</small>}
            </button>
          )
        })}
      </div>
      {!exploredAll && !completed && (
        <p className="interaction-hint">
          Abre las {cards.length} pistas. Cada una añade una pieza a la idea principal.
        </p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status">✓ Pistas aprendidas</p>
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
