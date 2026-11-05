import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'

import { ProductFeedbackPage } from './ProductFeedbackPage'

const apiMock = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn() }))

vi.mock('../../../shared/api/httpClient', () => ({
  api: apiMock,
  getErrorMessage: () => 'No fue posible completar la solicitud.',
}))

const savedFeedback = {
  id: 1,
  app_version: '1.0.0',
  ease_of_use: 5,
  content_clarity: 5,
  educational_usefulness: 5,
  satisfaction: 5,
  accessibility: 5,
  open_comment: '',
  informed_consent: true,
  submitted_at: '2026-10-29T12:00:00Z',
  updated_at: '2026-10-29T12:00:00Z',
}

describe('ProductFeedbackPage', () => {
  beforeEach(() => {
    apiMock.get.mockResolvedValue({ data: null })
    apiMock.post.mockResolvedValue({ data: savedFeedback })
  })

  it('es accesible y exige una respuesta completa', async () => {
    const user = userEvent.setup()
    const { container } = render(<MemoryRouter><ProductFeedbackPage /></MemoryRouter>)
    await screen.findByRole('button', { name: 'Guardar Evaluación' })

    const accessibility = await axe(container)
    expect(accessibility.violations).toEqual([])

    await user.click(screen.getByRole('button', { name: 'Guardar Evaluación' }))
    expect(screen.getByRole('alert')).toHaveTextContent('Responde las cinco preguntas')
    expect(apiMock.post).not.toHaveBeenCalled()
  })

  it('guarda las cinco métricas y el consentimiento', async () => {
    const user = userEvent.setup()
    render(<MemoryRouter><ProductFeedbackPage /></MemoryRouter>)
    await screen.findByRole('button', { name: 'Guardar Evaluación' })

    for (const question of [
      '¿Qué tan fácil fue utilizar la plataforma?',
      '¿Qué tan claros fueron los textos y las instrucciones?',
      '¿Qué tan útil fue el contenido para tu aprendizaje?',
      '¿Qué tan satisfecho estás con tu experiencia general?',
      '¿Qué tan fácil fue percibir y operar los controles?',
    ]) {
      await user.click(screen.getByLabelText(`${question}: 5 de 5`))
    }
    await user.click(screen.getByLabelText(/Acepto que estas respuestas/i))
    await user.click(screen.getByRole('button', { name: 'Guardar Evaluación' }))

    await waitFor(() => expect(apiMock.post).toHaveBeenCalledWith(
      '/product-validation/feedback/',
      expect.objectContaining({
        ease_of_use: 5,
        content_clarity: 5,
        educational_usefulness: 5,
        satisfaction: 5,
        accessibility: 5,
        informed_consent: true,
      }),
    ))
    expect(screen.getByRole('status')).toHaveTextContent('Tu evaluación quedó guardada')
  })

  it('no muestra el formulario antes de completar el curso', async () => {
    apiMock.get.mockRejectedValueOnce(new Error('forbidden'))

    render(<MemoryRouter><ProductFeedbackPage /></MemoryRouter>)

    expect(await screen.findByRole('alert')).toHaveTextContent('No fue posible completar la solicitud.')
    expect(screen.queryByRole('button', { name: 'Guardar Evaluación' })).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Volver al curso' })).toHaveAttribute('href', '/curso')
  })
})
