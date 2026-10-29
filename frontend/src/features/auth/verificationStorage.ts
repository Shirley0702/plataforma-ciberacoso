const PENDING_EMAIL_KEY = 'cibersegura_pending_email'

export const verificationStorage = {
  get: () => sessionStorage.getItem(PENDING_EMAIL_KEY) ?? '',
  save: (email: string) => sessionStorage.setItem(PENDING_EMAIL_KEY, email),
  clear: () => sessionStorage.removeItem(PENDING_EMAIL_KEY),
}
