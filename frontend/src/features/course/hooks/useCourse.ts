import { useCallback, useEffect, useMemo, useState } from 'react'
import { api, getErrorMessage } from '../../../shared/api/httpClient'
import type { CourseUnit, LearningItem, QuizResult } from '../types'

export function useCourse() {
  const [units, setUnits] = useState<CourseUnit[]>([])
  const [openLessonId, setOpenLessonId] = useState<number | null>(null)
  const [activityChoices, setActivityChoices] = useState<Record<number, string>>({})
  const [activityFeedback, setActivityFeedback] = useState<Record<number, string>>({})
  const [quizAnswers, setQuizAnswers] = useState<Record<number, number>>({})
  const [quizResults, setQuizResults] = useState<Record<number, QuizResult | null>>({})
  const [error, setError] = useState('')
  const [savingLessonId, setSavingLessonId] = useState<number | null>(null)
  const [submittingUnitId, setSubmittingUnitId] = useState<number | null>(null)

  const loadCourse = useCallback(async () => {
    try {
      const { data } = await api.get<CourseUnit[]>('/courses/units/')
      setUnits(data)
      setQuizResults(Object.fromEntries(
        data.map((unit) => [unit.id, unit.latest_quiz]),
      ))
      setOpenLessonId((current) => (
        current
        ?? data.flatMap((unit) => unit.lessons).find((lesson) => !lesson.completed)?.id
        ?? data[0]?.lessons[0]?.id
        ?? null
      ))
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }, [])

  useEffect(() => {
    void loadCourse()
  }, [loadCourse])

  const progress = useMemo(() => {
    const lessons = units.flatMap((unit) => unit.lessons)
    const completed = lessons.filter((lesson) => lesson.completed).length
    const percentage = lessons.length ? Math.round(completed / lessons.length * 100) : 0
    return { completed, total: lessons.length, percentage }
  }, [units])

  const updateCompletion = async (lesson: LearningItem, completed: boolean) => {
    setSavingLessonId(lesson.id)
    setError('')
    try {
      const payload: { completed: boolean; activity_choice?: string } = { completed }
      if (lesson.kind === 'activity' && completed) {
        payload.activity_choice = activityChoices[lesson.id]
      }
      const { data } = await api.post<{ feedback?: string }>(
        `/courses/lessons/${lesson.id}/complete/`,
        payload,
      )
      if (data.feedback) {
        setActivityFeedback((current) => ({
          ...current,
          [lesson.id]: data.feedback ?? '',
        }))
      }
      await loadCourse()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSavingLessonId(null)
    }
  }

  const submitQuiz = async (unit: CourseUnit) => {
    const hasUnansweredQuestion = unit.quiz_questions.some(
      (question) => !quizAnswers[question.id],
    )
    if (hasUnansweredQuestion) {
      setError('Responde todas las preguntas del cuestionario antes de enviarlo.')
      return
    }
    setSubmittingUnitId(unit.id)
    setError('')
    try {
      const { data } = await api.post<QuizResult>('/courses/quiz/submit/', {
        unit_id: unit.id,
        answers: unit.quiz_questions.map((question) => ({
          question_id: question.id,
          option_id: quizAnswers[question.id],
        })),
      })
      setQuizResults((current) => ({ ...current, [unit.id]: data }))
      await loadCourse()
      document.getElementById(`resultado-cuestionario-${unit.id}`)?.scrollIntoView({
        behavior: 'smooth',
      })
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmittingUnitId(null)
    }
  }

  const downloadCertificate = async (unit: CourseUnit) => {
    if (!unit.certificate) return
    try {
      const response = await api.get(unit.certificate.download_url, { responseType: 'blob' })
      const downloadUrl = URL.createObjectURL(response.data)
      const anchor = document.createElement('a')
      anchor.href = downloadUrl
      anchor.download = `certificado-${unit.certificate.verification_code}.pdf`
      anchor.click()
      URL.revokeObjectURL(downloadUrl)
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }

  return {
    units,
    progress,
    error,
    openLessonId,
    setOpenLessonId,
    activityChoices,
    setActivityChoices,
    activityFeedback,
    quizAnswers,
    setQuizAnswers,
    quizResults,
    savingLessonId,
    submittingUnitId,
    updateCompletion,
    submitQuiz,
    downloadCertificate,
  }
}
