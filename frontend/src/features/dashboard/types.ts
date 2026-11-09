import type { CourseSummary } from '../../shared/types/courseSummary'
import type { User } from '../../shared/types/user'

export interface DashboardData {
  user: User
  diagnostic: null | {
    suggested_unit: CourseSummary
    recommended_units: (CourseSummary & { priority: number })[]
    route_type: 'prioritized' | 'preventive_general'
    dimension_profile: {
      unit_id: number
      title: string
      score: number
      maximum: number
      percentage: number
      priority: number | null
    }[]
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
