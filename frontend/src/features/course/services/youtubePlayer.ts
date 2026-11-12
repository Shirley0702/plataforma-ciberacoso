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
const API_SCRIPT_ID = 'youtube-iframe-api'
const API_LOAD_TIMEOUT_MS = 12_000

function availableApi() {
  return window.YT?.Player ? window.YT : null
}

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
  const loadedApi = availableApi()
  if (loadedApi) return Promise.resolve(loadedApi)
  if (apiPromise) return apiPromise

  apiPromise = new Promise((resolve, reject) => {
    const previousReadyHandler = window.onYouTubeIframeAPIReady
    let settled = false
    let script = document.getElementById(API_SCRIPT_ID) as HTMLScriptElement | null
    let timeoutId = 0

    const cleanUp = () => {
      window.clearTimeout(timeoutId)
      script?.removeEventListener('error', handleError)
      if (window.onYouTubeIframeAPIReady === handleReady) {
        window.onYouTubeIframeAPIReady = previousReadyHandler
      }
    }

    const fail = (message: string) => {
      if (settled) return
      settled = true
      cleanUp()
      script?.remove()
      apiPromise = null
      reject(new Error(message))
    }

    const handleReady = () => {
      previousReadyHandler?.()
      const readyApi = availableApi()
      if (!readyApi || settled) return
      settled = true
      cleanUp()
      resolve(readyApi)
    }

    function handleError() {
      fail('No se pudo cargar la API del reproductor de YouTube.')
    }

    window.onYouTubeIframeAPIReady = handleReady

    if (!script) {
      script = document.createElement('script')
      script.id = API_SCRIPT_ID
      script.src = 'https://www.youtube.com/iframe_api'
      script.async = true
    }
    script.addEventListener('error', handleError, { once: true })
    if (!script.isConnected) document.head.appendChild(script)
    timeoutId = window.setTimeout(() => {
      fail('La API del reproductor de YouTube no respondió a tiempo.')
    }, API_LOAD_TIMEOUT_MS)
  })

  return apiPromise
}
