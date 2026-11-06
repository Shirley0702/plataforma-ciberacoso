import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, getErrorMessage } from '../../../shared/api/httpClient'
import { LoadingScreen } from '../../../shared/components/LoadingScreen'
import { useAuth } from '../../auth/context/AuthContext'
import type { DashboardData } from '../../dashboard/types'


export function HomePage() {
  const { user } = useAuth()
  const [dashboard, setDashboard] = useState<DashboardData | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get<DashboardData>('/users/dashboard/')
      .then(({ data }) => setDashboard(data))
      .catch((requestError) => setError(getErrorMessage(requestError)))
  }, [])

  if (!dashboard && !error) return <LoadingScreen label="Preparando tu bienvenida…" />

  const hasDiagnostic = Boolean(dashboard?.diagnostic)

  return (
    <div className="page-wrap home-page">
      <header className="welcome-hero">
        <div className="welcome-copy">
          <span className="eyebrow light">Tu espacio seguro de aprendizaje</span>
          <h1>Hola, {user?.full_name}</h1>
          <p>
            Aquí aprenderás a reconocer situaciones incómodas o difíciles en entornos digitales, protegerte y encontrar rutas claras de apoyo.
            Avanza a tu ritmo; este espacio es privado y orientativo.
          </p>
          <div className="welcome-actions">
            <Link className="btn btn-primary btn-lg" to={hasDiagnostic ? '/panel' : '/evaluacion'}>
              {hasDiagnostic ? 'Continuar con mi ruta' : 'Comenzar mi evaluación'}
            </Link>
            {hasDiagnostic && <Link className="btn btn-outline-light" to="/evaluacion">Repetir evaluación</Link>}
          </div>
        </div>
        <div className="welcome-shield" aria-hidden="true">
          <span>CS</span>
        </div>
      </header>

      {error && <div className="alert alert-danger" role="alert">{error}</div>}

      {!user?.birth_date && (
        <aside className="profile-reminder" aria-label="Perfil pendiente">
          <div>
            <strong>Completa tu información personal</strong>
            <p>Agrega tu fecha de nacimiento para que el sistema calcule tu edad automáticamente.</p>
          </div>
          <Link className="btn btn-outline-primary" to="/mi-cuenta">Completar Perfil</Link>
        </aside>
      )}

      <section className="journey-section" aria-labelledby="journey-title">
        <div className="section-heading">
          <span className="eyebrow">Cómo funciona</span>
          <h2 id="journey-title">Tu recorrido personalizado</h2>
          <p>Primero conocemos tu situación y después organizamos el contenido que más puede ayudarte.</p>
        </div>
        <ol className="journey-grid">
          <li className={hasDiagnostic ? 'completed' : 'current'}>
            <span className="journey-number">01</span>
            <div>
              <h3>Evaluación por Escenarios</h3>
              <p>Responde casos cotidianos. No existen respuestas buenas o malas.</p>
            </div>
          </li>
          <li className={hasDiagnostic ? 'current' : ''}>
            <span className="journey-number">02</span>
            <div>
              <h3>Ruta Personalizada</h3>
              <p>El sistema analiza tus respuestas y recomienda por dónde comenzar.</p>
            </div>
          </li>
          <li>
            <span className="journey-number">03</span>
            <div>
              <h3>Curso y Recursos</h3>
              <p>Aprende con contenidos prácticos y consulta opciones de ayuda verificadas.</p>
            </div>
          </li>
        </ol>
      </section>

      <aside className="home-safety-note">
        <span aria-hidden="true">i</span>
        <p><strong>Recuerda:</strong> la plataforma ofrece orientación educativa. Si existe peligro inmediato en Ecuador, comunícate con el 9-1-1.</p>
      </aside>
    </div>
  )
}
