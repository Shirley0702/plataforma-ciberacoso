export type InteractionType =
  | 'guided'
  | 'decision'
  | 'checklist'
  | 'practice'
  | 'safety_plan'

export interface InteractionCard {
  title: string
  body: string
}

export interface InteractionOption {
  id: string
  label: string
  feedback: string
  recommended?: boolean
}

export interface InteractionItem {
  id: string
  label: string
  detail: string
}

export interface InteractionConfig {
  cards?: InteractionCard[]
  options?: InteractionOption[]
  items?: InteractionItem[]
  completion_message?: string
  completion_feedback?: string
  privacy_note?: string
}

export interface InteractionResponse {
  selected_option?: string
  selected_items?: string[]
}

export interface LearningItem {
  id: number
  title: string
  summary: string
  content: string
  interaction_type: InteractionType
  duration_minutes: number
  interaction_prompt: string
  interaction_config: InteractionConfig
  interaction_response: InteractionResponse
  completed: boolean
}

export interface ModuleQuizQuestion {
  id: number
  text: string
  options: { id: number; label: string }[]
}

export interface QuizResult {
  score_percentage: number
  passed: boolean
  certificate?: CertificateData | null
}

export interface CertificateData {
  verification_code: string
  download_url: string
}

export interface CourseUnit {
  id: number
  title: string
  slug: string
  description: string
  order: number
  priority: number
  duration_minutes: number
  lessons: LearningItem[]
  quiz_unlocked: boolean
  quiz_questions: ModuleQuizQuestion[]
  latest_quiz: QuizResult | null
  certificate: CertificateData | null
}
