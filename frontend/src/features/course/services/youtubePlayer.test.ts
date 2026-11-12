import { afterEach, describe, expect, it, vi } from 'vitest'

afterEach(() => {
  document.getElementById('youtube-iframe-api')?.remove()
  delete window.YT
  delete window.onYouTubeIframeAPIReady
  vi.resetModules()
})

describe('servicio del reproductor de YouTube', () => {
  it('prepara el video para recibir eventos de finalización', async () => {
    const { buildTrackedVideoUrl } = await import('./youtubePlayer')
    const url = new URL(buildTrackedVideoUrl(
      'https://www.youtube-nocookie.com/embed/video-seguro',
    ))

    expect(url.searchParams.get('enablejsapi')).toBe('1')
    expect(url.searchParams.get('playsinline')).toBe('1')
    expect(url.searchParams.get('origin')).toBe(window.location.origin)
  })

  it('carga la API oficial y la reutiliza', async () => {
    const { loadYouTubePlayerApi } = await import('./youtubePlayer')
    class MockPlayer {
      destroy() {}
    }
    const loading = loadYouTubePlayerApi()
    const script = document.getElementById('youtube-iframe-api')

    expect(script).toHaveAttribute('src', 'https://www.youtube.com/iframe_api')
    Object.defineProperty(window, 'YT', {
      configurable: true,
      value: { Player: MockPlayer },
    })
    window.onYouTubeIframeAPIReady?.()

    const api = await loading
    await expect(loadYouTubePlayerApi()).resolves.toBe(api)
    expect(document.querySelectorAll('#youtube-iframe-api')).toHaveLength(1)
  })

  it('permite volver a cargar la API después de un error de red', async () => {
    const { loadYouTubePlayerApi } = await import('./youtubePlayer')
    const firstLoading = loadYouTubePlayerApi()
    const failedScript = document.getElementById('youtube-iframe-api') as HTMLScriptElement
    failedScript.dispatchEvent(new Event('error'))

    await expect(firstLoading).rejects.toThrow('No se pudo cargar')
    expect(document.getElementById('youtube-iframe-api')).not.toBeInTheDocument()

    class MockPlayer {
      destroy() {}
    }
    const secondLoading = loadYouTubePlayerApi()
    Object.defineProperty(window, 'YT', {
      configurable: true,
      value: { Player: MockPlayer },
    })
    window.onYouTubeIframeAPIReady?.()

    await expect(secondLoading).resolves.toEqual({ Player: MockPlayer })
  })
})
