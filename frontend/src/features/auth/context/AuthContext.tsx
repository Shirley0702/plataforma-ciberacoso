import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { api, tokenStorage } from '../../../shared/api/httpClient'
import type { User } from '../../../shared/types/user'

interface RegisterPayload {
  email: string
  birth_date: string
  password: string
  confirm_password: string
  full_name: string
  accepted_terms: boolean
}

interface AuthValue {
  user: User | null
  loading: boolean
  login: (identifier: string, password: string) => Promise<void>
  register: (payload: RegisterPayload) => Promise<string>
  verifyEmail: (email: string, code: string) => Promise<void>
  resendVerification: (email: string) => Promise<void>
  refreshUser: () => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    tokenStorage.clearLegacy()
    const restore = async () => {
      if (!tokenStorage.access()) {
        setLoading(false)
        return
      }
      try {
        const { data } = await api.get<User>('/users/me/')
        setUser(data)
      } catch {
        tokenStorage.clear()
      } finally {
        setLoading(false)
      }
    }
    void restore()

    const expire = () => setUser(null)
    window.addEventListener('auth-expired', expire)
    return () => window.removeEventListener('auth-expired', expire)
  }, [])

  const value = useMemo<AuthValue>(
    () => ({
      user,
      loading,
      login: async (identifier, password) => {
        const { data } = await api.post<{ access: string; refresh: string }>('/auth/token/', {
          identifier,
          password,
        })
        tokenStorage.save(data.access, data.refresh)
        const profile = await api.get<User>('/users/me/')
        setUser(profile.data)
      },
      register: async (payload) => {
        const { data } = await api.post<{ email: string }>(
          '/auth/register/',
          payload,
        )
        return data.email
      },
      verifyEmail: async (email, code) => {
        const { data } = await api.post<{ user: User; access: string; refresh: string }>(
          '/auth/verify-email/',
          { email, code },
        )
        tokenStorage.save(data.access, data.refresh)
        setUser(data.user)
      },
      resendVerification: async (email) => {
        await api.post('/auth/resend-verification/', { email })
      },
      refreshUser: async () => {
        const { data } = await api.get<User>('/users/me/')
        setUser(data)
      },
      logout: async () => {
        const refresh = tokenStorage.refresh()
        try {
          if (refresh) await api.post('/auth/logout/', { refresh })
        } finally {
          tokenStorage.clear()
          setUser(null)
        }
      },
    }),
    [loading, user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth debe utilizarse dentro de AuthProvider')
  return context
}
