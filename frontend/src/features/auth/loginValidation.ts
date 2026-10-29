export interface LoginForm {
  identifier: string
  password: string
}

export type LoginErrors = Partial<Record<keyof LoginForm, string>>

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function validateLogin(form: LoginForm): LoginErrors {
  const errors: LoginErrors = {}
  const identifier = form.identifier.trim().toLowerCase()

  if (!identifier) {
    errors.identifier = 'El correo institucional es obligatorio.'
  } else if (identifier !== 'demo' && !EMAIL_PATTERN.test(identifier)) {
    errors.identifier = 'Ingresa un correo institucional válido.'
  }
  if (!form.password) {
    errors.password = 'La contraseña es obligatoria.'
  }
  return errors
}
