import { describe, expect, it } from 'vitest'
import { getCoursePuzzleVisual } from './coursePuzzleVisuals'

describe('recursos visuales de los puzzles', () => {
  it('asigna una imagen diferente a cada mecánica del curso', () => {
    const sources = [
      getCoursePuzzleVisual('acoso-vertical', 'guided').src,
      getCoursePuzzleVisual('acoso-vertical', 'decision').src,
      getCoursePuzzleVisual('acoso-vertical', 'matching').src,
      getCoursePuzzleVisual('acoso-vertical', 'practice').src,
      getCoursePuzzleVisual('acoso-vertical', 'safety_plan').src,
    ]

    expect(new Set(sources)).toHaveLength(5)
    expect(sources.at(-1)).toContain('/sequence.jpg')
  })
})
