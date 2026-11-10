import type { InteractionConfig } from '../../types'

interface VideoExperienceProps {
  viewingPrompt: string
  config: InteractionConfig
  watched: boolean
  completed: boolean
  feedback?: string
  saving: boolean
  onWatchedChange: (watched: boolean) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function VideoExperience({
  viewingPrompt,
  config,
  watched,
  completed,
  feedback,
  saving,
  onWatchedChange,
  onCompletion,
}: VideoExperienceProps) {
  const videoWatched = completed || watched

  return (
    <div className="video-experience">
      <div className="video-learning-callout">
        <span aria-hidden="true">▶</span>
        <p>{viewingPrompt}</p>
      </div>
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
      <label className={`video-watch-confirmation ${videoWatched ? 'selected' : ''}`}>
        <input
          type="checkbox"
          checked={videoWatched}
          disabled={completed}
          onChange={(event) => onWatchedChange(event.target.checked)}
        />
        <span>
          <strong>Terminé de ver el video completo</strong>
          <small>Márcalo al finalizar. No hay una pregunta ni una calificación.</small>
        </span>
      </label>
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
      {completed ? (
        <p className="puzzle-completed" role="status">✓ Video completado</p>
      ) : (
        <button
          className="btn btn-primary"
          type="button"
          disabled={saving || !watched}
          onClick={() => void onCompletion(true)}
        >
          {saving ? 'Guardando…' : 'Continuar a los puzzles'}
        </button>
      )}
    </div>
  )
}
