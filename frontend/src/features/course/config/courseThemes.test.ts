import { describe, expect, it } from 'vitest'
import { COURSE_THEME_BY_SLUG, getCourseThemeClass } from './courseThemes'

describe('identidad visual de las rutas', () => {
  it('asigna un tema distinto a cada uno de los cinco tipos de curso', () => {
    const expectedThemes = {
      'acoso-vertical': 'course-theme-authority',
      'acoso-horizontal': 'course-theme-peers',
      'acoso-tecnologico': 'course-theme-digital',
      'acoso-vulnerabilidad': 'course-theme-diversity',
      'fundamentos-preventivos': 'course-theme-prevention',
    }
    const themeClasses = Object.values(COURSE_THEME_BY_SLUG)
    expect(themeClasses).toHaveLength(5)
    expect(new Set(themeClasses).size).toBe(5)
    for (const [slug, themeClass] of Object.entries(expectedThemes)) {
      expect(getCourseThemeClass(slug)).toBe(themeClass)
    }
  })
})
