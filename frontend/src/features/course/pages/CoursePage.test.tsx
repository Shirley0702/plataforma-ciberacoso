import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { InteractionResponse, LearningItem } from '../types'
import { CoursePage } from './CoursePage'

const mocks = vi.hoisted(() => ({
  useCourse: vi.fn(),
  updateCompletion: vi.fn(),
}))

vi.mock('../hooks/useCourse', () => ({ useCourse: mocks.useCourse }))
vi.mock('../components/CourseProgressPanel', () => ({ CourseProgressPanel: () => null }))
vi.mock('../components/CourseSafetyBanner', () => ({ CourseSafetyBanner: () => null }))
vi.mock('../components/ModuleAssessment', () => ({ ModuleAssessment: () => null }))
vi.mock('../components/LearningExperience', () => ({
  LearningExperience: ({
    lesson,
    onCompletion,
  }: {
    lesson: LearningItem
    onCompletion: (
      lesson: LearningItem,
      completed: boolean,
      response?: InteractionResponse,
    ) => Promise<void>
  }) => (
    <section data-testid="current-experience">
      <span>{lesson.title}</span>
      <button type="button" onClick={() => void onCompletion(lesson, true, {})}>
        Completar experiencia actual
      </button>
    </section>
  ),
}))

const firstLesson: LearningItem = {
  id: 1,
  title: 'Primera experiencia',
  summary: 'Primera idea',
  content: 'Contenido',
  interaction_type: 'guided',
  duration_minutes: 5,
  interaction_prompt: 'Resuelve la actividad.',
  interaction_config: { cards: [] },
  interaction_response: {},
  completed: false,
}

const secondLesson: LearningItem = {
  ...firstLesson,
  id: 2,
  title: 'Segunda experiencia',
  completed: true,
}

describe('CoursePage', () => {
  beforeEach(() => {
    mocks.updateCompletion.mockReset()
    mocks.updateCompletion.mockResolvedValue(true)
    mocks.useCourse.mockReturnValue({
      units: [{
        id: 1,
        title: 'Unidad de prueba',
        slug: 'acoso-vertical',
        description: 'Descripción',
        order: 1,
        priority: 1,
        duration_minutes: 20,
        lessons: [firstLesson, secondLesson],
        quiz_unlocked: false,
        quiz_questions: [],
        latest_quiz: null,
        certificate: null,
      }],
      progressPercentage: 50,
      error: '',
      interactionResponses: {},
      setInteractionResponse: vi.fn(),
      interactionFeedback: {},
      quizAnswers: {},
      setQuizAnswers: vi.fn(),
      quizResults: { 1: null },
      savingLessonId: null,
      submittingUnitId: null,
      updateCompletion: mocks.updateCompletion,
      submitQuiz: vi.fn(),
      downloadCertificate: vi.fn(),
    })
  })

  it('permanece en la experiencia completada hasta que el usuario pulse siguiente', async () => {
    const user = userEvent.setup()
    render(<CoursePage />)

    await user.click(await screen.findByRole('button', { name: 'Completar experiencia actual' }))
    await waitFor(() => expect(mocks.updateCompletion).toHaveBeenCalledWith(firstLesson, true, {}))
    expect(screen.getByTestId('current-experience')).toHaveTextContent('Primera experiencia')
    expect(screen.getByTestId('current-experience')).not.toHaveTextContent('Segunda experiencia')
  })
})
