import { useState } from 'react'
import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionOption, InteractionResponse } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

interface DialogueBuilderPuzzleProps {
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

export function DialogueBuilderPuzzle({
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
}: DialogueBuilderPuzzleProps) {
  const [draggedOptionId, setDraggedOptionId] = useState<string | null>(null)
  const selectedOption = options.find((option) => option.id === chosenOptionId)
  const exploredIds = completed ? options.map((option) => option.id) : exploredOptionIds

  const testResponse = (optionId: string) => {
    if (completed || saving) return
    const option = options.find((candidate) => candidate.id === optionId)
    if (!option) return
    const nextExplored = exploredIds.includes(optionId) ? exploredIds : [...exploredIds, optionId]
    onChange(nextExplored, option.id)
    if (nextExplored.length === options.length && option.recommended) {
      void onCompletion(true, { selected_items: nextExplored, chosen_option: option.id })
    }
  }

  return (
    <div className="dialogue-builder-puzzle">
      <header className="puzzle-instruction">
        <span><PuzzleIcon name="chat" size={26} /></span>
        <div><strong>Construye una respuesta que cuide los límites</strong><p>{prompt}</p></div>
      </header>

      <div className="dialogue-workspace">
        <figure className="puzzle-scene dialogue-scene">
          <img src={visual.src} alt={visual.alt} />
          <figcaption><PuzzleIcon name="play" size={16} /> {visual.videoCue}</figcaption>
        </figure>

        <div className="dialogue-builder">
          <div
            className={`dialogue-preview ${selectedOption ? 'filled' : ''}`}
            onDragOver={(event) => event.preventDefault()}
            onDrop={() => {
              if (draggedOptionId) testResponse(draggedOptionId)
              setDraggedOptionId(null)
            }}
          >
            <span className="dialogue-avatar"><PuzzleIcon name="person" size={26} /></span>
            <div>
              <small>Tu respuesta</small>
              <p>{selectedOption?.label ?? 'Arrastra una pieza de diálogo hasta aquí.'}</p>
            </div>
          </div>
          {selectedOption && (
            <div className={`dialogue-result ${selectedOption.recommended ? 'protective' : 'review'}`} role="status">
              <PuzzleIcon name={selectedOption.recommended ? 'shield' : 'review'} size={22} />
              <span><strong>{selectedOption.recommended ? 'Esta respuesta conserva el control' : 'Observa lo que produciría'}</strong>{selectedOption.feedback}</span>
            </div>
          )}

          <div className="dialogue-pieces" role="group" aria-label="Piezas de respuesta">
            {options.map((option, index) => (
              <button
                className={`dialogue-piece ${chosenOptionId === option.id ? 'selected' : ''} ${exploredIds.includes(option.id) ? 'tested' : ''}`}
                type="button"
                draggable={!completed}
                disabled={completed || saving}
                onDragStart={() => setDraggedOptionId(option.id)}
                onDragEnd={() => setDraggedOptionId(null)}
                onClick={() => testResponse(option.id)}
                key={option.id}
              >
                <PuzzleIcon name={['spark', 'boundary', 'reply'][index] ?? 'chat'} size={20} />
                <span>{option.label}</span>
                <small>{exploredIds.includes(option.id) ? 'Probada' : 'Probar'}</small>
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="map-progress" aria-live="polite">
        <span>{exploredIds.length === options.length ? 'Ya comparaste todas. Coloca nuevamente la que protege mejor.' : 'Prueba las tres piezas para comparar su efecto.'}</span>
        <strong>{exploredIds.length}/{options.length}</strong>
      </div>
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed && <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Respuesta construida</p>}
    </div>
  )
}
