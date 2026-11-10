export const COURSE_THEME_BY_SLUG: Record<string, string> = {
  'acoso-vertical': 'course-theme-authority',
  'acoso-horizontal': 'course-theme-peers',
  'acoso-tecnologico': 'course-theme-digital',
  'acoso-vulnerabilidad': 'course-theme-diversity',
  'fundamentos-preventivos': 'course-theme-prevention',
}

export function getCourseThemeClass(slug?: string) {
  return slug ? COURSE_THEME_BY_SLUG[slug] ?? '' : ''
}
