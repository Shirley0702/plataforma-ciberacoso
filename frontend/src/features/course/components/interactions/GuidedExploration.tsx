import { useState } from 'react'
import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionCard } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'
import { PuzzleGuide } from './PuzzleGuide'
import { PuzzleSceneImage } from './PuzzleSceneImage'

interface GuidedExplorationProps {
  cards: InteractionCard[]
  prompt: string
  visual: CoursePuzzleVisual
  completed: boolean
  feedback?: string
  saving: boolean
  onCompletion: (completed: boolean) => Promise<void>
}

const HOTSPOT_POSITIONS = [
  { left: '18%', top: '24%' },
  { left: '53%', top: '42%' },
  { left: '79%', top: '68%' },
]

export function GuidedExploration({
  cards,
  prompt,
  visual,
  completed,
  feedback,
  saving,
  onCompletion,
}: GuidedExplorationProps) {
  const [discoveredIndexes, setDiscoveredIndexes] = useState<number[]>([])
  const [activeIndex, setActiveIndex] = useState<number | null>(null)
  const visibleIndexes = completed ? cards.map((_, index) => index) : discoveredIndexes

  const discoverSignal = (index: number) => {
    if (completed || saving) return
    setActiveIndex(index)
    if (visibleIndexes.includes(index)) return
    const nextIndexes = [...visibleIndexes, index]
    setDiscoveredIndexes(nextIndexes)
    if (nextIndexes.length === cards.length) void onCompletion(true)
  }

  return (
    <div className="guided-exploration signal-hunt-puzzle">
      <PuzzleGuide
        icon="target"
        title="Encuentra las señales escondidas en la escena"
        summary={prompt}
        steps={[
          'Observa la ilustración completa.',
          'Pulsa cada marcador numerado para descubrir una señal.',
          'Lee la explicación que aparece en tu cuaderno.',
        ]}
        completion={`descubras las ${cards.length} señales de la escena.`}
      />

      <div className="signal-hunt-layout">
        <figure className="signal-hunt-scene">
          <PuzzleSceneImage visual={visual} />
          {cards.map((card, index) => {
            const discovered = visibleIndexes.includes(index)
            const active = activeIndex === index
            return (
              <button
                className={`signal-hotspot ${discovered ? 'discovered' : ''} ${active ? 'active' : ''}`}
                type="button"
                aria-label={`${discovered ? 'Revisar' : 'Descubrir'} señal ${index + 1}: ${card.title}`}
                aria-pressed={active}
                disabled={completed || saving}
                onClick={() => discoverSignal(index)}
                style={HOTSPOT_POSITIONS[index % HOTSPOT_POSITIONS.length]}
                key={card.title}
              >
                {discovered ? <PuzzleIcon name="check" size={19} /> : index + 1}
              </button>
            )
          })}
          <figcaption><PuzzleIcon name="play" size={16} /> Pista del video: {visual.videoCue}</figcaption>
        </figure>

        <aside className="signal-notebook" aria-live="polite">
          <div className="signal-notebook-header">
            <div>
              <span>Cuaderno de hallazgos</span>
              <strong>{visibleIndexes.length} de {cards.length}</strong>
            </div>
            <progress value={visibleIndexes.length} max={Math.max(cards.length, 1)}>
              {visibleIndexes.length} de {cards.length}
            </progress>
          </div>
          <ol>
            {cards.map((card, index) => {
              const discovered = visibleIndexes.includes(index)
              return (
                <li className={discovered ? 'revealed' : ''} key={card.title}>
                  <span>{discovered ? <PuzzleIcon name="clue" size={19} /> : index + 1}</span>
                  <div>
                    <strong>{discovered ? card.title : `Señal ${index + 1} por descubrir`}</strong>
                    <p>{discovered ? card.body : 'Busca el marcador correspondiente en la imagen.'}</p>
                  </div>
                </li>
              )
            })}
          </ol>
        </aside>
      </div>

      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed && (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Señales descubiertas</p>
      )}
    </div>
  )
}
