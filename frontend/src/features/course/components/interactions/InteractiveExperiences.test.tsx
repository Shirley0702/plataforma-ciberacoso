import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { ChecklistInteraction } from './ChecklistInteraction'
import { ChoiceInteraction } from './ChoiceInteraction'
import { GuidedExploration } from './GuidedExploration'

describe('experiencias interactivas del curso', () => {
  it('exige explorar todas las tarjetas antes de completar', async () => {
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

    const completeButton = screen.getByRole('button', { name: 'Completar exploración' })
    expect(completeButton).toBeDisabled()
    await user.click(screen.getByRole('button', { name: /Primera idea/ }))
    expect(screen.getByText('Detalle uno')).toBeVisible()
    expect(completeButton).toBeDisabled()
    await user.click(screen.getByRole('button', { name: /Segunda idea/ }))
    expect(completeButton).toBeEnabled()
    await user.click(completeButton)
    expect(onCompletion).toHaveBeenCalledWith(true)
  })

  it('permite elegir una decisión sin revelar cuál se recomienda', async () => {
    const user = userEvent.setup()
    const onSelect = vi.fn()
    render(
      <ChoiceInteraction
        lessonId={1}
        options={[
          { id: 'pausar', label: 'Pausar y buscar apoyo', feedback: 'Buena opción', recommended: true },
          { id: 'responder', label: 'Responder de inmediato', feedback: 'Puede aumentar el riesgo' },
        ]}
        completed={false}
        saving={false}
        actionLabel="Confirmar decisión"
        onSelect={onSelect}
        onCompletion={vi.fn()}
      />,
    )

    expect(screen.queryByText(/recomendad/i)).not.toBeInTheDocument()
    await user.click(screen.getByRole('radio', { name: 'Pausar y buscar apoyo' }))
    expect(onSelect).toHaveBeenCalledWith('pausar')
  })

  it('requiere revisar todos los pasos del plan y muestra la nota de privacidad', async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()
    render(
      <ChecklistInteraction
        items={[
          { id: 'persona', label: 'Persona de confianza', detail: 'Alguien que pueda acompañar' },
          { id: 'canal', label: 'Canal universitario', detail: 'Un servicio de orientación' },
        ]}
        selectedItems={[]}
        completed={false}
        saving={false}
        privacyNote="No escribas nombres ni teléfonos."
        actionLabel="Guardar plan seguro"
        onChange={onChange}
        onCompletion={vi.fn()}
      />,
    )

    expect(screen.getByText(/No escribas nombres ni teléfonos/)).toBeVisible()
    expect(screen.getByRole('button', { name: 'Guardar plan seguro' })).toBeDisabled()
    await user.click(screen.getByRole('checkbox', { name: /Persona de confianza/ }))
    expect(onChange).toHaveBeenCalledWith(['persona'])
  })
})
