import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'

const ACCESS_KEY = 'cibersegura_access'
const REFRESH_KEY = 'cibersegura_refresh'

export const tokenStorage = {
  access: () => sessionStorage.getItem(ACCESS_KEY),
  refresh: () => sessionStorage.getItem(REFRESH_KEY),
  save: (access: string, refresh?: string) => {
    sessionStorage.setItem(ACCESS_KEY, access)
    if (refresh) sessionStorage.setItem(REFRESH_KEY, refresh)
  },
  clear: () => {
    sessionStorage.removeItem(ACCESS_KEY)
    sessionStorage.removeItem(REFRESH_KEY)
  },
  clearLegacy: () => {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
  },
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 12000,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const access = tokenStorage.access()
  if (access) config.headers.Authorization = `Bearer ${access}`
  return config
})

interface RetryConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

let refreshRequest: Promise<string> | null = null

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as RetryConfig | undefined
    const refresh = tokenStorage.refresh()
    const isAuthRoute = original?.url?.includes('/auth/token')

    if (error.response?.status === 401 && original && !original._retry && refresh && !isAuthRoute) {
      original._retry = true
      refreshRequest ??= axios
        .post(`${api.defaults.baseURL}/auth/token/refresh/`, { refresh })
        .then(({ data }) => {
          tokenStorage.save(data.access, data.refresh)
          return data.access as string
        })
        .finally(() => {
          refreshRequest = null
        })

      try {
        const access = await refreshRequest
        original.headers.Authorization = `Bearer ${access}`
        return api(original)
      } catch {
        tokenStorage.clear()
        window.dispatchEvent(new Event('auth-expired'))
      }
    }

    return Promise.reject(error)
  },
)

export function getErrorMessage(error: unknown): string {
  if (!axios.isAxiosError(error)) return 'Ocurrió un error inesperado. Inténtalo de nuevo.'
  const data = error.response?.data as Record<string, unknown> | undefined
  if (typeof data?.detail === 'string') return data.detail
  if (data) {
    const first = Object.values(data)[0]
    if (Array.isArray(first) && typeof first[0] === 'string') return first[0]
    if (typeof first === 'string') return first
  }
  if (error.code === 'ECONNABORTED') return 'La solicitud tardó demasiado. Revisa tu conexión.'
  return 'No fue posible conectar con el servicio. Inténtalo nuevamente.'
}
