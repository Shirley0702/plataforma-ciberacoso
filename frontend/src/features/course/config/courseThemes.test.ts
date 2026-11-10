import { describe, expect, it } from 'vitest'
import { COURSE_THEME_BY_SLUG, getCourseThemeClass } from './courseThemes'

describe('identidad visual de las rutas', () => {
  it('asigna un tema distinto a cada uno de los cinco tipos de curso', () => {
    const themeClasses = Object.values(COURSE_THEME_BY_SLUG)
    expect(themeClasses).toHaveLength(5)
    expect(new Set(themeClasses).size).toBe(5)
    expect(getCourseThemeClass('acoso-tecnologico')).toBe('course-theme-digital')
  })
})
