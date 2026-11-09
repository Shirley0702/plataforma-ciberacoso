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

  const toggleCard = (index: number) => {
    setRevealedCards((current) => {
      const next = new Set(current)
      if (next.has(index)) next.delete(index)
      else next.add(index)
      return next
    })
  }
  const exploredAll = revealedCards.size === cards.length

  return (
    <div className="guided-exploration">
      <div className="guided-cards">
        {cards.map((card, index) => {
          const revealed = revealedCards.has(index)
          return (
            <button
              className={`guided-card ${revealed ? 'revealed' : ''}`}
              type="button"
              aria-expanded={revealed}
              onClick={() => toggleCard(index)}
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
        <p className="interaction-hint">Abre las {cards.length} tarjetas para continuar.</p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      <button
        className={`btn ${completed ? 'btn-outline-primary' : 'btn-primary'}`}
        type="button"
        disabled={saving || (!completed && !exploredAll)}
        onClick={() => void onCompletion(!completed)}
      >
        {saving ? 'Guardando…' : completed ? 'Marcar como pendiente' : 'Completar exploración'}
      </button>
    </div>
  )
}
