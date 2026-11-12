import type { InteractionResponse, LearningItem } from '../../types'
import { ConsequencePuzzle } from './ConsequencePuzzle'
import { GuidedExploration } from './GuidedExploration'
import { MatchingPuzzle } from './MatchingPuzzle'
import { OrderingPuzzle } from './OrderingPuzzle'
import { VideoExperience } from './VideoExperience'

interface InteractionPanelProps {
  lesson: LearningItem
  response: InteractionResponse
  feedback?: string
  saving: boolean
  onResponseChange: (response: InteractionResponse) => void
  onCompletion: (
    completed: boolean,
    responseOverride?: InteractionResponse,
    advance?: boolean,
  ) => Promise<void>
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
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
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
        chosenOptionId={response.chosen_option}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        variant={lesson.interaction_type}
        onChange={(selectedItems, chosenOption) => onResponseChange({
          selected_items: selectedItems,
          chosen_option: chosenOption,
        })}
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
    <OrderingPuzzle
      items={config.items ?? []}
      orderedItemIds={response.selected_items ?? []}
      completed={lesson.completed}
      feedback={feedback}
      privacyNote={config.privacy_note}
      saving={saving}
      onChange={(orderedItemIds) => onResponseChange({ selected_items: orderedItemIds })}
      onCompletion={onCompletion}
    />
  )
}
