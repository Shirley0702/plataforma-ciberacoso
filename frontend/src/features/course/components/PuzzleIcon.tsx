import type { ReactNode } from 'react'

interface PuzzleIconProps {
  name?: string
  size?: number
}

const ICON_PATHS: Record<string, ReactNode> = {
  pause: <><path d="M9 7v10M15 7v10" /><circle cx="12" cy="12" r="9" /></>,
  document: <><path d="M7 3h7l4 4v14H7z" /><path d="M14 3v5h5M10 12h5M10 16h5" /></>,
  support: <><path d="M8.5 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM15.5 12a2.5 2.5 0 1 0 0-5" /><path d="M3.5 20c.4-4 2.2-6 5-6s4.6 2 5 6M14 15c3.4-.4 5.5 1.3 6 4" /></>,
  compass: <><circle cx="12" cy="12" r="9" /><path d="m15.5 8.5-2 5-5 2 2-5z" /></>,
  stop: <><path d="M8 4h8l4 4v8l-4 4H8l-4-4V8z" /><path d="M9 9l6 6M15 9l-6 6" /></>,
  chat: <><path d="M4 5h16v11H9l-5 4z" /><path d="M8 9h8M8 12h5" /></>,
  help: <><circle cx="12" cy="12" r="9" /><path d="M9.8 9a2.4 2.4 0 1 1 3.3 2.2c-.9.4-1.1 1-1.1 1.8M12 17h.01" /></>,
  lock: <><rect x="5" y="10" width="14" height="11" rx="2" /><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3" /></>,
  report: <><path d="M6 3v18M7 5h11l-2 4 2 4H7" /></>,
  observe: <><path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" /><circle cx="12" cy="12" r="2.5" /></>,
  university: <><path d="m3 9 9-5 9 5-9 5zM6 12v6M10 14v4M14 14v4M18 12v6M4 20h16" /></>,
  emergency: <><path d="M8 4h8l2 6v10H6V10zM9 4V2h6v2M9 14h6M12 11v6" /></>,
  clue: <><circle cx="11" cy="11" r="6" /><path d="m16 16 5 5M9 11l1.5 1.5L14 9" /></>,
  route: <><circle cx="6" cy="18" r="2" /><circle cx="18" cy="6" r="2" /><path d="M8 18h3a3 3 0 0 0 3-3v-6a3 3 0 0 1 3-3" /></>,
  connect: <><circle cx="6" cy="12" r="3" /><circle cx="18" cy="12" r="3" /><path d="M9 12h6" /></>,
  check: <path d="m5 12 4 4L19 6" />,
  play: <><circle cx="12" cy="12" r="9" /><path d="m10 8 6 4-6 4z" /></>,
  puzzle: <><path d="M4 4h6a2 2 0 1 0 4 0h6v6a2 2 0 1 1 0 4v6h-6a2 2 0 1 0-4 0H4v-6a2 2 0 1 1 0-4z" /></>,
  'chevron-up': <path d="m7 14 5-5 5 5" />,
  'chevron-down': <path d="m7 10 5 5 5-5" />,
}

export function PuzzleIcon({ name = 'clue', size = 28 }: PuzzleIconProps) {
  return (
    <svg
      aria-hidden="true"
      className="puzzle-icon"
      viewBox="0 0 24 24"
      width={size}
      height={size}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {ICON_PATHS[name] ?? ICON_PATHS.clue}
    </svg>
  )
}
