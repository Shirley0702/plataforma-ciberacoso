import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { PuzzleSceneImage } from './PuzzleSceneImage'

describe('PuzzleSceneImage', () => {
  it('mantiene una imagen descriptiva completa y un fondo únicamente decorativo', () => {
    const { container } = render(
      <PuzzleSceneImage
        visual={{
          src: '/assets/course-puzzles/authority/sequence.jpg',
          alt: 'Ruta ilustrada para ordenar acciones.',
          videoCue: 'Pista educativa.',
        }}
      />,
    )

    expect(screen.getByRole('img', { name: 'Ruta ilustrada para ordenar acciones.' }))
      .toHaveClass('puzzle-scene-image-artwork')
    expect(container.querySelector('.puzzle-scene-image-backdrop'))
      .toHaveAttribute('aria-hidden', 'true')
    expect(container.querySelector('.puzzle-scene-image-backdrop'))
      .toHaveAttribute('alt', '')
  })
})
