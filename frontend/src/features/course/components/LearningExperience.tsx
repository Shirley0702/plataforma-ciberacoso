import type { InteractionResponse, InteractionType, LearningItem } from '../types'
import { InteractionPanel } from './interactions/InteractionPanel'

const INTERACTION_LABELS: Record<InteractionType, string> = {
  video: 'Video para aprender',
  guided: 'Puzzle de pistas',
  decision: 'Puzzle de caminos',
  matching: 'Puzzle de conexiones',
  practice: 'Laboratorio de respuestas',
  safety_plan: 'Kit personal de apoyo',
}

interface LearningExperienceProps {
  lesson: LearningItem
  position: number
  total: number
  saving: boolean
  response: InteractionResponse
  feedback?: string
  onResponseChange: (response: InteractionResponse) => void
  onCompletion: (lesson: LearningItem, completed: boolean) => Promise<void>
}

export function LearningExperience({
  lesson,
  position,
  total,
  saving,
  response,
  feedback,
  onResponseChange,
  onCompletion,
}: LearningExperienceProps) {
  return (
    <article className={`learning-experience interaction-${lesson.interaction_type}`}>
      <header className="learning-experience-header">
        <div>
          <span className="experience-kicker">Experiencia {position} de {total}</span>
          <span className="experience-type">{INTERACTION_LABELS[lesson.interaction_type]}</span>
        </div>
        <span className="experience-duration">{lesson.duration_minutes} min</span>
      </header>
      <h2>{lesson.title}</h2>
      {lesson.interaction_type !== 'video' && (
        <section className="learning-concept" aria-labelledby={`concept-${lesson.id}`}>
          <span className="learning-phase">1 · Aprende</span>
          <h3 id={`concept-${lesson.id}`}>Idea clave</h3>
          <p className="experience-summary">{lesson.summary}</p>
          <p className="experience-content">{lesson.content}</p>
        </section>
      )}
      <section className="interactive-activity" aria-label={INTERACTION_LABELS[lesson.interaction_type]}>
        <span className="learning-phase">
          {lesson.interaction_type === 'video' ? 'Observa' : '2 · Descubre practicando'}
        </span>
        {lesson.interaction_type !== 'video' && <h3>{lesson.interaction_prompt}</h3>}
        <InteractionPanel
          lesson={lesson}
          response={response}
          feedback={feedback}
          saving={saving}
          onResponseChange={onResponseChange}
          onCompletion={(completed) => onCompletion(lesson, completed)}
        />
      </section>
    </article>
  )
}
