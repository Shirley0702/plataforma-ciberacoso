import type { InteractionType } from '../types'
import { getCoursePuzzleVisual } from '../config/coursePuzzleVisuals'
import { PuzzleIcon } from './PuzzleIcon'

const PUZZLE_ACTIONS: Record<Exclude<InteractionType, 'video'>, string> = {
  guided: 'Descubre cada pista y arma la idea completa.',
  decision: 'Explora las consecuencias y elige el camino que conserva más opciones.',
  matching: 'Conecta cada señal con el significado que le corresponde.',
  practice: 'Compara las respuestas y construye una forma segura de actuar.',
  safety_plan: 'Ordena las piezas hasta formar una secuencia que puedas recordar.',
}

interface PuzzleMissionProps {
  unitSlug: string
  interactionType: Exclude<InteractionType, 'video'>
  mission: string
}

export function PuzzleMission({ unitSlug, interactionType, mission }: PuzzleMissionProps) {
  const visual = getCoursePuzzleVisual(unitSlug)

  return (
    <section className="puzzle-mission" aria-labelledby="puzzle-mission-title">
      <figure className="puzzle-mission-visual">
        <img src={visual.src} alt={visual.alt} loading="eager" />
        <figcaption>
          <PuzzleIcon name="play" size={18} />
          <span><strong>Vuelve a la idea del video</strong>{visual.videoCue}</span>
        </figcaption>
      </figure>
      <div className="puzzle-mission-copy">
        <span className="puzzle-mission-label">Tu misión</span>
        <h3 id="puzzle-mission-title">{mission}</h3>
        <ol className="puzzle-mission-steps">
          <li><span>1</span><p><strong>Observa</strong>Usa la escena y la idea del video como pistas.</p></li>
          <li><span>2</span><p><strong>Resuelve</strong>{PUZZLE_ACTIONS[interactionType]}</p></li>
          <li><span>3</span><p><strong>Comprueba</strong>Corrige las piezas cuantas veces necesites; no hay penalización.</p></li>
        </ol>
      </div>
    </section>
  )
}
