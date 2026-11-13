import { PuzzleIcon } from '../PuzzleIcon'

interface PuzzleGuideProps {
  icon: string
  title: string
  summary: string
  steps: string[]
  completion: string
}

export function PuzzleGuide({
  icon,
  title,
  summary,
  steps,
  completion,
}: PuzzleGuideProps) {
  return (
    <header className="puzzle-guide">
      <div className="puzzle-guide-heading">
        <span className="puzzle-guide-icon"><PuzzleIcon name={icon} size={25} /></span>
        <div>
          <span className="puzzle-guide-label">Cómo resolverlo</span>
          <strong>{title}</strong>
          <p>{summary}</p>
        </div>
      </div>
      <ol className="puzzle-guide-steps">
        {steps.map((step, index) => (
          <li key={step}>
            <span>{index + 1}</span>
            <p>{step}</p>
          </li>
        ))}
      </ol>
      <p className="puzzle-guide-goal">
        <PuzzleIcon name="flag" size={17} />
        <span><strong>Se completa cuando:</strong> {completion}</span>
      </p>
    </header>
  )
}
