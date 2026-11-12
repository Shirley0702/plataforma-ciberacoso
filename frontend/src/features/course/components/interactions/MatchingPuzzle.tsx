import { useState } from 'react'
import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionItem } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

interface MatchingPuzzleProps {
  items: InteractionItem[]
  matches: Record<string, string>
  prompt: string
  visual: CoursePuzzleVisual
  completed: boolean
  feedback?: string
  saving: boolean
  onChange: (matches: Record<string, string>) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function MatchingPuzzle({
  items,
  matches,
  prompt,
  visual,
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
    <div className="matching-puzzle visual-matching-puzzle">
      <header className="puzzle-instruction">
        <span><PuzzleIcon name="connect" size={26} /></span>
        <div><strong>Encaja cada señal con lo que significa</strong><p>{prompt}</p></div>
      </header>

      <div className="matching-visual-layout">
        <figure className="puzzle-scene matching-scene">
          <img src={visual.src} alt={visual.alt} />
          <figcaption><PuzzleIcon name="play" size={16} /> {visual.videoCue}</figcaption>
        </figure>

        <div className="matching-workbench">
          <section className="matching-piece-tray" aria-label="Señales para conectar">
            <h4>Piezas con señales</h4>
            {items.map((item) => {
              const currentMeaning = visibleMatches[item.id]
              const isIncorrect = checked && currentMeaning !== item.id
              return (
                <button
                  className={`matching-piece ${selectedClueId === item.id ? 'selected' : ''} ${currentMeaning ? 'connected' : ''} ${isIncorrect ? 'needs-review' : ''}`}
                  type="button"
                  aria-pressed={selectedClueId === item.id}
                  disabled={completed}
                  onClick={() => {
                    setChecked(false)
                    setSelectedClueId(item.id)
                  }}
                  key={item.id}
                >
                  <span><PuzzleIcon name={item.visual || 'clue'} size={23} /></span>
                  <strong>{item.label}</strong>
                  <small>{currentMeaning ? 'Conectada' : 'Seleccionar'}</small>
                </button>
              )
            })}
          </section>

          <section className="matching-slot-board" aria-label="Significados disponibles">
            <h4>{selectedClueId ? 'Ahora elige dónde encaja' : 'Espacios de significado'}</h4>
            {shuffledMeanings.map((meaning) => {
              const connectedClueId = Object.keys(visibleMatches).find(
                (clueId) => visibleMatches[clueId] === meaning.id,
              )
              return (
                <button
                  className={`matching-slot ${connectedClueId ? 'filled' : ''}`}
                  type="button"
                  disabled={completed || !selectedClueId}
                  onClick={() => connectMeaning(meaning.id)}
                  key={meaning.id}
                >
                  <span className="slot-notch" aria-hidden="true" />
                  <PuzzleIcon name={connectedClueId ? 'check' : 'puzzle'} size={20} />
                  <span>{meaning.detail}</span>
                </button>
              )
            })}
          </section>
        </div>
      </div>

      {checked && !solved && (
        <p className="matching-feedback" role="alert">Algunas piezas no encajan todavía. Las señales marcadas necesitan otro espacio.</p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Conexiones completadas</p>
      ) : (
        <button className="btn btn-primary" type="button" disabled={saving || !allConnected} onClick={checkConnections}>
          {saving ? 'Guardando…' : 'Comprobar encaje'}
        </button>
      )}
    </div>
  )
}
