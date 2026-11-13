import type { InteractionType } from '../types'

export type PuzzleKind = Exclude<InteractionType, 'video'>

export interface CoursePuzzleVisual {
  src: string
  alt: string
  videoCue: string
}

interface CourseVisualIdentity {
  folder: string
  subject: string
  videoCue: string
}

const COURSE_VISUAL_IDENTITIES: Record<string, CourseVisualIdentity> = {
  'acoso-vertical': {
    folder: 'authority',
    subject: 'límites, apoyo y decisiones ante relaciones de autoridad',
    videoCue: 'Distingue una orientación respetuosa de una conducta que reduce la participación o el control.',
  },
  'acoso-horizontal': {
    folder: 'peers',
    subject: 'presión de grupo, apoyo privado y participación entre pares',
    videoCue: 'Observa cómo reenviar, participar o guardar silencio cambia el efecto de una acción grupal.',
  },
  'acoso-tecnologico': {
    folder: 'digital-safety',
    subject: 'privacidad, consentimiento y recuperación del control digital',
    videoCue: 'Antes de publicar o reenviar, comprueba el consentimiento, el alcance y las opciones de apoyo.',
  },
  'acoso-vulnerabilidad': {
    folder: 'diversity',
    subject: 'trato digno, diversidad y participación inclusiva',
    videoCue: 'Mira la conducta y su efecto: apoyar también significa no decidir ni hablar por otra persona.',
  },
  'fundamentos-preventivos': {
    folder: 'prevention',
    subject: 'acuerdos, límites y autocuidado preventivo',
    videoCue: 'Relaciona los acuerdos cotidianos con una convivencia más clara, segura y respetuosa.',
  },
}

const VISUAL_DESCRIPTION: Record<PuzzleKind, string> = {
  guided: 'Ilustración que se reconstruye como un mosaico visual',
  decision: 'Mapa ilustrado con varios caminos posibles',
  matching: 'Mesa visual con señales que deben conectarse',
  practice: 'Escena ilustrada para construir una respuesta',
  safety_plan: 'Ruta ilustrada que debe ordenarse paso a paso',
}

const FILE_NAME_BY_KIND: Record<PuzzleKind, string> = {
  guided: '',
  decision: 'decision',
  matching: 'matching',
  practice: 'dialogue',
  safety_plan: 'sequence',
}

const FALLBACK_IDENTITY = COURSE_VISUAL_IDENTITIES['fundamentos-preventivos']

export function getCoursePuzzleVisual(
  unitSlug: string,
  kind: PuzzleKind,
): CoursePuzzleVisual {
  const identity = COURSE_VISUAL_IDENTITIES[unitSlug] ?? FALLBACK_IDENTITY
  const fileName = kind === 'guided'
    ? `/assets/course-puzzles/${identity.folder}-v2.jpg`
    : `/assets/course-puzzles/${identity.folder}/${FILE_NAME_BY_KIND[kind]}-v2.jpg`

  return {
    src: fileName,
    alt: `${VISUAL_DESCRIPTION[kind]} sobre ${identity.subject}.`,
    videoCue: identity.videoCue,
  }
}
