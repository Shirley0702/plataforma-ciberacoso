import type { InteractionResponse, InteractionType, LearningItem } from '../types'
import { InteractionPanel } from './interactions/InteractionPanel'

const INTERACTION_LABELS: Record<InteractionType, string> = {
  video: 'Microvideo y comprobación',
  guided: 'Exploración guiada',
  decision: 'Decisión con consecuencias',
  checklist: 'Lista interactiva',
  practice: 'Práctica segura',
  safety_plan: 'Plan personal seguro',
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
      <p className="experience-summary">{lesson.summary}</p>
      <p className="experience-content">{lesson.content}</p>
      <section className="interactive-activity" aria-label={INTERACTION_LABELS[lesson.interaction_type]}>
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
