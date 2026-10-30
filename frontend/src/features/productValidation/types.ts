export interface ProductFeedback {
  id: number
  app_version: string
  ease_of_use: number
  content_clarity: number
  educational_usefulness: number
  satisfaction: number
  accessibility: number
  open_comment: string
  informed_consent: boolean
  submitted_at: string
  updated_at: string
}

export interface ProductFeedbackForm {
  ease_of_use: number
  content_clarity: number
  educational_usefulness: number
  satisfaction: number
  accessibility: number
  open_comment: string
  informed_consent: boolean
}
