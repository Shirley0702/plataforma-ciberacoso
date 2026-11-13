import type { InteractionResponse, LearningItem } from '../../types'
import { getCoursePuzzleVisual } from '../../config/coursePuzzleVisuals'
import { DecisionMapPuzzle } from './DecisionMapPuzzle'
import { DialogueBuilderPuzzle } from './DialogueBuilderPuzzle'
import { GuidedExploration } from './GuidedExploration'
import { MatchingPuzzle } from './MatchingPuzzle'
import { OrderingPuzzle } from './OrderingPuzzle'
import { VideoExperience } from './VideoExperience'

interface InteractionPanelProps {
  lesson: LearningItem
  unitSlug: string
  response: InteractionResponse
  feedback?: string
  saving: boolean
  onResponseChange: (response: InteractionResponse) => void
  onCompletion: (
    completed: boolean,
    responseOverride?: InteractionResponse,
  ) => Promise<void>
}

export function InteractionPanel({
  lesson,
  unitSlug,
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
    const visual = getCoursePuzzleVisual(unitSlug, 'guided')
    return (
      <GuidedExploration
        cards={config.cards ?? []}
        prompt={lesson.interaction_prompt}
        visual={visual}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        onCompletion={onCompletion}
      />
    )
  }

  if (lesson.interaction_type === 'decision') {
    const visual = getCoursePuzzleVisual(unitSlug, 'decision')
    return (
      <DecisionMapPuzzle
        options={config.options ?? []}
        exploredOptionIds={response.selected_items ?? []}
        chosenOptionId={response.chosen_option}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        prompt={lesson.interaction_prompt}
        visual={visual}
        onChange={(selectedItems, chosenOption) => onResponseChange({
          selected_items: selectedItems,
          chosen_option: chosenOption,
        })}
        onCompletion={onCompletion}
      />
    )
  }

  if (lesson.interaction_type === 'practice') {
    const visual = getCoursePuzzleVisual(unitSlug, 'practice')
    return (
      <DialogueBuilderPuzzle
        options={config.options ?? []}
        exploredOptionIds={response.selected_items ?? []}
        chosenOptionId={response.chosen_option}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        prompt={lesson.interaction_prompt}
        visual={visual}
        onChange={(selectedItems, chosenOption) => onResponseChange({
          selected_items: selectedItems,
          chosen_option: chosenOption,
        })}
        onCompletion={onCompletion}
      />
    )
  }

  if (lesson.interaction_type === 'matching') {
    const visual = getCoursePuzzleVisual(unitSlug, 'matching')
    return (
      <MatchingPuzzle
        items={config.items ?? []}
        prompt={lesson.interaction_prompt}
        visual={visual}
        matches={response.matches ?? {}}
        completed={lesson.completed}
        feedback={feedback}
        saving={saving}
        onChange={(matches) => onResponseChange({ matches })}
        onCompletion={onCompletion}
      />
    )
  }

  const visual = getCoursePuzzleVisual(unitSlug, 'safety_plan')
  return (
    <OrderingPuzzle
      items={config.items ?? []}
      prompt={lesson.interaction_prompt}
      visual={visual}
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
