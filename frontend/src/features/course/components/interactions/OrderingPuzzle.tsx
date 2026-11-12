import { useMemo, useState } from 'react'
import type { InteractionItem } from '../../types'
import { PuzzleIcon } from '../PuzzleIcon'

interface OrderingPuzzleProps {
  items: InteractionItem[]
  orderedItemIds: string[]
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
  ;[nextOrder[currentIndex], nextOrder[targetIndex]] = [
    nextOrder[targetIndex],
    nextOrder[currentIndex],
  ]
  return nextOrder
}

function swapItems(order: string[], sourceId: string, targetId: string) {
  const sourceIndex = order.indexOf(sourceId)
  const targetIndex = order.indexOf(targetId)
  if (sourceIndex < 0 || targetIndex < 0 || sourceIndex === targetIndex) return order
  const nextOrder = [...order]
  ;[nextOrder[sourceIndex], nextOrder[targetIndex]] = [
    nextOrder[targetIndex],
    nextOrder[sourceIndex],
  ]
  return nextOrder
}

export function OrderingPuzzle({
  items,
  orderedItemIds,
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
    () => expectedOrder.length > 1
      ? [...expectedOrder.slice(1), expectedOrder[0]]
      : expectedOrder,
    [expectedOrder],
  )
  const activeOrder = completed
    ? expectedOrder
    : hasEveryItem(orderedItemIds, expectedOrder)
      ? orderedItemIds
      : scrambledOrder
  const orderedItems = activeOrder
    .map((itemId) => items.find((item) => item.id === itemId))
    .filter((item): item is InteractionItem => Boolean(item))
  const solved = activeOrder.every((itemId, index) => itemId === expectedOrder[index])
  const correctPositions = activeOrder.filter(
    (itemId, index) => itemId === expectedOrder[index],
  ).length

  const updateOrder = (nextOrder: string[]) => {
    setChecked(false)
    onChange(nextOrder)
  }

  const checkOrder = () => {
    setChecked(true)
    if (solved) void onCompletion(true)
  }

  const resetPuzzle = () => {
    setChecked(false)
    onChange(scrambledOrder)
  }

  return (
    <div className="ordering-puzzle">
      {privacyNote && <p className="interaction-privacy"><strong>Privacidad:</strong> {privacyNote}</p>}
      <div className="puzzle-board-heading">
        <span><PuzzleIcon name="puzzle" size={28} /></span>
        <div>
          <strong>Construye la ruta paso a paso</strong>
          <small>Arrastra las tarjetas o usa sus controles para cambiar el orden.</small>
        </div>
      </div>
      <div className="puzzle-progress" aria-live="polite">
        <span>{completed ? 'Secuencia aprendida' : 'Ordena los pasos del primero al último'}</span>
        <strong>{checked ? `${correctPositions}/${items.length} en posición` : `${items.length} tarjetas`}</strong>
      </div>
      <ol className="ordering-board" aria-label="Tarjetas para ordenar">
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
            <span className="ordering-position" aria-label={`Posición ${index + 1}`}>{index + 1}</span>
            <span className="ordering-visual" aria-hidden="true">
              <PuzzleIcon name={item.visual} size={52} />
            </span>
            <span className="ordering-copy">
              <strong>{item.label}</strong>
              <small>{item.detail}</small>
            </span>
            {!completed && (
              <span className="ordering-controls">
                <button type="button" disabled={index === 0} aria-label={`Mover ${item.label} hacia arriba`} onClick={() => updateOrder(moveItem(activeOrder, item.id, -1))}><PuzzleIcon name="chevron-up" size={20} /></button>
                <button type="button" disabled={index === orderedItems.length - 1} aria-label={`Mover ${item.label} hacia abajo`} onClick={() => updateOrder(moveItem(activeOrder, item.id, 1))}><PuzzleIcon name="chevron-down" size={20} /></button>
              </span>
            )}
          </li>
        ))}
      </ol>
      {checked && !solved && (
        <p className="ordering-feedback" role="alert">
          Algunas tarjetas aún están fuera de lugar. Usa las consecuencias de cada paso como pista.
        </p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status"><PuzzleIcon name="check" size={16} /> Secuencia completada</p>
      ) : (
        <div className="ordering-actions">
          <button className="btn btn-primary" type="button" disabled={saving} onClick={checkOrder}>
            {saving ? 'Guardando…' : 'Comprobar secuencia'}
          </button>
          <button className="btn btn-outline-primary" type="button" onClick={resetPuzzle}>
            Reiniciar puzzle
          </button>
        </div>
      )}
    </div>
  )
}
