import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'

import { AppShell } from '../app/layout/AppShell'
import { LoginPage } from '../features/auth/pages/LoginPage'
import { RegisterPage } from '../features/auth/pages/RegisterPage'
import { DiagnosticPage } from '../features/diagnostic/pages/DiagnosticPage'
import { ResourcesPage } from '../features/resources/pages/ResourcesPage'

const apiMock = vi.hoisted(() => ({
  get: vi.fn(),
  post: vi.fn(),
}))

const authMock = vi.hoisted(() => ({
  user: {
    id: 2,
    username: 'demo',
    email: 'demo@espe.edu.ec',
    full_name: 'Usuario Demo',
    birth_date: '2002-01-01',
    age: 24,
    avatar_url: '',
    bio: '',
    phone: '',
    city: '',
  },
  loading: false,
  login: vi.fn(),
  register: vi.fn(),
  verifyEmail: vi.fn(),
  resendVerification: vi.fn(),
  refreshUser: vi.fn(),
  logout: vi.fn(),
}))

vi.mock('../shared/api/httpClient', () => ({
  api: apiMock,
  getErrorMessage: () => 'No fue posible completar la solicitud.',
  tokenStorage: { clear: vi.fn() },
}))

vi.mock('../features/auth/context/AuthContext', () => ({
  useAuth: () => authMock,
}))

async function expectNoAutomatedViolations(container: HTMLElement) {
  const result = await axe(container)
  expect(result.violations).toEqual([])
}

describe('auditoría automatizada de accesibilidad', () => {
  beforeEach(() => {
    apiMock.get.mockReset()
    apiMock.post.mockReset()
    authMock.user = {
      id: 2,
      username: 'demo',
      email: 'demo@espe.edu.ec',
      full_name: 'Usuario Demo',
      birth_date: '2002-01-01',
      age: 24,
      avatar_url: '',
      bio: '',
      phone: '',
      city: '',
    }
  })

  it('audita las pantallas públicas de acceso y registro sin excluir contraste', async () => {
    const login = render(<MemoryRouter><LoginPage /></MemoryRouter>)
    await expectNoAutomatedViolations(login.container)
    login.unmount()

    const register = render(<MemoryRouter><RegisterPage /></MemoryRouter>)
    await expectNoAutomatedViolations(register.container)
  })

  it('ofrece salto al contenido, título de página y navegación semántica', async () => {
    const { container } = render(
      <MemoryRouter initialEntries={['/inicio']}>
        <Routes>
          <Route element={<AppShell />}>
            <Route path="/inicio" element={<h1>Inicio accesible</h1>} />
          </Route>
        </Routes>
      </MemoryRouter>,
    )

    expect(screen.getByRole('link', { name: 'Saltar al contenido' })).toHaveAttribute('href', '#contenido-principal')
    expect(screen.getByRole('main')).toHaveFocus()
    expect(document.title).toBe('Inicio | CiberSegura')
    await expectNoAutomatedViolations(container)
  })

  it('audita la evaluación con datos representativos', async () => {
    apiMock.get.mockResolvedValue({
      data: [{
        id: 1,
        text: 'Una conversación te hace sentir incómodo. ¿Qué sucede con más frecuencia?',
        order: 1,
        options: [
          { id: 10, label: 'Puedo expresarlo y la otra persona se detiene.', order: 1 },
          { id: 11, label: 'La situación continúa aunque pido que se detenga.', order: 2 },
        ],
      }],
    })

    const { container } = render(<MemoryRouter><DiagnosticPage /></MemoryRouter>)
    await screen.findByRole('heading', { level: 2 })
    await expectNoAutomatedViolations(container)
  })

  it('audita recursos incluso cuando el directorio llega de forma asíncrona', async () => {
    apiMock.get.mockResolvedValue({
      data: [{
        id: 1,
        name: 'ECU 911',
        description: 'Atención de emergencias en Ecuador.',
        url: 'https://www.ecu911.gob.ec/',
        phone: '911',
        country: 'Ecuador',
        emergency: true,
      }],
    })

    const { container } = render(<MemoryRouter><ResourcesPage /></MemoryRouter>)
    await waitFor(() => expect(screen.getByRole('heading', { name: 'ECU 911' })).toBeInTheDocument())
    await expectNoAutomatedViolations(container)
  })
})
