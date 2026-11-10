import { useCallback, useEffect, useMemo, useState } from 'react'
import { api, getErrorMessage } from '../../../shared/api/httpClient'
import type {
  CourseUnit,
  InteractionResponse,
  LearningItem,
  QuizResult,
} from '../types'

export function useCourse() {
  const [units, setUnits] = useState<CourseUnit[]>([])
  const [interactionResponses, setInteractionResponses] = useState<
    Record<number, InteractionResponse>
  >({})
  const [interactionFeedback, setInteractionFeedback] = useState<Record<number, string>>({})
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
      const storedResponses = Object.fromEntries(
        data.flatMap((unit) => unit.lessons).map((lesson) => [
          lesson.id,
          lesson.interaction_response ?? {},
        ]),
      )
      setInteractionResponses((current) => ({ ...storedResponses, ...current }))
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }, [])

  useEffect(() => {
    void loadCourse()
  }, [loadCourse])

  const progressPercentage = useMemo(() => {
    const lessons = units.flatMap((unit) => unit.lessons)
    const completed = lessons.filter((lesson) => lesson.completed).length
    return lessons.length ? Math.round(completed / lessons.length * 100) : 0
  }, [units])

  const setInteractionResponse = (lessonId: number, response: InteractionResponse) => {
    setInteractionResponses((current) => ({ ...current, [lessonId]: response }))
  }

  const updateCompletion = async (
    lesson: LearningItem,
    completed: boolean,
    responseOverride?: InteractionResponse,
  ) => {
    setSavingLessonId(lesson.id)
    setError('')
    try {
      const payload = {
        completed,
        interaction_response: completed
          ? responseOverride ?? interactionResponses[lesson.id] ?? {}
          : {},
      }
      const { data } = await api.post<{ feedback?: string }>(
        `/courses/lessons/${lesson.id}/complete/`,
        payload,
      )
      setInteractionFeedback((current) => ({
        ...current,
        [lesson.id]: data.feedback ?? '',
      }))
      if (!completed) setInteractionResponse(lesson.id, {})
      await loadCourse()
      return true
    } catch (requestError) {
      setError(getErrorMessage(requestError))
      return false
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
      return false
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
      return data.passed
    } catch (requestError) {
      setError(getErrorMessage(requestError))
      return false
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
    progressPercentage,
    error,
    interactionResponses,
    setInteractionResponse,
    interactionFeedback,
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
