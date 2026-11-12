export type InteractionType =
  | 'video'
  | 'guided'
  | 'decision'
  | 'matching'
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
  visual?: string
}

export interface InteractionConfig {
  cards?: InteractionCard[]
  options?: InteractionOption[]
  items?: InteractionItem[]
  completion_message?: string
  completion_feedback?: string
  privacy_note?: string
  video_url?: string
  video_watch_url?: string
  video_title?: string
  source_label?: string
}

export interface InteractionResponse {
  selected_items?: string[]
  chosen_option?: string
  matches?: Record<string, string>
  watched?: boolean
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
