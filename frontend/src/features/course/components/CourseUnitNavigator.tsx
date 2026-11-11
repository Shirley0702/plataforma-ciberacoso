import type { ReactNode } from 'react'
import type { CourseUnit } from '../types'

interface CourseUnitNavigatorProps {
  units: CourseUnit[]
  activeIndex: number
  activeUnitDetails?: ReactNode
  onSelect: (index: number) => void
}

export function CourseUnitNavigator({
  units,
  activeIndex,
  activeUnitDetails,
  onSelect,
}: CourseUnitNavigatorProps) {
  return (
    <nav className="unit-navigator" aria-label="Unidades del curso">
      {units.map((unit, index) => {
        const unlocked = index === 0 || Boolean(units[index - 1]?.certificate)
        const completed = Boolean(unit.certificate)
        const active = activeIndex === index
        const state = completed ? 'Completada' : unlocked ? 'Disponible' : 'Bloqueada'
        return (
          <div
            className={`unit-route-group ${active ? 'active' : ''}`}
            role="group"
            aria-label={`Unidad ${index + 1}: ${unit.title}`}
            key={unit.id}
          >
            <button
              className={`unit-tab ${active ? 'active' : ''} ${completed ? 'completed' : ''}`}
              type="button"
              disabled={!unlocked}
              aria-current={active ? 'step' : undefined}
              aria-expanded={active}
              title={unlocked ? unit.title : 'Completa la unidad anterior para continuar'}
              onClick={() => onSelect(index)}
            >
              <span className="unit-tab-marker" aria-hidden="true">{completed ? '✓' : index + 1}</span>
              <span className="unit-tab-copy">
                <small>Unidad {index + 1}</small>
                <strong>{unit.title}</strong>
                <em>{state}</em>
              </span>
            </button>
            {active && activeUnitDetails && (
              <div className="unit-route-experiences">
                {activeUnitDetails}
              </div>
            )}
          </div>
        )
      })}
    </nav>
  )
}
