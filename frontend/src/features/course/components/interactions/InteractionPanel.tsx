import type { InteractionResponse, LearningItem } from '../../types'
import { ChecklistInteraction } from './ChecklistInteraction'
import { ChoiceInteraction } from './ChoiceInteraction'
import { GuidedExploration } from './GuidedExploration'
import { VideoExperience } from './VideoExperience'

interface InteractionPanelProps {
  lesson: LearningItem
  response: InteractionResponse
  feedback?: string
  saving: boolean
  onResponseChange: (response: InteractionResponse) => void
  onCompletion: (completed: boolean) => Promise<void>
}

export function InteractionPanel({
  lesson,
  response,
  feedback,
  saving,
  onResponseChange,
  onCompletion,
}: InteractionPanelProps) {
  const config = lesson.interaction_config

  if (lesson.interaction_type === 'video') {
    return (
      <VideoExperience
        lessonId={lesson.id}
        checkpointPrompt={lesson.interaction_prompt}
        config={config}
        selectedOption={response.selected_option}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        onSelect={(selectedOption) => onResponseChange({ selected_option: selectedOption })}
        onCompletion={onCompletion}
      />
    )
  }

  if (lesson.interaction_type === 'guided') {
    return (
      <GuidedExploration
        cards={config.cards ?? []}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        onCompletion={onCompletion}
      />
    )
  }

  if (lesson.interaction_type === 'decision' || lesson.interaction_type === 'practice') {
    return (
      <ChoiceInteraction
        lessonId={lesson.id}
        options={config.options ?? []}
        selectedOption={response.selected_option}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        actionLabel={lesson.interaction_type === 'practice' ? 'Practicar respuesta' : 'Confirmar decisión'}
        onSelect={(selectedOption) => onResponseChange({ selected_option: selectedOption })}
        onCompletion={onCompletion}
      />
    )
  }

  return (
    <ChecklistInteraction
      items={config.items ?? []}
      selectedItems={response.selected_items ?? []}
      completed={lesson.completed}
      feedback={feedback}
      privacyNote={config.privacy_note}
      saving={saving}
      actionLabel={lesson.interaction_type === 'safety_plan' ? 'Guardar plan seguro' : 'Completar revisión'}
      onChange={(selectedItems) => onResponseChange({ selected_items: selectedItems })}
      onCompletion={onCompletion}
    />
  )
}
