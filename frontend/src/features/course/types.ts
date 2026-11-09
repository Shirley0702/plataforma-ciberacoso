export interface LearningItem {
  id: number
  title: string
  summary: string
  content: string
  kind: 'lesson' | 'activity'
  duration_minutes: number
  activity_prompt: string
  activity_options: { id: string; label: string; feedback: string }[]
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
