import { useMemo, useState } from 'react'
import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import type { InteractionItem } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

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
  const scrambledOrder = useMemo(() => expectedOrder.length > 1 ? [...expectedOrder.slice(1), expectedOrder[0]] : expectedOrder, [expectedOrder])
  const activeOrder = completed ? expectedOrder : hasEveryItem(orderedItemIds, expectedOrder) ? orderedItemIds : scrambledOrder
  const orderedItems = activeOrder.map((itemId) => items.find((item) => item.id === itemId)).filter((item): item is InteractionItem => Boolean(item))
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
      <header className="puzzle-instruction">
        <span><PuzzleIcon name="sequence" size={26} /></span>
        <div><strong>Construye la ruta en el orden correcto</strong><p>{prompt}</p></div>
      </header>
      {privacyNote && <p className="interaction-privacy"><strong>Privacidad:</strong> {privacyNote}</p>}

      <figure className="puzzle-scene sequence-scene">
        <img src={visual.src} alt={visual.alt} />
        <figcaption><PuzzleIcon name="play" size={16} /> Usa la ilustración como pista; {visual.videoCue.toLowerCase()}</figcaption>
      </figure>

      <div className="sequence-track" aria-hidden="true"><span /><span /><span /><span /></div>
      <ol className="sequence-pieces" aria-label="Piezas para ordenar">
        {orderedItems.map((item, index) => (
          <li
            className={`${draggedItemId === item.id ? 'dragging' : ''} ${checked && item.id === expectedOrder[index] ? 'correct-position' : ''}`}
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
            <span className="sequence-position">{index + 1}</span>
            <span className="sequence-icon"><PuzzleIcon name={item.visual} size={32} /></span>
            <span className="sequence-copy"><strong>{item.label}</strong><small>{item.detail}</small></span>
            {!completed && (
              <span className="sequence-controls">
                <button type="button" disabled={index === 0} aria-label={`Mover ${item.label} hacia atrás`} onClick={() => updateOrder(moveItem(activeOrder, item.id, -1))}><PuzzleIcon name="chevron-left" size={19} /></button>
                <button type="button" disabled={index === orderedItems.length - 1} aria-label={`Mover ${item.label} hacia adelante`} onClick={() => updateOrder(moveItem(activeOrder, item.id, 1))}><PuzzleIcon name="chevron-right" size={19} /></button>
              </span>
            )}
          </li>
        ))}
      </ol>

      {checked && !solved && <p className="ordering-feedback" role="alert">{correctPositions} de {items.length} piezas están en su lugar. Revisa qué acción permite realizar la siguiente.</p>}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Ruta completada</p>
      ) : (
        <div className="ordering-actions">
          <button className="btn btn-primary" type="button" disabled={saving} onClick={checkOrder}>{saving ? 'Guardando…' : 'Comprobar ruta'}</button>
          <button className="btn btn-outline-primary" type="button" onClick={() => updateOrder(scrambledOrder)}>Reiniciar</button>
        </div>
      )}
    </div>
  )
}
