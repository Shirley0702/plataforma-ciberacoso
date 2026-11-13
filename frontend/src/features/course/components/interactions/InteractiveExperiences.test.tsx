import { useState } from 'react'
import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import type { CoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import { DecisionMapPuzzle } from './DecisionMapPuzzle'
import { DialogueBuilderPuzzle } from './DialogueBuilderPuzzle'
import { GuidedExploration } from './GuidedExploration'
import { MatchingPuzzle } from './MatchingPuzzle'
import { OrderingPuzzle } from './OrderingPuzzle'
import { VideoExperience } from './VideoExperience'

const visual: CoursePuzzleVisual = {
  src: '/assets/course-puzzles/test.jpg',
  alt: 'Escena educativa para resolver el puzzle.',
  videoCue: 'Usa la idea central del video como pista.',
}

describe('experiencias interactivas del curso', () => {
  it('descubre señales dentro de una escena y revela su significado', async () => {
    const user = userEvent.setup()
    const onCompletion = vi.fn().mockResolvedValue(undefined)
    render(
      <GuidedExploration
        cards={[
          { title: 'Límite', body: 'Idea revelada' },
          { title: 'Apoyo', body: 'Segunda idea' },
          { title: 'Control', body: 'Tercera idea' },
        ]}
        prompt="Encuentra las señales."
        visual={visual}
        completed={false}
        saving={false}
        onCompletion={onCompletion}
      />,
    )

    await user.click(screen.getByRole('button', { name: /Descubrir señal 1: Límite/ }))
    expect(screen.getByText('Idea revelada')).toBeVisible()
    await user.click(screen.getByRole('button', { name: /Descubrir señal 2: Apoyo/ }))
    await user.click(screen.getByRole('button', { name: /Descubrir señal 3: Control/ }))
    expect(onCompletion).toHaveBeenCalledWith(true)
  })

  it('enseña consecuencias en un mapa antes de elegir una ruta', async () => {
    const user = userEvent.setup()
    const onCompletion = vi.fn().mockResolvedValue(undefined)

    function StatefulPuzzle() {
      const [exploredOptionIds, setExploredOptionIds] = useState<string[]>([])
      const [chosenOptionId, setChosenOptionId] = useState<string>()
      return (
        <DecisionMapPuzzle
          options={[
            { id: 'pausar', label: 'Pausar y buscar apoyo', feedback: 'Conserva opciones', recommended: true },
            { id: 'responder', label: 'Responder de inmediato', feedback: 'Puede aumentar el riesgo' },
          ]}
          exploredOptionIds={exploredOptionIds}
          chosenOptionId={chosenOptionId}
          completed={false}
          saving={false}
          prompt="Compara los caminos."
          visual={visual}
          onChange={(nextIds, nextChoice) => {
            setExploredOptionIds(nextIds)
            setChosenOptionId(nextChoice)
          }}
          onCompletion={onCompletion}
        />
      )
    }

    render(<StatefulPuzzle />)
    await user.click(screen.getByRole('button', { name: /Explorar camino 1: Pausar y buscar apoyo/ }))
    await user.click(screen.getByRole('button', { name: /Explorar camino 2: Responder de inmediato/ }))
    await user.click(screen.getByRole('button', { name: /Elegir camino 2: Responder de inmediato/ }))
    expect(screen.getByRole('alert')).toHaveTextContent(/aumenta el riesgo/i)
    await user.click(screen.getByRole('button', { name: /Elegir camino 1: Pausar y buscar apoyo/ }))
    expect(onCompletion).toHaveBeenCalledWith(true, {
      selected_items: ['pausar', 'responder'],
      chosen_option: 'pausar',
    })
  })

  it('construye y compara respuestas dentro de un diálogo', async () => {
    const user = userEvent.setup()
    const onCompletion = vi.fn().mockResolvedValue(undefined)

    function StatefulDialogue() {
      const [explored, setExplored] = useState<string[]>([])
      const [chosen, setChosen] = useState<string>()
      return (
        <DialogueBuilderPuzzle
          options={[
            { id: 'ataque', label: 'Responder con una amenaza', feedback: 'Escala la situación' },
            { id: 'limite', label: 'Marcar un límite claro', feedback: 'Conserva el control', recommended: true },
          ]}
          exploredOptionIds={explored}
          chosenOptionId={chosen}
          completed={false}
          saving={false}
          prompt="Construye una respuesta."
          visual={visual}
          onChange={(nextIds, nextChoice) => {
            setExplored(nextIds)
            setChosen(nextChoice)
          }}
          onCompletion={onCompletion}
        />
      )
    }

    render(<StatefulDialogue />)
    await user.click(screen.getByRole('button', { name: /Probar respuesta 1: Responder con una amenaza/ }))
    expect(screen.getByText('Escala la situación')).toBeVisible()
    await user.click(screen.getByRole('button', { name: /Probar respuesta 2: Marcar un límite claro/ }))
    await user.click(screen.getByRole('button', { name: /Elegir respuesta final 2: Marcar un límite claro/ }))
    expect(onCompletion).toHaveBeenCalledWith(true, {
      selected_items: ['ataque', 'limite'],
      chosen_option: 'limite',
    })
  })

  it('identifica ambos extremos de cada conexión y permite comprobarlas', async () => {
    const user = userEvent.setup()
    const onCompletion = vi.fn().mockResolvedValue(undefined)

    function StatefulMatchingPuzzle() {
      const [matches, setMatches] = useState<Record<string, string>>({})
      return (
        <MatchingPuzzle
          items={[
            { id: 'hecho', label: 'Hecho observable', detail: 'Puede describirse sin adivinar intenciones', visual: 'observe' },
            { id: 'apoyo', label: 'Red de apoyo', detail: 'Puede acompañar', visual: 'support' },
          ]}
          matches={matches}
          prompt="Conecta las señales."
          visual={visual}
          completed={false}
          saving={false}
          onChange={setMatches}
          onCompletion={onCompletion}
        />
      )
    }

    render(<StatefulMatchingPuzzle />)
    await user.click(screen.getByRole('button', { name: /Hecho observable/ }))
    await user.click(screen.getByRole('button', { name: /Puede describirse/ }))
    expect(screen.getAllByLabelText('Pareja 1')).toHaveLength(2)
    await user.click(screen.getByRole('button', { name: /Red de apoyo/ }))
    await user.click(screen.getByRole('button', { name: /Puede acompañar/ }))
    expect(screen.getAllByLabelText('Pareja 2')).toHaveLength(2)
    await user.click(screen.getByRole('button', { name: 'Comprobar 2 conexiones' }))
    expect(onCompletion).toHaveBeenCalledWith(true)
  })

  it('ordena una ruta ilustrada mediante controles accesibles', async () => {
    const user = userEvent.setup()
    const onCompletion = vi.fn().mockResolvedValue(undefined)

    function StatefulOrderingPuzzle() {
      const [order, setOrder] = useState<string[]>([])
      return (
        <OrderingPuzzle
          items={[
            { id: 'pausa', label: 'Hacer una pausa', detail: 'Recuperar calma', visual: 'pause' },
            { id: 'apoyo', label: 'Buscar apoyo', detail: 'No quedarse a solas', visual: 'support' },
          ]}
          orderedItemIds={order}
          prompt="Ordena la ruta."
          visual={visual}
          completed={false}
          saving={false}
          privacyNote="No escribas nombres ni teléfonos."
          onChange={setOrder}
          onCompletion={onCompletion}
        />
      )
    }

    render(<StatefulOrderingPuzzle />)
    await user.click(screen.getByRole('button', { name: 'Mover Buscar apoyo un lugar hacia el final' }))
    await user.click(screen.getByRole('button', { name: 'Comprobar la ruta' }))
    expect(onCompletion).toHaveBeenCalledWith(true)
  })

  it('marca el video automáticamente cuando el reproductor llega al final', async () => {
    let stateChangeHandler: ((event: { data: number }) => void) | undefined
    class MockYouTubePlayer {
      constructor(_element: HTMLIFrameElement, options: { events: { onStateChange: (event: { data: number }) => void } }) {
        stateChangeHandler = options.events.onStateChange
      }
      destroy() {}
    }
    Object.defineProperty(window, 'YT', { configurable: true, value: { Player: MockYouTubePlayer } })
    const onCompletion = vi.fn().mockResolvedValue(undefined)

    function StatefulVideoExperience() {
      const [completed, setCompleted] = useState(false)
      return (
        <VideoExperience
          viewingPrompt="Mira el video completo antes de continuar."
          config={{
            video_url: 'https://www.youtube-nocookie.com/embed/video-seguro',
            video_watch_url: 'https://www.youtube.com/watch?v=video-seguro',
            video_title: 'Convivencia respetuosa',
            source_label: 'Fuente educativa',
          }}
          completed={completed}
          saving={false}
          onCompletion={async (...args) => {
            await onCompletion(...args)
            setCompleted(true)
          }}
        />
      )
    }

    render(<StatefulVideoExperience />)
    const video = screen.getByTitle('Convivencia respetuosa')
    expect(video.getAttribute('src')).toContain('enablejsapi=1')
    await waitFor(() => expect(stateChangeHandler).toBeDefined())
    act(() => stateChangeHandler?.({ data: 0 }))
    await waitFor(() => expect(onCompletion).toHaveBeenCalledWith(true, { watched: true }))
    delete window.YT
  })
})
