from dataclasses import dataclass

from apps.courses.models import CourseUnit

from .ml.preprocessing import normalize_spanish_text


@dataclass(frozen=True)
class ContextPattern:
    key: str
    label: str
    terms: tuple[str, ...]
    recommendation: str


CONTEXT_PATTERNS = (
    ContextPattern(
        key="pressure",
        label="Presión o amenaza",
        terms=("amenaza", "obliga", "presiona", "chantaje", "si no haces"),
        recommendation=(
            "Si existe presión o una amenaza, evita negociar a solas y busca apoyo "
            "antes de responder."
        ),
    ),
    ContextPattern(
        key="privacy",
        label="Privacidad o difusión",
        terms=(
            "foto",
            "captura",
            "publicar",
            "compartir",
            "difundir",
            "privada",
            "contraseña",
        ),
        recommendation=(
            "Revisa la privacidad de tus cuentas, cambia accesos comprometidos y "
            "conserva enlaces o capturas completas sin volver a difundir el contenido."
        ),
    ),
    ContextPattern(
        key="repetition",
        label="Situación repetida",
        terms=(
            "cada día",
            "todos los días",
            "otra vez",
            "continúa",
            "continuan",
            "repite",
            "insiste",
        ),
        recommendation=(
            "Anota fechas y canales para construir una secuencia clara de lo ocurrido."
        ),
    ),
    ContextPattern(
        key="exclusion",
        label="Exclusión o presión grupal",
        terms=("excluir", "dejar fuera", "grupo", "aislar", "novatada"),
        recommendation=(
            "Identifica una persona del entorno académico que pueda acompañarte y "
            "ayudar a detener la exclusión sin exponerte."
        ),
    ),
    ContextPattern(
        key="authority",
        label="Relación de autoridad",
        terms=(
            "profesor",
            "tutor",
            "docente",
            "jefe",
            "calificación",
            "nota",
        ),
        recommendation=(
            "Conserva las instrucciones y comunicaciones académicas, y utiliza un "
            "canal institucional distinto si necesitas acompañamiento."
        ),
    ),
)

ROUTE_RECOMMENDATIONS = {
    "acoso-vertical": (
        "En tu ruta encontrarás formas de documentar límites y pedir acompañamiento "
        "cuando existe una relación de autoridad."
    ),
    "acoso-horizontal": (
        "Tu ruta incluye decisiones para afrontar presión grupal y fortalecer una red "
        "de apoyo entre pares."
    ),
    "acoso-tecnologico": (
        "Tu ruta profundiza en privacidad, evidencia digital y controles de seguridad."
    ),
    "acoso-vulnerabilidad": (
        "Tu ruta trabaja límites, trato digno y búsqueda de apoyo ante sesgos o "
        "comentarios sobre características personales."
    ),
}


def detect_contexts(text: str) -> list[str]:
    normalized_text = normalize_spanish_text(text)
    return [
        pattern.key
        for pattern in CONTEXT_PATTERNS
        if any(term in normalized_text for term in pattern.terms)
    ]


def context_labels(context_keys: list[str]) -> list[str]:
    labels = {pattern.key: pattern.label for pattern in CONTEXT_PATTERNS}
    return [labels[key] for key in context_keys if key in labels]


def build_recommendations(
    *,
    needs_attention: bool,
    attention_level: str,
    context_keys: list[str],
    recommended_unit: CourseUnit | None,
) -> list[str]:
    if needs_attention:
        recommendations = [
            "Conserva el contexto completo, las fechas y los enlaces si hacerlo no aumenta el riesgo.",
            "Comparte la situación con una persona de confianza o con bienestar estudiantil.",
        ]
    else:
        recommendations = [
            "Observa el contexto, la repetición y si la situación cambia después de expresar un límite.",
            "Puedes conservar el mensaje y comentarlo con una persona de confianza aunque no aparezcan señales claras.",
        ]

    if attention_level == "high":
        recommendations.insert(
            0,
            "Prioriza tu seguridad y evita una confrontación directa si la situación puede escalar.",
        )

    recommendations.extend(
        pattern.recommendation
        for pattern in CONTEXT_PATTERNS
        if pattern.key in context_keys
    )
    if recommended_unit:
        recommendations.append(
            ROUTE_RECOMMENDATIONS.get(
                recommended_unit.slug,
                f"Continúa con tu ruta educativa: {recommended_unit.title}.",
            )
        )
    return list(dict.fromkeys(recommendations))
