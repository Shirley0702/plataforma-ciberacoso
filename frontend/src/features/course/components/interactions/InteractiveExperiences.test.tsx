import { useState } from 'react'
import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { ConsequencePuzzle } from './ConsequencePuzzle'
import { GuidedExploration } from './GuidedExploration'
import { MatchingPuzzle } from './MatchingPuzzle'
import { OrderingPuzzle } from './OrderingPuzzle'
import { VideoExperience } from './VideoExperience'

describe('experiencias interactivas del curso', () => {
  it('convierte las tarjetas en un puzzle de pistas sin calificación', async () => {
    const user = userEvent.setup()
    const onCompletion = vi.fn().mockResolvedValue(undefined)
    render(
      <GuidedExploration
        cards={[
          { title: 'Primera idea', body: 'Detalle uno' },
          { title: 'Segunda idea', body: 'Detalle dos' },
        ]}
        completed={false}
        saving={false}
        onCompletion={onCompletion}
      />,
    )

    const completeButton = screen.getByRole('button', { name: 'Guardar lo aprendido' })
    expect(completeButton).toBeDisabled()
    await user.click(screen.getByRole('button', { name: /Primera idea/ }))
    expect(screen.getByText('Detalle uno')).toBeVisible()
    await user.click(screen.getByRole('button', { name: /Segunda idea/ }))
    expect(completeButton).toBeEnabled()
    await user.click(completeButton)
    expect(onCompletion).toHaveBeenCalledWith(true)
  })

  it('enseña consecuencias al explorar todos los caminos', async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()

    function StatefulConsequencePuzzle() {
      const [exploredOptionIds, setExploredOptionIds] = useState<string[]>([])
      const handleChange = (nextIds: string[]) => {
        onChange(nextIds)
        setExploredOptionIds(nextIds)
      }

      return (
        <ConsequencePuzzle
          options={[
            { id: 'pausar', label: 'Pausar y buscar apoyo', feedback: 'Conserva opciones' },
            { id: 'responder', label: 'Responder de inmediato', feedback: 'Puede aumentar el riesgo' },
          ]}
          exploredOptionIds={exploredOptionIds}
          completed={false}
          saving={false}
          actionLabel="Guardar lo descubierto"
          onChange={handleChange}
          onCompletion={vi.fn()}
        />
      )
    }

    render(<StatefulConsequencePuzzle />)

    expect(screen.getByText(/Aquí no hay nota/)).toBeVisible()
    await user.click(screen.getByRole('button', { name: /Pausar y buscar apoyo/ }))
    expect(screen.getByText('Conserva opciones')).toBeVisible()
    expect(onChange).toHaveBeenCalledWith(['pausar'])
  })

  it('permite resolver conexiones sin penalización', async () => {
    const user = userEvent.setup()
    const onCompletion = vi.fn().mockResolvedValue(undefined)

    function StatefulMatchingPuzzle() {
      const [matches, setMatches] = useState<Record<string, string>>({})
      return (
        <MatchingPuzzle
          items={[
            { id: 'hecho', label: 'Hecho observable', detail: 'Algo que puede describirse sin adivinar intenciones' },
            { id: 'apoyo', label: 'Red de apoyo', detail: 'Personas o canales que pueden acompañar' },
          ]}
          matches={matches}
          completed={false}
          saving={false}
          onChange={setMatches}
          onCompletion={onCompletion}
        />
      )
    }

    render(<StatefulMatchingPuzzle />)
    const selects = screen.getAllByRole('combobox')
    await user.selectOptions(selects[0], 'hecho')
    await user.selectOptions(selects[1], 'apoyo')
    await user.click(screen.getByRole('button', { name: 'Comprobar conexiones' }))
    expect(onCompletion).toHaveBeenCalledWith(true)
  })

  it('ordena un puzzle visual también mediante controles accesibles', async () => {
    const user = userEvent.setup()
    const onCompletion = vi.fn().mockResolvedValue(undefined)

    function StatefulOrderingPuzzle() {
      const [order, setOrder] = useState<string[]>([])
      return (
        <OrderingPuzzle
          items={[
            { id: 'pausa', label: 'Hacer una pausa', detail: 'Recuperar calma', visual: '✋' },
            { id: 'apoyo', label: 'Buscar apoyo', detail: 'No quedarse a solas', visual: '🤝' },
          ]}
          orderedItemIds={order}
          completed={false}
          saving={false}
          privacyNote="No escribas nombres ni teléfonos."
          onChange={setOrder}
          onCompletion={onCompletion}
        />
      )
    }

    render(<StatefulOrderingPuzzle />)

    expect(screen.getByText(/No escribas nombres ni teléfonos/)).toBeVisible()
    expect(screen.getByText('Buscar apoyo')).toBeVisible()
    await user.click(screen.getByRole('button', { name: 'Mover Buscar apoyo hacia abajo' }))
    await user.click(screen.getByRole('button', { name: 'Comprobar secuencia' }))
    expect(onCompletion).toHaveBeenCalledWith(true)
  })

  it('marca el video automáticamente cuando el reproductor llega al final', async () => {
    let stateChangeHandler: ((event: { data: number }) => void) | undefined
    class MockYouTubePlayer {
      constructor(
        _element: HTMLIFrameElement,
        options: { events: { onStateChange: (event: { data: number }) => void } },
      ) {
        stateChangeHandler = options.events.onStateChange
      }

      destroy() {}
    }
    Object.defineProperty(window, 'YT', {
      configurable: true,
      value: { Player: MockYouTubePlayer },
    })
    const onCompletion = vi.fn().mockResolvedValue(undefined)
    render(
      <VideoExperience
        viewingPrompt="Mira el video completo antes de continuar."
        config={{
          video_url: 'https://www.youtube-nocookie.com/embed/video-seguro',
          video_watch_url: 'https://www.youtube.com/watch?v=video-seguro',
          video_title: 'Convivencia respetuosa',
          source_label: 'Fuente educativa',
        }}
        completed={false}
        saving={false}
        onCompletion={onCompletion}
      />,
    )

    const video = screen.getByTitle('Convivencia respetuosa')
    expect(video).toHaveAttribute('loading', 'lazy')
    expect(video).not.toHaveAttribute('autoplay')
    expect(video.getAttribute('src')).toContain('enablejsapi=1')
    expect(screen.queryByText(/resumen/i)).not.toBeInTheDocument()
    expect(screen.queryByRole('radio')).not.toBeInTheDocument()
    expect(screen.queryByRole('checkbox')).not.toBeInTheDocument()
    expect(screen.getByText(/Por hacer: mira el video hasta el final/)).toBeVisible()
    await waitFor(() => expect(stateChangeHandler).toBeDefined())
    act(() => stateChangeHandler?.({ data: 0 }))
    expect(onCompletion).toHaveBeenCalledWith(true, { watched: true }, false)
    delete window.YT
  })
})
