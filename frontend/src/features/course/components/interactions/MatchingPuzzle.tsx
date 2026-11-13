import { useState } from 'react'
import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionItem } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'
import { PuzzleGuide } from './PuzzleGuide'
import { PuzzleSceneImage } from './PuzzleSceneImage'

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
  const selectedClue = items.find((item) => item.id === selectedClueId)
  const connectedCount = Object.keys(visibleMatches).length
  const allConnected = items.length > 0 && items.every((item) => visibleMatches[item.id])
  const solved = allConnected && items.every((item) => visibleMatches[item.id] === item.id)

  const connectMeaning = (meaningId: string) => {
    if (!selectedClueId || completed || saving) return
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
    <div className="matching-puzzle connection-lab-puzzle">
      <PuzzleGuide
        icon="connect"
        title="Conecta cada señal con su significado"
        summary={prompt}
        steps={[
          'Selecciona una señal de la columna izquierda.',
          'Pulsa la explicación que le corresponde a la derecha.',
          'Cuando las conectes todas, comprueba el tablero.',
        ]}
        completion={`formes correctamente las ${items.length} conexiones.`}
      />

      <figure className="connection-reference">
        <PuzzleSceneImage visual={visual} />
        <figcaption><PuzzleIcon name="play" size={16} /> Pista del video: {visual.videoCue}</figcaption>
      </figure>

      <div className="connection-selection" role="status">
        <PuzzleIcon name={selectedClue ? selectedClue.visual || 'clue' : 'target'} size={22} />
        <div>
          <small>{selectedClue ? 'Segundo paso' : connectedCount ? 'Siguiente conexión' : 'Primer paso'}</small>
          <strong>
            {selectedClue
              ? `Ahora elige la explicación de «${selectedClue.label}»`
              : `${connectedCount} de ${items.length} conexiones creadas · Elige una señal de la izquierda`}
          </strong>
        </div>
      </div>

      <div className="connection-board">
        <section className="connection-clues" aria-label="Señales">
          <h4><span>1</span> Señales</h4>
          {items.map((item, index) => {
            const currentMeaning = visibleMatches[item.id]
            const isIncorrect = checked && currentMeaning !== item.id
            const pairNumber = index + 1
            return (
              <button
                className={`${selectedClueId === item.id ? 'selected' : ''} ${currentMeaning ? `connected connection-pair-${pairNumber}` : ''} ${isIncorrect ? 'needs-review' : ''}`}
                type="button"
                aria-pressed={selectedClueId === item.id}
                disabled={completed || saving}
                onClick={() => {
                  setChecked(false)
                  setSelectedClueId(item.id)
                }}
                key={item.id}
              >
                <span><PuzzleIcon name={item.visual || 'clue'} size={23} /></span>
                <div><strong>{item.label}</strong><small>{currentMeaning ? `Pareja ${pairNumber} creada · pulsa para cambiar` : 'Seleccionar señal'}</small></div>
                {currentMeaning && <span className="connection-pair-marker" aria-label={`Pareja ${pairNumber}`}>{pairNumber}</span>}
              </button>
            )
          })}
        </section>

        <section className="connection-meanings" aria-label="Explicaciones">
          <h4><span>2</span> Explicaciones</h4>
          {shuffledMeanings.map((meaning) => {
            const connectedClueId = Object.keys(visibleMatches).find(
              (clueId) => visibleMatches[clueId] === meaning.id,
            )
            const connectedClueIndex = items.findIndex((item) => item.id === connectedClueId)
            const pairNumber = connectedClueIndex + 1
            const isIncorrect = checked && connectedClueId && connectedClueId !== meaning.id
            return (
              <button
                className={`${connectedClueId ? `filled connection-pair-${pairNumber}` : ''} ${isIncorrect ? 'needs-review' : ''}`}
                type="button"
                disabled={completed || saving || !selectedClueId}
                onClick={() => connectMeaning(meaning.id)}
                key={meaning.id}
              >
                {connectedClueId
                  ? <span className="connection-pair-marker" aria-label={`Pareja ${pairNumber}`}>{pairNumber}</span>
                  : <PuzzleIcon name="puzzle" size={20} />}
                <span>{meaning.detail}</span>
              </button>
            )
          })}
        </section>
      </div>

      {checked && !solved && (
        <p className="matching-feedback" role="alert">Cada número muestra las dos tarjetas que uniste. Revisa las parejas destacadas, selecciona otra vez su señal y elige una explicación diferente.</p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Conexiones comprendidas</p>
      ) : (
        <button className="btn btn-primary puzzle-check-button" type="button" disabled={saving || !allConnected} onClick={checkConnections}>
          {saving ? 'Guardando…' : `Comprobar ${items.length} conexiones`}
        </button>
      )}
    </div>
  )
}
