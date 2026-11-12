import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { CourseUnit } from '../types'
import { CourseWelcome } from './CourseWelcome'

function unit(id: number, title: string): CourseUnit {
  return {
    id,
    title,
    slug: `ruta-${id}`,
    description: `Descripción de ${title}`,
    order: id,
    priority: id,
    duration_minutes: 30,
    lessons: [],
    quiz_unlocked: false,
    quiz_questions: [],
    latest_quiz: null,
    certificate: null,
  }
}

describe('bienvenida de la ruta personalizada', () => {
  it('explica que la evaluación puede asignar varios módulos y permite comenzar', async () => {
    const user = userEvent.setup()
    const onStart = vi.fn()
    render(
      <CourseWelcome
        units={[unit(1, 'Relaciones de autoridad'), unit(2, 'Seguridad digital')]}
        activeUnitIndex={0}
        onStart={onStart}
      />,
    )

    expect(screen.getByText(/2 módulos asignados/)).toBeVisible()
    expect(screen.getByText(/Avanzarás uno por uno/)).toBeVisible()
    expect(screen.getByRole('list')).toHaveTextContent('Relaciones de autoridad')
    expect(screen.getByRole('list')).toHaveTextContent('Seguridad digital')

    await user.click(screen.getByRole('button', { name: 'Comenzar primera experiencia' }))
    expect(onStart).toHaveBeenCalledOnce()
  })

  it('utiliza singular cuando solo corresponde la ruta preventiva', () => {
    render(
      <CourseWelcome
        units={[unit(5, 'Prevención y convivencia digital')]}
        activeUnitIndex={0}
        onStart={vi.fn()}
      />,
    )

    expect(screen.getByText(/1 módulo asignado/)).toBeVisible()
    expect(screen.getByText(/preparó un módulo/)).toBeVisible()
  })
})
