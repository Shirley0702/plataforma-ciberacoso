import { useState } from 'react'
import type { CourseUnit, LearningItem } from '../types'
import { CourseStepNavigator } from './CourseStepNavigator'
import { CourseUnitNavigator } from './CourseUnitNavigator'

interface CourseProgressPanelProps {
  units: CourseUnit[]
  activeUnitIndex: number
  lessons: LearningItem[]
  activeStep: number
  progressPercentage: number
  onSelectUnit: (index: number) => void
  onSelectStep: (index: number) => void
}

export function CourseProgressPanel({
  units,
  activeUnitIndex,
  lessons,
  activeStep,
  progressPercentage,
  onSelectUnit,
  onSelectStep,
}: CourseProgressPanelProps) {
  const [mobileExpanded, setMobileExpanded] = useState(false)
  const activeUnit = units[activeUnitIndex]
  const completedLessons = lessons.filter((lesson) => lesson.completed).length

  return (
    <aside className="course-progress-panel" aria-label="Panel de progreso del curso">
      <header className="course-progress-panel-header">
        <div>
          <span>Tu progreso</span>
          <strong>{progressPercentage}%</strong>
        </div>
        <progress value={progressPercentage} max="100">
          {progressPercentage}%
        </progress>
        <div className="course-progress-panel-summary">
          <small>{completedLessons} de {lessons.length} experiencias en esta unidad</small>
          <button
            type="button"
            aria-expanded={mobileExpanded}
            aria-controls="course-progress-detail"
            onClick={() => setMobileExpanded((current) => !current)}
          >
            {mobileExpanded ? 'Ocultar detalle' : 'Ver detalle'}
          </button>
        </div>
      </header>

      <div id="course-progress-detail" className={`course-progress-panel-body ${mobileExpanded ? 'expanded' : 'collapsed'}`}>
        <section className="course-progress-navigation" aria-labelledby="course-units-heading">
          <h2 id="course-units-heading">Ruta personalizada</h2>
          <CourseUnitNavigator
            units={units}
            activeIndex={activeUnitIndex}
            activeUnitDetails={activeUnit && (
              <CourseStepNavigator
                lessons={lessons}
                activeStep={activeStep}
                quizUnlocked={activeUnit.quiz_unlocked}
                onSelect={onSelectStep}
              />
            )}
            onSelect={onSelectUnit}
          />
        </section>
      </div>
    </aside>
  )
}
