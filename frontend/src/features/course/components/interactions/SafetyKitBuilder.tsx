import type { InteractionItem } from '../../types'

interface SafetyKitBuilderProps {
  items: InteractionItem[]
  selectedItems: string[]
  completed: boolean
  feedback?: string
  privacyNote?: string
  saving: boolean
  onChange: (itemIds: string[]) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function SafetyKitBuilder({
  items,
  selectedItems,
  completed,
  feedback,
  privacyNote,
  saving,
  onChange,
  onCompletion,
}: SafetyKitBuilderProps) {
  const visibleItems = completed ? items.map((item) => item.id) : selectedItems
  const toggleItem = (itemId: string) => {
    const next = visibleItems.includes(itemId)
      ? visibleItems.filter((currentId) => currentId !== itemId)
      : [...visibleItems, itemId]
    onChange(next)
  }
  const kitReady = items.length > 0 && visibleItems.length === items.length

  return (
    <div className="safety-kit-builder">
      {privacyNote && <p className="interaction-privacy"><strong>Privacidad:</strong> {privacyNote}</p>}
      <div className="safety-kit-grid">
        {items.map((item) => (
          <label className={visibleItems.includes(item.id) ? 'selected' : ''} key={item.id}>
            <input
              type="checkbox"
              checked={visibleItems.includes(item.id)}
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
      {!kitReady && !completed && (
        <p className="interaction-hint">Añade cada recurso para construir tu kit de apoyo.</p>
      )}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status">✓ Kit personal preparado</p>
      ) : (
        <button
          className="btn btn-primary"
          type="button"
          disabled={saving || !kitReady}
          onClick={() => void onCompletion(true)}
        >
          {saving ? 'Guardando…' : 'Guardar mi kit'}
        </button>
      )}
    </div>
  )
}
