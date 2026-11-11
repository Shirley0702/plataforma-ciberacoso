import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { CourseUnit, LearningItem } from '../types'
import { CourseProgressPanel } from './CourseProgressPanel'

const lesson: LearningItem = {
  id: 1,
  title: 'Reconocer una señal',
  summary: 'Resumen',
  content: 'Contenido',
  interaction_type: 'guided',
  duration_minutes: 5,
  interaction_prompt: 'Descubre las pistas',
  interaction_config: { cards: [] },
  interaction_response: {},
  completed: true,
}

const unit: CourseUnit = {
  id: 1,
  title: 'Bienestar digital',
  slug: 'acoso-tecnologico',
  description: 'Descripción',
  order: 1,
  priority: 1,
  duration_minutes: 30,
  lessons: [lesson],
  quiz_unlocked: true,
  quiz_questions: [],
  latest_quiz: null,
  certificate: null,
}

describe('panel lateral de progreso', () => {
  it('mantiene visibles el avance, las unidades y cada experiencia', () => {
    render(
      <CourseProgressPanel
        units={[unit]}
        activeUnitIndex={0}
        lessons={[lesson]}
        activeStep={0}
        progressPercentage={42}
        onSelectUnit={vi.fn()}
        onSelectStep={vi.fn()}
      />,
    )

    expect(screen.getByRole('complementary', { name: 'Panel de progreso del curso' })).toBeVisible()
    expect(screen.getByRole('progressbar')).toHaveValue(42)
    const unitButton = screen.getByRole('button', { name: /Unidad 1.*Bienestar digital.*Disponible/ })
    const experienceButton = screen.getByRole('button', { name: /Experiencia 1 Reconocer una señal.*completada/ })
    expect(unitButton).toBeVisible()
    expect(experienceButton).toBeVisible()
    expect(unitButton.compareDocumentPosition(experienceButton) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
    expect(screen.queryByText('Avance de la unidad')).not.toBeInTheDocument()
  })
})
