import { useState, type InputHTMLAttributes, type KeyboardEvent, type PointerEvent } from 'react'


type PasswordInputProps = Omit<InputHTMLAttributes<HTMLInputElement>, 'type'>

const REVEAL_KEYS = new Set(['Enter', ' '])


export function PasswordInput({ id, className = '', ...inputProps }: PasswordInputProps) {
  const [isVisible, setIsVisible] = useState(false)

  const reveal = (event: PointerEvent<HTMLButtonElement>) => {
    if (event.button === 0) setIsVisible(true)
  }

  const revealWithKeyboard = (event: KeyboardEvent<HTMLButtonElement>) => {
    if (REVEAL_KEYS.has(event.key)) setIsVisible(true)
  }

  const hideWithKeyboard = (event: KeyboardEvent<HTMLButtonElement>) => {
    if (REVEAL_KEYS.has(event.key)) setIsVisible(false)
  }

  return (
    <div className="input-group password-input">
      <input
        {...inputProps}
        id={id}
        className={className}
        type={isVisible ? 'text' : 'password'}
      />
      <button
        className="btn password-visibility-button"
        type="button"
        aria-label={isVisible ? 'Suelta para ocultar la contraseña' : 'Mantén presionado para ver la contraseña'}
        aria-controls={id}
        aria-pressed={isVisible}
        title="Mantén presionado para ver la contraseña"
        onPointerDown={reveal}
        onPointerUp={() => setIsVisible(false)}
        onPointerLeave={() => setIsVisible(false)}
        onPointerCancel={() => setIsVisible(false)}
        onKeyDown={revealWithKeyboard}
        onKeyUp={hideWithKeyboard}
        onBlur={() => setIsVisible(false)}
      >
        {isVisible ? <EyeOffIcon /> : <EyeIcon />}
      </button>
    </div>
  )
}


function EyeIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  )
}


function EyeOffIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="m3 3 18 18" />
      <path d="M10.6 6.2A9.8 9.8 0 0 1 12 6c6.5 0 10 6 10 6a17 17 0 0 1-2.1 2.8M6.2 6.2C3.5 8 2 12 2 12s3.5 6 10 6c1.8 0 3.3-.5 4.6-1.2" />
      <path d="M10.1 10.1a3 3 0 0 0 3.8 3.8" />
    </svg>
  )
}
