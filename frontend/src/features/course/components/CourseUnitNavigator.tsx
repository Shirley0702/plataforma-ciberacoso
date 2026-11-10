import type { CourseUnit } from '../types'

interface CourseUnitNavigatorProps {
  units: CourseUnit[]
  activeIndex: number
  onSelect: (index: number) => void
}

export function CourseUnitNavigator({ units, activeIndex, onSelect }: CourseUnitNavigatorProps) {
  return (
    <nav className="unit-navigator" aria-label="Unidades del curso">
      {units.map((unit, index) => {
        const unlocked = index === 0 || Boolean(units[index - 1]?.certificate)
        const completed = Boolean(unit.certificate)
        const state = completed ? 'Completada' : unlocked ? 'Disponible' : 'Bloqueada'
        return (
          <button
            className={`unit-tab ${activeIndex === index ? 'active' : ''} ${completed ? 'completed' : ''}`}
            type="button"
            disabled={!unlocked}
            aria-current={activeIndex === index ? 'step' : undefined}
            title={unlocked ? unit.title : 'Completa la unidad anterior para continuar'}
            onClick={() => onSelect(index)}
            key={unit.id}
          >
            <span className="unit-tab-marker" aria-hidden="true">{completed ? '✓' : index + 1}</span>
            <span className="unit-tab-copy">
              <small>Unidad {index + 1}</small>
              <strong>{unit.title}</strong>
              <em>{state}</em>
            </span>
          </button>
        )
      })}
    </nav>
  )
}
