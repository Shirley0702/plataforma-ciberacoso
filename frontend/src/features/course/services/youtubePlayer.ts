export const YOUTUBE_VIDEO_ENDED = 0

interface YouTubeStateChangeEvent {
  data: number
}

export interface YouTubePlayerInstance {
  destroy: () => void
}

interface YouTubePlayerOptions {
  events: {
    onStateChange: (event: YouTubeStateChangeEvent) => void
  }
}

interface YouTubePlayerApi {
  Player: new (
    element: HTMLIFrameElement,
    options: YouTubePlayerOptions,
  ) => YouTubePlayerInstance
}

declare global {
  interface Window {
    YT?: YouTubePlayerApi
    onYouTubeIframeAPIReady?: () => void
  }
}

let apiPromise: Promise<YouTubePlayerApi> | null = null

export function buildTrackedVideoUrl(videoUrl: string) {
  if (!videoUrl) return ''
  const url = new URL(videoUrl)
  url.searchParams.set('enablejsapi', '1')
  url.searchParams.set('playsinline', '1')
  if (window.location.origin.startsWith('http')) {
    url.searchParams.set('origin', window.location.origin)
  }
  return url.toString()
}

export function loadYouTubePlayerApi(): Promise<YouTubePlayerApi> {
  if (window.YT?.Player) return Promise.resolve(window.YT)
  if (apiPromise) return apiPromise

  apiPromise = new Promise((resolve, reject) => {
    const previousReadyHandler = window.onYouTubeIframeAPIReady
    window.onYouTubeIframeAPIReady = () => {
      previousReadyHandler?.()
      if (window.YT?.Player) resolve(window.YT)
    }

    const existingScript = document.getElementById('youtube-iframe-api')
    if (existingScript) return

    const script = document.createElement('script')
    script.id = 'youtube-iframe-api'
    script.src = 'https://www.youtube.com/iframe_api'
    script.async = true
    script.addEventListener(
      'error',
      () => {
        apiPromise = null
        reject(new Error('No se pudo cargar la API del reproductor de YouTube.'))
      },
      { once: true },
    )
    document.head.appendChild(script)
  })

  return apiPromise
}
