export function LoadingScreen({ label = 'Cargando tu espacio seguro…' }: { label?: string }) {
  return (
    <div className="loading-screen" role="status" aria-live="polite">
      <div className="brand-mark" aria-hidden="true">CS</div>
      <div className="spinner-border text-primary" aria-hidden="true" />
      <p>{label}</p>
    </div>
  )
}
