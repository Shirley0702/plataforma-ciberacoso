import type { CourseSummary } from '../../shared/types/courseSummary'

export interface TextReviewResult {
  result_id: number
  possible_signals: boolean
  attention_level: 'low' | 'moderate' | 'high'
  title: string
  guidance: string
  recommendations: string[]
  recommended_unit: CourseSummary | null
  created_at: string
  privacy_notice: string
}

