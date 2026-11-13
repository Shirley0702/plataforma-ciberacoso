import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'

const applicationStyles = readFileSync(
  resolve(process.cwd(), 'src/shared/styles/application.css'),
  'utf8',
)

describe('escala tipográfica global', () => {
  it('define una sola escala para las pantallas y la reutiliza en el curso', () => {
    expect(applicationStyles).toContain('--type-page-title: 1.75rem;')
    expect(applicationStyles).toContain('--type-section-title: 1.25rem;')
    expect(applicationStyles).toContain('--type-body: .875rem;')
    expect(applicationStyles).toContain('h1 { font-size: var(--type-page-title);')
    expect(applicationStyles).toContain('.btn { border-radius: 12px; font-size: var(--type-button);')
    expect(applicationStyles).toContain('--course-type-page-title: var(--type-page-title);')
    expect(applicationStyles).toContain('--course-type-body: var(--type-body);')
  })

  it('evita tamaños fluidos que rompan la consistencia entre páginas', () => {
    expect(applicationStyles).not.toMatch(/font-size:\s*clamp\(/)
  })
})
