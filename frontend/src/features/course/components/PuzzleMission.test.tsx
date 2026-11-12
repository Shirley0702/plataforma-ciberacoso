import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { PuzzleMission } from './PuzzleMission'

describe('misión visual del puzzle', () => {
  it('conecta la experiencia con el video y la ilustración de su ruta', () => {
    render(
      <PuzzleMission
        unitSlug="acoso-tecnologico"
        interactionType="matching"
        mission="Conecta cada señal con su significado."
      />,
    )

    expect(screen.getByRole('img')).toHaveAttribute(
      'src',
      '/assets/course-puzzles/digital-safety.jpg',
    )
    expect(screen.getByText(/Recuerda la idea central del video/)).toBeVisible()
    expect(screen.getByRole('heading', { name: /Conecta cada señal/ })).toBeVisible()
    expect(screen.getByText(/no hay penalización/)).toBeVisible()
  })
})
