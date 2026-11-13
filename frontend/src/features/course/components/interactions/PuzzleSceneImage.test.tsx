import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { PuzzleSceneImage } from './PuzzleSceneImage'

describe('PuzzleSceneImage', () => {
  it('muestra una sola imagen descriptiva ajustada al cuadro', () => {
    const { container } = render(
      <PuzzleSceneImage
        visual={{
          src: '/assets/course-puzzles/authority/sequence-v2.jpg',
          alt: 'Ruta ilustrada para ordenar acciones.',
          videoCue: 'Pista educativa.',
        }}
      />,
    )

    expect(screen.getByRole('img', { name: 'Ruta ilustrada para ordenar acciones.' }))
      .toHaveClass('puzzle-scene-image-artwork')
    expect(container.querySelectorAll('img')).toHaveLength(1)
    expect(container.querySelector('.puzzle-scene-image-backdrop')).not.toBeInTheDocument()
  })
})
