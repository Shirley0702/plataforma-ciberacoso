import type { InteractionItem } from '../../types'

interface ChecklistInteractionProps {
  items: InteractionItem[]
  selectedItems: string[]
  completed: boolean
  feedback?: string
  privacyNote?: string
  saving: boolean
  actionLabel: string
  onChange: (itemIds: string[]) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function ChecklistInteraction({
  items,
  selectedItems,
  completed,
  feedback,
  privacyNote,
  saving,
  actionLabel,
  onChange,
  onCompletion,
}: ChecklistInteractionProps) {
  const toggleItem = (itemId: string) => {
    const next = selectedItems.includes(itemId)
      ? selectedItems.filter((currentId) => currentId !== itemId)
      : [...selectedItems, itemId]
    onChange(next)
  }
  const selectedAll = items.length > 0 && selectedItems.length === items.length

  return (
    <div className="checklist-interaction">
      {privacyNote && <p className="interaction-privacy"><strong>Privacidad:</strong> {privacyNote}</p>}
      <div className="interactive-checklist">
        {items.map((item) => (
          <label className={selectedItems.includes(item.id) ? 'selected' : ''} key={item.id}>
            <input
              type="checkbox"
              checked={selectedItems.includes(item.id)}
              disabled={completed}
              onChange={() => toggleItem(item.id)}
            />
            <span>
              <strong>{item.label}</strong>
              <small>{item.detail}</small>
            </span>
          </label>
        ))}
      </div>
      {!selectedAll && !completed && (
        <p className="interaction-hint">Revisa y marca cada elemento para continuar.</p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      <button
        className={`btn ${completed ? 'btn-outline-primary' : 'btn-primary'}`}
        type="button"
        disabled={saving || (!completed && !selectedAll)}
        onClick={() => void onCompletion(!completed)}
      >
        {saving ? 'Guardando…' : completed ? 'Marcar como pendiente' : actionLabel}
      </button>
    </div>
  )
}
