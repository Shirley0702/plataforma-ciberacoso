import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'

import { TextReviewPage } from './TextReviewPage'

const apiMock = vi.hoisted(() => ({
  get: vi.fn(),
  post: vi.fn(),
}))

vi.mock('../../../shared/api/httpClient', () => ({
  api: apiMock,
  getErrorMessage: () => 'No fue posible completar la solicitud.',
  tokenStorage: { clear: vi.fn() },
}))

const result = {
  result_id: 1,
  possible_signals: true,
  attention_level: 'moderate' as const,
  title: 'Conviene revisar esta situación con cuidado',
  guidance: 'El contexto y la repetición también son importantes.',
  contexts_considered: ['Situación repetida', 'Privacidad o difusión'],
  recommendations: ['Conserva capturas si hacerlo no aumenta el riesgo.'],
  recommended_unit: {
    id: 1,
    slug: 'bienestar-digital',
    title: 'Bienestar y Seguridad Digital',
    description: 'Herramientas prácticas.',
  },
  created_at: '2026-10-29T10:00:00Z',
  privacy_notice: 'El texto original no se guardó en la base de datos.',
}

function renderPage() {
  return render(
    <MemoryRouter>
      <TextReviewPage />
    </MemoryRouter>,
  )
}

describe('TextReviewPage', () => {
  beforeEach(() => {
    apiMock.get.mockResolvedValue({ data: null })
    apiMock.post.mockResolvedValue({ data: result })
  })

  it('explica la privacidad y bloquea el envío de una descripción incompleta', async () => {
    const { container } = renderPage()

    expect(screen.getByText(/El texto no se guarda/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Obtener Orientación' })).toBeDisabled()
    await waitFor(() => expect(apiMock.get).toHaveBeenCalledWith('/text-reviews/latest/'))

    const accessibility = await axe(container)
    expect(accessibility.violations).toEqual([])
  })

  it('envía la situación y presenta recomendaciones conectadas con el curso', async () => {
    const user = userEvent.setup()
    renderPage()
    const description = 'Comparten capturas para burlarse y continúan aunque se pidió que se detuvieran.'

    await user.type(screen.getByLabelText('Situación a Revisar'), description)
    await user.click(screen.getByRole('button', { name: 'Obtener Orientación' }))

    await waitFor(() => {
      expect(apiMock.post).toHaveBeenCalledWith('/text-reviews/review/', { text: description })
    })
    expect(screen.getByRole('heading', { name: result.title })).toBeInTheDocument()
    expect(screen.getByText('Situación repetida')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continuar con Mi Curso' })).toHaveAttribute('href', '/curso')
    expect(screen.getByText(/no se guardó en la base de datos/i)).toBeInTheDocument()
  })
})
