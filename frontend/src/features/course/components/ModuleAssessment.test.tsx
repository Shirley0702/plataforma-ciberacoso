import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'

import type { CourseUnit } from '../types'
import { ModuleAssessment } from './ModuleAssessment'


const completedUnit: CourseUnit = {
  id: 1,
  title: 'Ruta personalizada',
  description: 'Ruta de prueba',
  duration_minutes: 20,
  lessons: [],
  quiz_unlocked: true,
  quiz_questions: [],
  latest_quiz: { score_percentage: 100, passed: true },
  certificate: {
    verification_code: 'CERT-001',
    download_url: '/courses/certificates/CERT-001/download/',
  },
}

function renderAssessment(unit: CourseUnit) {
  render(
    <MemoryRouter>
      <ModuleAssessment
        unit={unit}
        answers={{}}
        setAnswers={vi.fn()}
        result={null}
        submitting={false}
        onSubmit={vi.fn()}
        onDownload={vi.fn()}
      />
    </MemoryRouter>,
  )
}

describe('ModuleAssessment', () => {
  it('ofrece evaluar la plataforma después de certificar el curso', () => {
    renderAssessment(completedUnit)

    expect(screen.getByRole('link', { name: 'Evaluar la plataforma' }))
      .toHaveAttribute('href', '/evaluar-plataforma')
  })

  it('oculta la evaluación mientras el curso no está certificado', () => {
    renderAssessment({ ...completedUnit, certificate: null })

    expect(screen.queryByRole('link', { name: 'Evaluar la plataforma' }))
      .not.toBeInTheDocument()
  })
})
