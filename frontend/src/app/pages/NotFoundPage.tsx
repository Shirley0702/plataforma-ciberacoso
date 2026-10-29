import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return <main className="not-found"><span className="brand-mark" aria-hidden="true">CS</span><h1>Página no encontrada</h1><p>La ruta que buscas no existe o cambió.</p><Link className="btn btn-primary" to="/panel">Volver al panel</Link></main>
}
