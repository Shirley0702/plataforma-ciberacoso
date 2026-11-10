import type { InteractionResponse, LearningItem } from '../../types'
import { ConsequencePuzzle } from './ConsequencePuzzle'
import { GuidedExploration } from './GuidedExploration'
import { MatchingPuzzle } from './MatchingPuzzle'
import { SafetyKitBuilder } from './SafetyKitBuilder'
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
        viewingPrompt={lesson.interaction_prompt}
        config={config}
        watched={response.watched ?? false}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        onWatchedChange={(watched) => onResponseChange({ watched })}
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
      <ConsequencePuzzle
        options={config.options ?? []}
        exploredOptionIds={response.selected_items ?? []}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        actionLabel={lesson.interaction_type === 'practice' ? 'Completar laboratorio' : 'Guardar lo descubierto'}
        onChange={(selectedItems) => onResponseChange({ selected_items: selectedItems })}
        onCompletion={onCompletion}
      />
    )
  }

  if (lesson.interaction_type === 'matching') {
    return (
      <MatchingPuzzle
        items={config.items ?? []}
        matches={response.matches ?? {}}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        onChange={(matches) => onResponseChange({ matches })}
        onCompletion={onCompletion}
      />
    )
  }

  return (
    <SafetyKitBuilder
      items={config.items ?? []}
      selectedItems={response.selected_items ?? []}
      completed={lesson.completed}
      feedback={feedback}
      privacyNote={config.privacy_note}
      saving={saving}
      onChange={(selectedItems) => onResponseChange({ selected_items: selectedItems })}
      onCompletion={onCompletion}
    />
  )
}
