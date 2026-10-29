import type { CourseSummary } from '../../shared/types/courseSummary'
import type { User } from '../../shared/types/user'

export interface DashboardData {
  user: User
  diagnostic: null | {
    suggested_unit: CourseSummary
    created_at: string
  }
  text_review: null | {
    possible_signals: boolean
    attention_level: 'low' | 'moderate' | 'high'
    created_at: string
  }
  course: {
    completed: number
    total: number
    percentage: number
  }
}
