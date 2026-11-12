export interface CoursePuzzleVisual {
  src: string
  alt: string
  videoCue: string
}

const COURSE_PUZZLE_VISUALS: Record<string, CoursePuzzleVisual> = {
  'acoso-vertical': {
    src: '/assets/course-puzzles/authority.jpg',
    alt: 'Estudiante organizando pistas sobre límites, pausa y acompañamiento universitario.',
    videoCue: 'Recuerda cómo el video diferencia una orientación respetuosa de una relación que limita la participación.',
  },
  'acoso-horizontal': {
    src: '/assets/course-puzzles/peers.jpg',
    alt: 'Grupo de estudiantes deteniendo una cadena de mensajes y construyendo apoyo entre compañeros.',
    videoCue: 'Recuerda cómo el video muestra que reenviar, participar o guardar silencio puede sostener la presión del grupo.',
  },
  'acoso-tecnologico': {
    src: '/assets/course-puzzles/digital-safety.jpg',
    alt: 'Estudiante ordenando acciones para detener una difusión, proteger una cuenta y buscar apoyo.',
    videoCue: 'Recuerda la idea central del video: antes de publicar o reenviar, comprueba el consentimiento y el alcance.',
  },
  'acoso-vulnerabilidad': {
    src: '/assets/course-puzzles/diversity.jpg',
    alt: 'Estudiantes diversos construyendo juntos un puzzle de participación e inclusión.',
    videoCue: 'Recuerda cómo el video presenta la diversidad como una parte valiosa de la convivencia y la participación.',
  },
  'fundamentos-preventivos': {
    src: '/assets/course-puzzles/prevention.jpg',
    alt: 'Estudiantes construyendo una ruta visual de acuerdos, límites y apoyo cotidiano.',
    videoCue: 'Recuerda cómo el video relaciona los acuerdos cotidianos con una convivencia más segura y respetuosa.',
  },
}

const FALLBACK_VISUAL = COURSE_PUZZLE_VISUALS['fundamentos-preventivos']

export function getCoursePuzzleVisual(unitSlug: string): CoursePuzzleVisual {
  return COURSE_PUZZLE_VISUALS[unitSlug] ?? FALLBACK_VISUAL
}
