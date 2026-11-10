import { useState } from 'react'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { ConsequencePuzzle } from './ConsequencePuzzle'
import { GuidedExploration } from './GuidedExploration'
import { MatchingPuzzle } from './MatchingPuzzle'
import { SafetyKitBuilder } from './SafetyKitBuilder'
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

  it('construye un kit personal sin pedir datos privados', async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()
    render(
      <SafetyKitBuilder
        items={[
          { id: 'persona', label: 'Persona de confianza', detail: 'Alguien que pueda acompañar' },
          { id: 'canal', label: 'Canal universitario', detail: 'Un servicio de orientación' },
        ]}
        selectedItems={[]}
        completed={false}
        saving={false}
        privacyNote="No escribas nombres ni teléfonos."
        onChange={onChange}
        onCompletion={vi.fn()}
      />,
    )

    expect(screen.getByText(/No escribas nombres ni teléfonos/)).toBeVisible()
    expect(screen.getByRole('button', { name: 'Guardar mi kit' })).toBeDisabled()
    await user.click(screen.getByRole('checkbox', { name: /Persona de confianza/ }))
    expect(onChange).toHaveBeenCalledWith(['persona'])
  })

  it('presenta el video sin resumen ni pregunta adicional', async () => {
    const user = userEvent.setup()
    const onWatchedChange = vi.fn()
    render(
      <VideoExperience
        viewingPrompt="Mira el video completo antes de continuar."
        config={{
          video_url: 'https://www.youtube-nocookie.com/embed/video-seguro',
          video_watch_url: 'https://www.youtube.com/watch?v=video-seguro',
          video_title: 'Convivencia respetuosa',
          source_label: 'Fuente educativa',
        }}
        watched={false}
        completed={false}
        saving={false}
        onWatchedChange={onWatchedChange}
        onCompletion={vi.fn()}
      />,
    )

    const video = screen.getByTitle('Convivencia respetuosa')
    expect(video).toHaveAttribute('loading', 'lazy')
    expect(video).not.toHaveAttribute('autoplay')
    expect(screen.queryByText(/resumen/i)).not.toBeInTheDocument()
    expect(screen.queryByRole('radio')).not.toBeInTheDocument()
    await user.click(screen.getByRole('checkbox', { name: /Terminé de ver el video completo/ }))
    expect(onWatchedChange).toHaveBeenCalledWith(true)
  })
})
