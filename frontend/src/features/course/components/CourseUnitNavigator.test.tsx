import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { CourseUnit } from '../types'
import { CourseUnitNavigator } from './CourseUnitNavigator'

function unit(id: number, certificate: CourseUnit['certificate'] = null): CourseUnit {
  return {
    id,
    title: `Tema ${id}`,
    slug: `tema-${id}`,
    description: 'Descripción',
    order: id,
    priority: id,
    duration_minutes: 30,
    lessons: [],
    quiz_unlocked: false,
    quiz_questions: [],
    latest_quiz: null,
    certificate,
  }
}

describe('navegación secuencial de unidades', () => {
  it('mantiene bloqueada la siguiente unidad hasta certificar la anterior', async () => {
    const user = userEvent.setup()
    const onSelect = vi.fn()
    const { rerender } = render(
      <CourseUnitNavigator units={[unit(1), unit(2)]} activeIndex={0} onSelect={onSelect} />,
    )

    expect(screen.getByRole('button', { name: /Unidad 2.*Bloqueada/ })).toBeDisabled()
    rerender(
      <CourseUnitNavigator
        units={[unit(1, { verification_code: 'ABC', download_url: '/certificado' }), unit(2)]}
        activeIndex={0}
        onSelect={onSelect}
      />,
    )
    await user.click(screen.getByRole('button', { name: /Unidad 2.*Disponible/ }))
    expect(onSelect).toHaveBeenCalledWith(1)
  })
})
