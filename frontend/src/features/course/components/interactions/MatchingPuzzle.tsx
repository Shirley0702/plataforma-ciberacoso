import { useState } from 'react'
import type { InteractionItem } from '../../types'

interface MatchingPuzzleProps {
  items: InteractionItem[]
  matches: Record<string, string>
  completed: boolean
  feedback?: string
  saving: boolean
  onChange: (matches: Record<string, string>) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function MatchingPuzzle({
  items,
  matches,
  completed,
  feedback,
  saving,
  onChange,
  onCompletion,
}: MatchingPuzzleProps) {
  const [checked, setChecked] = useState(false)
  const visibleMatches = completed
    ? Object.fromEntries(items.map((item) => [item.id, item.id]))
    : matches
  const shuffledMeanings = [...items].reverse()
  const allConnected = items.length > 0 && items.every((item) => visibleMatches[item.id])
  const solved = allConnected && items.every((item) => visibleMatches[item.id] === item.id)

  const updateMatch = (itemId: string, meaningId: string) => {
    setChecked(false)
    onChange({ ...visibleMatches, [itemId]: meaningId })
  }

  const checkConnections = () => {
    setChecked(true)
    if (solved) void onCompletion(true)
  }

  return (
    <div className="matching-puzzle">
      <div className="matching-board">
        {items.map((item, index) => {
          const isIncorrect = checked && visibleMatches[item.id] !== item.id
          return (
            <div className={`matching-row ${isIncorrect ? 'needs-review' : ''}`} key={item.id}>
              <span className="matching-number" aria-hidden="true">{index + 1}</span>
              <label htmlFor={`match-${item.id}`}>
                <strong>{item.label}</strong>
                <span>Conecta esta idea con su significado:</span>
              </label>
              <select
                id={`match-${item.id}`}
                value={visibleMatches[item.id] ?? ''}
                disabled={completed}
                aria-invalid={isIncorrect}
                onChange={(event) => updateMatch(item.id, event.target.value)}
              >
                <option value="">Selecciona una conexión</option>
                {shuffledMeanings.map((meaning) => (
                  <option value={meaning.id} key={meaning.id}>{meaning.detail}</option>
                ))}
              </select>
              {isIncorrect && (
                <small role="alert">Esta conexión no encaja todavía. Vuelve a leer ambas ideas.</small>
              )}
            </div>
          )
        })}
      </div>
      <p className="interaction-hint">
        Puedes probar cuantas veces necesites. No se asigna una calificación.
      </p>
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status">✓ Todas las conexiones están construidas</p>
      ) : (
        <button
          className="btn btn-primary"
          type="button"
          disabled={saving || !allConnected}
          onClick={checkConnections}
        >
          {saving ? 'Guardando…' : 'Comprobar conexiones'}
        </button>
      )}
    </div>
  )
}
