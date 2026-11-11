import { useEffect } from 'react'
import { tokenStorage } from '../../../shared/api/httpClient'

export function CourseSafetyBanner() {
  const quickExit = () => {
    tokenStorage.clear()
    window.location.replace('https://www.google.com/')
  }

  useEffect(() => {
    const handleQuickExit = (event: KeyboardEvent) => {
      if (event.key === 'Escape') quickExit()
    }
    window.addEventListener('keydown', handleQuickExit)
    return () => window.removeEventListener('keydown', handleQuickExit)
  }, [])

  return (
    <aside className="course-safety-banner" aria-label="Opciones de seguridad y apoyo">
      <span className="privacy-icon" aria-hidden="true">i</span>
      <div>
        <strong>Aprende a tu ritmo y protege tu privacidad.</strong>
        <p>Puedes pausar y volver después. Las actividades no solicitan nombres ni relatos personales.</p>
      </div>
      <button className="quick-exit-button" type="button" onClick={quickExit}>
        × Salir Rápido (Esc)
      </button>
    </aside>
  )
}
