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
  mosaic: <><rect x="3" y="3" width="8" height="8" rx="1" /><rect x="13" y="3" width="8" height="8" rx="1" /><rect x="3" y="13" width="8" height="8" rx="1" /><rect x="13" y="13" width="8" height="8" rx="1" /></>,
  boundary: <><path d="M12 3v18M5 7h4M5 12h4M5 17h4M15 7h4M15 12h4M15 17h4" /><circle cx="12" cy="12" r="2" /></>,
  shield: <><path d="M12 3 5 6v5c0 4.6 2.6 8 7 10 4.4-2 7-5.4 7-10V6z" /><path d="m9 12 2 2 4-5" /></>,
  broadcast: <><path d="M4 11v2M8 8a6 6 0 0 0 0 8M12 5a10 10 0 0 0 0 14" /><circle cx="4" cy="12" r="1" /></>,
  escalate: <><path d="M5 19 19 5M11 5h8v8" /><path d="M5 8v11h11" /></>,
  person: <><circle cx="12" cy="8" r="3" /><path d="M6 21c.5-5 2.5-7 6-7s5.5 2 6 7" /></>,
  review: <><circle cx="11" cy="11" r="7" /><path d="m16 16 5 5M11 7v5M11 15h.01" /></>,
  spark: <><path d="m12 3 1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5zM18 15l.7 2.3L21 18l-2.3.7L18 21l-.7-2.3L15 18l2.3-.7z" /></>,
  reply: <><path d="m10 7-6 5 6 5v-3h3c3.5 0 5.5 1 7 4-.3-6-3-9-7-9h-3z" /></>,
  sequence: <><circle cx="5" cy="6" r="2" /><circle cx="12" cy="12" r="2" /><circle cx="19" cy="18" r="2" /><path d="m7 7.5 3.5 3M13.5 13.5l3.5 3" /></>,
  repeat: <><path d="M4 7h12a4 4 0 0 1 4 4v1M7 4 4 7l3 3" /><path d="M20 17H8a4 4 0 0 1-4-4v-1M17 20l3-3-3-3" /></>,
  group: <><circle cx="9" cy="8" r="3" /><circle cx="17" cy="9" r="2" /><path d="M3 20c.4-4 2.4-6 6-6s5.6 2 6 6M15 15c3-.3 5 1.4 6 4" /></>,
  balance: <><path d="M12 3v18M5 6h14M7 6l-4 7h8zM17 6l-4 7h8zM8 21h8" /></>,
  opportunity: <><path d="M5 21V4h10l4 4v13zM15 4v5h5" /><path d="M8 14h8M12 10v8" /></>,
  tag: <><path d="M3 12 12 3h7l2 2v7l-9 9z" /><circle cx="17" cy="7" r="1" /></>,
  key: <><circle cx="8" cy="15" r="4" /><path d="m11 12 8-8M16 7l2 2M13 10l2 2" /></>,
  sessions: <><rect x="3" y="5" width="12" height="10" rx="1" /><path d="M7 19h12a2 2 0 0 0 2-2V9M7 15v4M4 19h6" /></>,
  flag: <><path d="M5 3v18M6 5h12l-2.5 4L18 13H6" /></>,
  target: <><circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="4" /><circle cx="12" cy="12" r="1" /></>,
  arrow: <><path d="M4 12h15M14 7l5 5-5 5" /></>,
  outcome: <><path d="M4 5h7v6H4zM13 13h7v6h-7zM11 8h3a3 3 0 0 1 3 3v2" /></>,
  'chevron-left': <path d="m14 7-5 5 5 5" />,
  'chevron-right': <path d="m10 7 5 5-5 5" />,
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
