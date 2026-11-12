import { useState } from 'react'
import type { InteractionItem } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

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
  const [selectedClueId, setSelectedClueId] = useState<string | null>(null)
  const [checked, setChecked] = useState(false)
  const visibleMatches = completed
    ? Object.fromEntries(items.map((item) => [item.id, item.id]))
    : matches
  const shuffledMeanings = [...items].reverse()
  const allConnected = items.length > 0 && items.every((item) => visibleMatches[item.id])
  const solved = allConnected && items.every((item) => visibleMatches[item.id] === item.id)

  const connectMeaning = (meaningId: string) => {
    if (!selectedClueId || completed) return
    const nextMatches = Object.fromEntries(
      Object.entries(visibleMatches).filter(([, currentMeaningId]) => currentMeaningId !== meaningId),
    )
    nextMatches[selectedClueId] = meaningId
    setChecked(false)
    setSelectedClueId(null)
    onChange(nextMatches)
  }

  const checkConnections = () => {
    setChecked(true)
    if (solved) void onCompletion(true)
  }

  return (
    <div className="matching-puzzle">
      <div className="matching-instructions" aria-live="polite">
        <PuzzleIcon name="connect" />
        <span>
          <strong>{selectedClueId ? 'Ahora elige su significado' : 'Selecciona una idea'}</strong>
          <small>Construye cada conexión entre las dos columnas.</small>
        </span>
      </div>

      <div className="matching-board">
        <section className="matching-column" aria-label="Ideas para conectar">
          <h4>Ideas</h4>
          {items.map((item, index) => {
            const currentMeaning = visibleMatches[item.id]
            const isIncorrect = checked && currentMeaning !== item.id
            return (
              <button
                className={`matching-card clue ${selectedClueId === item.id ? 'selected' : ''} ${currentMeaning ? 'connected' : ''} ${isIncorrect ? 'needs-review' : ''}`}
                type="button"
                aria-pressed={selectedClueId === item.id}
                disabled={completed}
                onClick={() => {
                  setChecked(false)
                  setSelectedClueId(item.id)
                }}
                key={item.id}
              >
                <span>{index + 1}</span>
                <strong>{item.label}</strong>
                {currentMeaning && <small>Conexión creada</small>}
              </button>
            )
          })}
        </section>

        <div className="matching-connector" aria-hidden="true">
          <PuzzleIcon name="connect" size={36} />
        </div>

        <section className="matching-column" aria-label="Significados disponibles">
          <h4>Significados</h4>
          {shuffledMeanings.map((meaning) => {
            const connectedClueId = Object.keys(visibleMatches).find(
              (clueId) => visibleMatches[clueId] === meaning.id,
            )
            return (
              <button
                className={`matching-card meaning ${connectedClueId ? 'connected' : ''}`}
                type="button"
                disabled={completed || !selectedClueId}
                onClick={() => connectMeaning(meaning.id)}
                key={meaning.id}
              >
                <PuzzleIcon name={connectedClueId ? 'check' : 'connect'} size={20} />
                <span>{meaning.detail}</span>
              </button>
            )
          })}
        </section>
      </div>

      {checked && !solved && (
        <p className="matching-feedback" role="alert">
          Algunas piezas no encajan todavía. Las tarjetas marcadas necesitan una conexión diferente.
        </p>
      )}
      <p className="interaction-hint">
        Puedes reorganizar las conexiones y probar nuevamente sin penalización.
      </p>
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Conexiones completadas</p>
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
