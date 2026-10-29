interface DiagnosticDraft {
  answers: Record<number, number>
  currentIndex: number
}

const STORAGE_KEY = 'cibersegura_diagnostic_draft'
const EMPTY_DRAFT: DiagnosticDraft = { answers: {}, currentIndex: 0 }


export const diagnosticDraftStorage = {
  load(): DiagnosticDraft {
    try {
      const rawDraft = sessionStorage.getItem(STORAGE_KEY)
      if (!rawDraft) return EMPTY_DRAFT
      const draft = JSON.parse(rawDraft) as Partial<DiagnosticDraft>
      const answers = Object.entries(draft.answers ?? {}).reduce<Record<number, number>>(
        (validAnswers, [questionId, optionId]) => {
          const numericQuestionId = Number(questionId)
          if (Number.isInteger(numericQuestionId) && Number.isInteger(optionId)) {
            validAnswers[numericQuestionId] = optionId
          }
          return validAnswers
        },
        {},
      )
      return {
        answers,
        currentIndex: Number.isInteger(draft.currentIndex) && Number(draft.currentIndex) >= 0
          ? Number(draft.currentIndex)
          : 0,
      }
    } catch {
      sessionStorage.removeItem(STORAGE_KEY)
      return EMPTY_DRAFT
    }
  },
  save(draft: DiagnosticDraft) {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(draft))
  },
  clear() {
    sessionStorage.removeItem(STORAGE_KEY)
  },
}
