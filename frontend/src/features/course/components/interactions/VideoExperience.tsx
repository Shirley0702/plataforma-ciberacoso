import type { InteractionConfig } from '../../types'
import { ChoiceInteraction } from './ChoiceInteraction'

interface VideoExperienceProps {
  lessonId: number
  checkpointPrompt: string
  config: InteractionConfig
  selectedOption?: string
  completed: boolean
  feedback?: string
  saving: boolean
  onSelect: (optionId: string) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function VideoExperience({
  lessonId,
  checkpointPrompt,
  config,
  selectedOption,
  completed,
  feedback,
  saving,
  onSelect,
  onCompletion,
}: VideoExperienceProps) {
  return (
    <div className="video-experience">
      <div className="video-frame">
        <iframe
          src={config.video_url}
          title={config.video_title ?? 'Video educativo'}
          loading="lazy"
          allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerPolicy="strict-origin-when-cross-origin"
          allowFullScreen
        />
      </div>
      <div className="video-meta">
        <p>
          El video no se reproduce automáticamente y utiliza el modo de privacidad mejorada de YouTube.
        </p>
        {config.video_watch_url && (
          <a href={config.video_watch_url} target="_blank" rel="noreferrer">
            Ver en {config.source_label ?? 'la fuente original'}
          </a>
        )}
      </div>
      <details className="video-summary">
        <summary>Leer resumen accesible del video</summary>
        <p>{config.accessible_summary}</p>
        {!!config.key_points?.length && (
          <ul>
            {config.key_points.map((point) => <li key={point}>{point}</li>)}
          </ul>
        )}
      </details>
      <div className="video-checkpoint">
        <h3>{checkpointPrompt}</h3>
        <ChoiceInteraction
          lessonId={lessonId}
          options={config.options ?? []}
          selectedOption={selectedOption}
          completed={completed}
          feedback={feedback}
          saving={saving}
          actionLabel="Comprobar y continuar"
          onSelect={onSelect}
          onCompletion={onCompletion}
        />
      </div>
    </div>
  )
}
