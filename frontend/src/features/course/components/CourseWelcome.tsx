import type { CourseUnit } from '../types'
import { PuzzleIcon } from './PuzzleIcon'

interface CourseWelcomeProps {
  units: CourseUnit[]
  activeUnitIndex: number
  onStart: () => void
}

const LEARNING_STEPS = [
  { icon: 'observe', title: 'Observa', description: 'Empieza con una explicación breve y clara.' },
  { icon: 'clue', title: 'Descubre', description: 'Reconoce señales mediante puzzles interactivos.' },
  { icon: 'route', title: 'Practica', description: 'Ensaya decisiones seguras sin exponer experiencias personales.' },
]

export function CourseWelcome({ units, activeUnitIndex, onStart }: CourseWelcomeProps) {
  const activeUnit = units[activeUnitIndex]
  if (!activeUnit) return null

  const moduleLabel = units.length === 1 ? '1 módulo asignado' : `${units.length} módulos asignados`
  const routeExplanation = units.length === 1
    ? 'La evaluación preparó un módulo para comenzar tu recorrido. Encontrarás explicaciones, videos y actividades prácticas.'
    : `La evaluación organizó ${units.length} módulos según tus respuestas. Avanzarás uno por uno y cada módulo se desbloqueará al completar el anterior.`

  return (
    <section className="course-welcome" aria-labelledby="course-welcome-title">
      <header className="course-welcome-intro">
        <div>
          <span className="course-welcome-badge">Tu ruta personalizada · {moduleLabel}</span>
          <h2 id="course-welcome-title">Bienvenida a tu recorrido de aprendizaje</h2>
          <p>{routeExplanation}</p>
        </div>
        <div className="course-welcome-symbol" aria-hidden="true">
          <PuzzleIcon name="compass" size={42} />
          <span>{activeUnitIndex + 1}/{units.length}</span>
        </div>
      </header>

      <div className="course-welcome-overview">
        <article className="course-welcome-current">
          <span>{activeUnitIndex === 0 ? 'Comenzarás por' : 'Continuarás con'}</span>
          <h3>{activeUnit.title}</h3>
          <p>{activeUnit.description}</p>
          <div>
            <small>{activeUnit.lessons.length} experiencias</small>
            <small>{activeUnit.duration_minutes} min aproximados</small>
          </div>
        </article>

        <div className="course-welcome-route" aria-labelledby="assigned-route-title">
          <h3 id="assigned-route-title">Módulos de tu ruta</h3>
          <ol>
            {units.map((unit, index) => {
              const completed = Boolean(unit.certificate)
              const state = completed ? 'Completado' : index === activeUnitIndex ? 'Ahora' : 'Después'
              return (
                <li className={index === activeUnitIndex ? 'active' : ''} key={unit.id}>
                  <span aria-hidden="true">{completed ? '✓' : index + 1}</span>
                  <div>
                    <strong>{unit.title}</strong>
                    <small>{state}</small>
                  </div>
                </li>
              )
            })}
          </ol>
        </div>
      </div>

      <div className="course-welcome-method" aria-label="Cómo aprenderás">
        {LEARNING_STEPS.map((step) => (
          <article key={step.title}>
            <PuzzleIcon name={step.icon} size={25} />
            <div>
              <strong>{step.title}</strong>
              <small>{step.description}</small>
            </div>
          </article>
        ))}
      </div>

      <footer className="course-welcome-actions">
        <p>Tu avance se guarda automáticamente. Puedes pausar y volver cuando lo necesites.</p>
        <button className="btn btn-primary" type="button" onClick={onStart}>
          Comenzar primera experiencia
        </button>
      </footer>
    </section>
  )
}
