import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionOption, InteractionResponse } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'
import { PuzzleGuide } from './PuzzleGuide'
import { PuzzleSceneImage } from './PuzzleSceneImage'

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
  const exploredIds = completed ? options.map((option) => option.id) : exploredOptionIds
  const selectedOption = options.find((option) => option.id === chosenOptionId)
  const exploredAll = options.length > 0 && exploredIds.length === options.length

  const testResponse = (option: InteractionOption) => {
    if (completed || saving) return
    const nextExplored = exploredIds.includes(option.id) ? exploredIds : [...exploredIds, option.id]
    onChange(nextExplored, option.id)
  }

  const sendFinalResponse = (option: InteractionOption) => {
    if (completed || saving || !exploredAll) return
    onChange(exploredIds, option.id)
    if (option.recommended) {
      void onCompletion(true, { selected_items: exploredIds, chosen_option: option.id })
    }
  }

  return (
    <div className="dialogue-builder-puzzle">
      <PuzzleGuide
        icon="chat"
        title="Ensaya respuestas dentro de una conversación"
        summary={prompt}
        steps={[
          'Pulsa una respuesta para verla dentro del chat.',
          'Lee el efecto que tendría sin enviar nada real.',
          'Prueba todas y después conserva la que marca un límite sin aumentar el riesgo.',
        ]}
        completion="compares todas las respuestas y envíes la que protege mejor."
      />

      <div className="chat-simulator">
        <div className="chat-scene">
          <PuzzleSceneImage visual={visual} />
          <div><PuzzleIcon name="play" size={16} /><span>Pista del video: {visual.videoCue}</span></div>
        </div>

        <section className="chat-window" aria-label="Simulador de conversación">
          <header>
            <span><PuzzleIcon name="group" size={20} /></span>
            <div><strong>Conversación de práctica</strong><small>No se envía ningún mensaje real</small></div>
          </header>
          <div className="chat-transcript" aria-live="polite">
            <div className="chat-bubble incoming"><small>Situación</small><p>{prompt}</p></div>
            {selectedOption ? (
              <>
                <div className="chat-bubble outgoing"><small>Tu respuesta de prueba</small><p>{selectedOption.label}</p></div>
                <div className={`chat-effect ${selectedOption.recommended ? 'protective' : 'review'}`}>
                  <PuzzleIcon name={selectedOption.recommended ? 'shield' : 'review'} size={21} />
                  <p><strong>Efecto probable</strong>{selectedOption.feedback}</p>
                </div>
              </>
            ) : (
              <div className="chat-empty"><PuzzleIcon name="reply" size={22} /><span>Elige abajo una respuesta para ensayarla.</span></div>
            )}
          </div>
        </section>

        <section className="reply-tray" aria-label="Respuestas para ensayar">
          <div className="reply-tray-heading">
            <strong>{exploredAll ? 'Elige la respuesta final' : 'Respuestas para probar'}</strong>
            <span>{exploredIds.length}/{options.length} comparadas</span>
          </div>
          <div>
            {options.map((option, index) => {
              const tested = exploredIds.includes(option.id)
              return (
                <button
                  className={`${chosenOptionId === option.id ? 'selected' : ''} ${tested ? 'tested' : ''}`}
                  type="button"
                  disabled={completed || saving}
                  aria-label={`${exploredAll ? 'Elegir respuesta final' : 'Probar respuesta'} ${index + 1}: ${option.label}`}
                  onClick={() => exploredAll ? sendFinalResponse(option) : testResponse(option)}
                  key={option.id}
                >
                  <span>{index + 1}</span>
                  <p>{option.label}</p>
                  <small>{exploredAll ? 'Usar esta' : tested ? 'Revisar de nuevo' : 'Probar en el chat'}</small>
                </button>
              )
            })}
          </div>
        </section>
      </div>

      {exploredAll && selectedOption && !selectedOption.recommended && !completed && (
        <p className="consequence-review" role="alert">
          Esa respuesta puede aumentar la presión o reducir el control. Revisa los efectos y elige otra.
        </p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed && <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Respuesta protectora construida</p>}
    </div>
  )
}
