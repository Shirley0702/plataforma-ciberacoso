import { useEffect, useState } from 'react'
import { api, getErrorMessage } from '../../../shared/api/httpClient'
import type { OrientationResource } from '../types'

export function ResourcesPage() {
  const [resources, setResources] = useState<OrientationResource[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    api.get<OrientationResource[]>('/resources/')
      .then(({ data }) => setResources(data))
      .catch((requestError) => setError(getErrorMessage(requestError)))
  }, [])

  return (
    <div className="page-wrap">
      <header className="page-header"><div><span className="eyebrow">Orientación verificada</span><h1>Recursos y rutas de ayuda</h1><p>Opciones oficiales para actuar con apoyo y según el nivel de urgencia.</p></div></header>
      {error && <div className="alert alert-danger" role="alert">{error}</div>}

      <section className="emergency-banner" aria-labelledby="emergency-title">
        <div className="emergency-number"><span>Emergencias</span><strong>9-1-1</strong></div>
        <div><h2 id="emergency-title">Si existe peligro inmediato, actúa ahora.</h2><p>En Ecuador, llama al ECU 911 desde un teléfono fijo o móvil. Busca un lugar seguro y avisa a una persona de confianza.</p></div>
        <a className="btn btn-light" href="tel:911">Llamar al 9-1-1</a>
      </section>

      <section className="safety-route" aria-labelledby="route-title">
        <div className="section-heading"><div><span className="eyebrow">Ruta breve</span><h2 id="route-title">Qué puedes hacer</h2></div></div>
        <ol className="route-steps">
          <li><span>1</span><div><strong>Prioriza tu seguridad</strong><p>Aléjate del riesgo y evita confrontar si una amenaza puede escalar.</p></div></li>
          <li><span>2</span><div><strong>Conserva evidencia</strong><p>Guarda capturas completas, enlaces, fechas y nombres de usuario.</p></div></li>
          <li><span>3</span><div><strong>Busca acompañamiento</strong><p>Cuéntalo a una persona adulta, docente, DECE, orientador o autoridad.</p></div></li>
          <li><span>4</span><div><strong>Reporta por el canal adecuado</strong><p>Usa la plataforma digital y, cuando corresponda, una institución oficial.</p></div></li>
        </ol>
      </section>

      <section aria-labelledby="official-title">
        <div className="section-heading"><div><span className="eyebrow">Directorio</span><h2 id="official-title">Recursos oficiales</h2></div></div>
        <div className="resource-grid">
          {resources.map((resource) => (
            <article className={`resource-card ${resource.emergency ? 'emergency' : ''}`} key={resource.id}>
              <div className="resource-card-top"><span className="resource-symbol" aria-hidden="true">{resource.emergency ? '!' : '+'}</span><span>{resource.country}</span></div>
              <h3>{resource.name}</h3><p>{resource.description}</p>
              {resource.phone && <a className="resource-phone" href={`tel:${resource.phone.replace(/[^0-9]/g, '')}`}>{resource.phone}</a>}
              {resource.url && <a className="resource-link" href={resource.url} target="_blank" rel="noreferrer">Abrir sitio oficial <span aria-hidden="true">↗</span></a>}
            </article>
          ))}
        </div>
      </section>

      <div className="resource-disclaimer"><strong>Importante</strong><p>CiberSegura brinda educación y orientación inicial. No investiga delitos, no reemplaza atención psicológica y no envía denuncias automáticamente.</p></div>
    </div>
  )
}
