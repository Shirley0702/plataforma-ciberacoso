export interface RegistrationForm {
  full_name: string
  birth_date: string
  email: string
  password: string
  confirm_password: string
  accepted_terms: boolean
}

export type RegistrationErrors = Partial<Record<keyof RegistrationForm, string>>

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const FULL_NAME_PATTERN = /^[\p{L}]+(?:[ '-][\p{L}]+)+$/u
const INVALID_FULL_NAME_CHARACTERS = /[^\p{L} '-]/gu

export const TODAY_DATE = toLocalDateInputValue(new Date())
export const EARLIEST_BIRTH_DATE = toLocalDateInputValue(
  new Date(new Date().getFullYear() - 120, new Date().getMonth(), new Date().getDate()),
)

function toLocalDateInputValue(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function calculateAge(birthDate: string): number | null {
  if (!birthDate) return null
  const [year, month, day] = birthDate.split('-').map(Number)
  const today = new Date()
  let age = today.getFullYear() - year
  if (today.getMonth() + 1 < month || (today.getMonth() + 1 === month && today.getDate() < day)) age -= 1
  return age
}

export function sanitizeFullName(value: string): string {
  return value.replace(INVALID_FULL_NAME_CHARACTERS, '')
}

export function validateRegistration(form: RegistrationForm): RegistrationErrors {
  const errors: RegistrationErrors = {}
  const fullName = form.full_name.trim().replace(/\s+/g, ' ')
  if (fullName.length > 120 || fullName.split(' ').length < 2 || !FULL_NAME_PATTERN.test(fullName)) {
    errors.full_name = 'Ingresa nombre y apellido usando únicamente letras, espacios, apóstrofes o guiones.'
  }
  if (!form.birth_date || form.birth_date > TODAY_DATE || form.birth_date < EARLIEST_BIRTH_DATE) {
    errors.birth_date = 'Ingresa una fecha de nacimiento válida que no sea futura.'
  }
  if (!EMAIL_PATTERN.test(form.email.trim())) {
    errors.email = 'Ingresa el correo institucional asignado por tu universidad.'
  }
  const missingPasswordRules = [
    form.password.length < 10 && '10 caracteres',
    !/[A-Z]/.test(form.password) && 'una mayúscula',
    !/[a-z]/.test(form.password) && 'una minúscula',
    !/\d/.test(form.password) && 'un número',
    !/[^A-Za-z0-9]/.test(form.password) && 'un símbolo',
  ].filter(Boolean)
  if (missingPasswordRules.length) {
    errors.password = `Incluye ${missingPasswordRules.join(', ')}.`
  }
  if (form.confirm_password !== form.password) {
    errors.confirm_password = 'Las contraseñas no coinciden.'
  }
  if (!form.accepted_terms) {
    errors.accepted_terms = 'Debes aceptar el aviso de uso orientativo.'
  }
  return errors
}
