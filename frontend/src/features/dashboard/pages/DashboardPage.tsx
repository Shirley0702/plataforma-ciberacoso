import { useEffect, useState } from 'react'
import { Link, Navigate } from 'react-router-dom'
import { api, getErrorMessage } from '../../../shared/api/httpClient'
import { LoadingScreen } from '../../../shared/components/LoadingScreen'
import type { DashboardData } from '../types'

const dateFormatter = new Intl.DateTimeFormat('es-EC', { dateStyle: 'medium' })

export function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get<DashboardData>('/users/dashboard/')
      .then((response) => setData(response.data))
      .catch((requestError) => setError(getErrorMessage(requestError)))
  }, [])

  if (!data && !error) return <LoadingScreen label="Preparando tu panel…" />
  if (data && !data.diagnostic) return <Navigate to="/inicio" replace />
  const mainPriorities = data?.diagnostic?.recommended_units.filter(
    (unit) => unit.priority === 1,
  ) ?? []

  return (
    <div className="page-wrap">
      <header className="page-header dashboard-header">
        <div>
          <span className="eyebrow">Tu recorrido</span>
          <h1>Hola, {data?.user.full_name}</h1>
          <p>Hoy puedes avanzar con una acción pequeña y concreta.</p>
        </div>
        <Link className="btn btn-outline-primary" to="/evaluacion">Repetir evaluación</Link>
      </header>

      {error && <div className="alert alert-danger" role="alert">{error}</div>}

      {data && (
        <>
          <section className="hero-card" aria-labelledby="next-step-title">
            <div className="hero-copy">
              <span className="status-pill">Siguiente paso recomendado</span>
              <h2 id="next-step-title">
                {data.diagnostic?.route_type === 'preventive_general'
                  ? 'Tu ruta preventiva está lista'
                  : mainPriorities.length > 1
                    ? `Prioridades principales: ${mainPriorities.map((unit) => unit.title).join(' y ')}`
                    : `Primera prioridad: ${data.diagnostic?.suggested_unit.title}`}
              </h2>
              <p>
                {data.diagnostic?.route_type === 'preventive_general'
                  ? 'La evaluación asignó un módulo preventivo general de convivencia, límites y autocuidado.'
                  : `La evaluación asignó ${data.diagnostic?.recommended_units.length} ${data.diagnostic?.recommended_units.length === 1 ? 'módulo priorizado' : 'módulos priorizados'}. Los completarás uno por uno, comenzando por la prioridad principal.`}
              </p>
              <Link className="btn btn-primary" to="/curso">Ver mi ruta y comenzar</Link>
            </div>
            <div className="hero-orbit" aria-hidden="true">
              <div className="orbit orbit-one" />
              <div className="orbit orbit-two" />
              <span>{data.course.percentage}%</span>
              <small>curso</small>
            </div>
          </section>

          <section className="metric-grid" aria-label="Resumen de actividad">
            <article className="metric-card">
              <div className="metric-label"><span className="metric-icon accent">✓</span> Módulos asignados a tu ruta</div>
              <ol className="dashboard-route-list">
                {data.diagnostic?.recommended_units.map((unit, index) => (
                  <li key={`${unit.title}-${index}`}>
                    <span>{index + 1}</span>
                    <strong>{unit.title}</strong>
                  </li>
                ))}
              </ol>
              <p>Este es el orden de aprendizaje; al completar un módulo se habilita el siguiente.</p>
              <p>Evaluación procesada el {data.diagnostic && dateFormatter.format(new Date(data.diagnostic.created_at))}.</p>
              <Link to="/evaluacion">Volver a realizar el test <span aria-hidden="true">→</span></Link>
            </article>
            <article className="metric-card">
              <div className="metric-label"><span className="metric-icon primary">▤</span> Curso</div>
              <strong>{data.course.percentage}% completado</strong>
              <div className="progress" role="progressbar" aria-label="Progreso del curso" aria-valuenow={data.course.percentage} aria-valuemin={0} aria-valuemax={100}>
                <div className="progress-bar" style={{ width: `${data.course.percentage}%` }} />
              </div>
              <p>{data.course.completed} de {data.course.total} lecciones completadas.</p>
              <Link to="/curso">Ir al curso <span aria-hidden="true">→</span></Link>
            </article>
            <article className="metric-card">
              <div className="metric-label"><span className="metric-icon accent">◫</span> Orientación Privada</div>
              <strong>{data.text_review ? 'Orientación disponible' : 'Explora una situación'}</strong>
              <p>
                {data.text_review
                  ? 'Puedes volver a revisar una situación sin guardar el texto original.'
                  : 'Describe una situación y recibe pasos personalizados junto con tu ruta.'}
              </p>
              <Link to="/orientacion-privada">Recibir orientación <span aria-hidden="true">→</span></Link>
            </article>
          </section>

          <section className="help-card">
            <span className="eyebrow light">¿Necesitas ayuda ahora?</span>
            <h2>No tienes que resolverlo a solas.</h2>
            <p>Revisa recursos oficiales o habla con una persona de confianza. Ante peligro inmediato en Ecuador, llama al 9-1-1.</p>
            <Link className="btn btn-outline-light" to="/recursos">Ver recursos</Link>
          </section>
        </>
      )}
    </div>
  )
}
