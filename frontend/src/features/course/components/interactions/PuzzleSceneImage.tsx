import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'

interface PuzzleSceneImageProps {
  visual: CoursePuzzleVisual
}

export function PuzzleSceneImage({ visual }: PuzzleSceneImageProps) {
  return (
    <span className="puzzle-scene-image">
      <img
        className="puzzle-scene-image-artwork"
        src={visual.src}
        alt={visual.alt}
      />
    </span>
  )
}
