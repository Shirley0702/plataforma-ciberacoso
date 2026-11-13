import { useMemo, useState } from 'react'
import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionItem } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'
import { PuzzleGuide } from './PuzzleGuide'

interface OrderingPuzzleProps {
  items: InteractionItem[]
  orderedItemIds: string[]
  prompt: string
  visual: CoursePuzzleVisual
  completed: boolean
  feedback?: string
  privacyNote?: string
  saving: boolean
  onChange: (itemIds: string[]) => void
  onCompletion: (completed: boolean) => Promise<void>
}

function hasEveryItem(order: string[], expectedIds: string[]) {
  return order.length === expectedIds.length
    && new Set(order).size === expectedIds.length
    && expectedIds.every((itemId) => order.includes(itemId))
}

function moveItem(order: string[], itemId: string, offset: number) {
  const currentIndex = order.indexOf(itemId)
  const targetIndex = currentIndex + offset
  if (currentIndex < 0 || targetIndex < 0 || targetIndex >= order.length) return order
  const nextOrder = [...order]
  ;[nextOrder[currentIndex], nextOrder[targetIndex]] = [nextOrder[targetIndex], nextOrder[currentIndex]]
  return nextOrder
}

function swapItems(order: string[], sourceId: string, targetId: string) {
  const sourceIndex = order.indexOf(sourceId)
  const targetIndex = order.indexOf(targetId)
  if (sourceIndex < 0 || targetIndex < 0 || sourceIndex === targetIndex) return order
  const nextOrder = [...order]
  ;[nextOrder[sourceIndex], nextOrder[targetIndex]] = [nextOrder[targetIndex], nextOrder[sourceIndex]]
  return nextOrder
}

export function OrderingPuzzle({
  items,
  orderedItemIds,
  prompt,
  visual,
  completed,
  feedback,
  privacyNote,
  saving,
  onChange,
  onCompletion,
}: OrderingPuzzleProps) {
  const [draggedItemId, setDraggedItemId] = useState<string | null>(null)
  const [checked, setChecked] = useState(false)
  const expectedOrder = useMemo(() => items.map((item) => item.id), [items])
  const scrambledOrder = useMemo(
    () => expectedOrder.length > 1 ? [...expectedOrder.slice(1), expectedOrder[0]] : expectedOrder,
    [expectedOrder],
  )
  const activeOrder = completed
    ? expectedOrder
    : hasEveryItem(orderedItemIds, expectedOrder) ? orderedItemIds : scrambledOrder
  const orderedItems = activeOrder
    .map((itemId) => items.find((item) => item.id === itemId))
    .filter((item): item is InteractionItem => Boolean(item))
  const solved = activeOrder.every((itemId, index) => itemId === expectedOrder[index])
  const correctPositions = activeOrder.filter((itemId, index) => itemId === expectedOrder[index]).length

  const updateOrder = (nextOrder: string[]) => {
    setChecked(false)
    onChange(nextOrder)
  }

  const checkOrder = () => {
    setChecked(true)
    if (solved) void onCompletion(true)
  }

  return (
    <div className="ordering-puzzle route-ordering-puzzle">
      <PuzzleGuide
        icon="sequence"
        title="Ordena una ruta que pueda aplicarse paso a paso"
        summary={prompt}
        steps={[
          'Lee las cuatro acciones antes de moverlas.',
          'Arrastra las piezas o usa sus flechas para cambiar el orden.',
          'Comprueba la ruta; el tablero indicará cuántas posiciones están correctas.',
        ]}
        completion="todas las acciones queden en una secuencia que se pueda seguir."
      />
      {privacyNote && <p className="interaction-privacy"><strong>Cuida tu privacidad:</strong> {privacyNote}</p>}

      <figure className="sequence-reference">
        <img src={visual.src} alt={visual.alt} />
        <figcaption><PuzzleIcon name="play" size={16} /> Pista del video: {visual.videoCue}</figcaption>
      </figure>

      <div className="sequence-status" aria-live="polite">
        <div><span>Ruta actual</span><strong>De la primera acción a la última</strong></div>
        {checked && <p>{correctPositions} de {items.length} posiciones correctas</p>}
      </div>

      <ol className="sequence-pieces" aria-label="Acciones ordenables">
        {orderedItems.map((item, index) => {
          const isCorrect = checked && item.id === expectedOrder[index]
          return (
            <li
              className={`${draggedItemId === item.id ? 'dragging' : ''} ${isCorrect ? 'correct-position' : ''} ${checked && !isCorrect ? 'needs-review' : ''}`}
              draggable={!completed}
              onDragStart={() => setDraggedItemId(item.id)}
              onDragEnd={() => setDraggedItemId(null)}
              onDragOver={(event) => event.preventDefault()}
              onDrop={() => {
                if (draggedItemId) updateOrder(swapItems(activeOrder, draggedItemId, item.id))
                setDraggedItemId(null)
              }}
              key={item.id}
            >
              <div className="sequence-piece-top">
                <span className="sequence-position">Paso {index + 1}</span>
                {checked && <span className="sequence-verdict">{isCorrect ? 'En su lugar' : 'Revisar posición'}</span>}
              </div>
              <span className="sequence-icon"><PuzzleIcon name={item.visual} size={31} /></span>
              <span className="sequence-copy"><strong>{item.label}</strong><small>{item.detail}</small></span>
              {!completed && (
                <span className="sequence-controls">
                  <button type="button" disabled={index === 0} aria-label={`Mover ${item.label} un lugar hacia el inicio`} onClick={() => updateOrder(moveItem(activeOrder, item.id, -1))}><PuzzleIcon name="chevron-left" size={19} /> Antes</button>
                  <button type="button" disabled={index === orderedItems.length - 1} aria-label={`Mover ${item.label} un lugar hacia el final`} onClick={() => updateOrder(moveItem(activeOrder, item.id, 1))}>Después <PuzzleIcon name="chevron-right" size={19} /></button>
                </span>
              )}
            </li>
          )
        })}
      </ol>

      {checked && !solved && <p className="ordering-feedback" role="alert">La ruta todavía no puede seguirse de principio a fin. Revisa las piezas marcadas y piensa qué acción prepara la siguiente.</p>}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Ruta construida correctamente</p>
      ) : (
        <div className="ordering-actions">
          <button className="btn btn-primary" type="button" disabled={saving} onClick={checkOrder}>{saving ? 'Guardando…' : 'Comprobar la ruta'}</button>
          <button className="btn btn-outline-primary" type="button" onClick={() => updateOrder(scrambledOrder)}>Volver a empezar</button>
        </div>
      )}
    </div>
  )
}
