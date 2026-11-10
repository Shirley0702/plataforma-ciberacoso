import { useEffect, useMemo, useRef, useState } from 'react'
import type { InteractionConfig, InteractionResponse } from '../../types'
import {
  buildTrackedVideoUrl,
  loadYouTubePlayerApi,
  type YouTubePlayerInstance,
  YOUTUBE_VIDEO_ENDED,
} from '../../services/youtubePlayer'

interface VideoExperienceProps {
  viewingPrompt: string
  config: InteractionConfig
  completed: boolean
  feedback?: string
  saving: boolean
  onCompletion: (
    completed: boolean,
    responseOverride?: InteractionResponse,
    advance?: boolean,
  ) => Promise<void>
}

export function VideoExperience({
  viewingPrompt,
  config,
  completed,
  feedback,
  saving,
  onCompletion,
}: VideoExperienceProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const completionRequested = useRef(false)
  const completionHandler = useRef(onCompletion)
  const [trackingError, setTrackingError] = useState('')
  const trackedVideoUrl = useMemo(
    () => buildTrackedVideoUrl(config.video_url ?? ''),
    [config.video_url],
  )

  useEffect(() => {
    completionHandler.current = onCompletion
  }, [onCompletion])

  useEffect(() => {
    if (completed || !iframeRef.current) return
    let disposed = false
    let player: YouTubePlayerInstance | null = null

    void loadYouTubePlayerApi()
      .then((youtube) => {
        if (disposed || !iframeRef.current) return
        player = new youtube.Player(iframeRef.current, {
          events: {
            onStateChange: (event) => {
              if (event.data !== YOUTUBE_VIDEO_ENDED || completionRequested.current) return
              completionRequested.current = true
              void completionHandler.current(true, { watched: true }, false)
                .finally(() => {
                  completionRequested.current = false
                })
            },
          },
        })
      })
      .catch(() => {
        if (!disposed) {
          setTrackingError('No se pudo activar el seguimiento automático. Recarga la página antes de continuar.')
        }
      })

    return () => {
      disposed = true
      player?.destroy()
    }
  }, [completed, trackedVideoUrl])

  return (
    <div className="video-experience">
      <div className="video-learning-callout">
        <span aria-hidden="true">▶</span>
        <p>{viewingPrompt}</p>
      </div>
      <div className="video-frame">
        <iframe
          ref={iframeRef}
          src={trackedVideoUrl}
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
      <div className={`video-completion-status ${completed ? 'completed' : ''}`} role="status">
        <span aria-hidden="true">{completed ? '✓' : '○'}</span>
        <div>
          <strong>{completed ? 'Hecho: video visto hasta el final' : 'Por hacer: mira el video hasta el final'}</strong>
          <small>
            {saving
              ? 'Registrando tu avance…'
              : 'Se marcará automáticamente al terminar; no necesitas pulsar ningún botón.'}
          </small>
        </div>
      </div>
      {trackingError && <p className="video-tracking-error" role="alert">{trackingError}</p>}
      {feedback && <div className="activity-feedback" role="status">{feedback}</div>}
    </div>
  )
}
