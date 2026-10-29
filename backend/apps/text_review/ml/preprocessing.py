import re
import unicodedata


URL_PATTERN = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w.-]+\.\w+\b", re.IGNORECASE)
MENTION_PATTERN = re.compile(r"(?<!\w)@[\w.]+")
PHONE_PATTERN = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")
WHITESPACE_PATTERN = re.compile(r"\s+")
REPEATED_CHARACTER_PATTERN = re.compile(r"(.)\1{3,}", re.IGNORECASE)


def normalize_spanish_text(value: str) -> str:
    """Normaliza ruido común sin eliminar información lingüística relevante."""
    text = unicodedata.normalize("NFKC", value or "").lower().strip()
    text = URL_PATTERN.sub(" enlace ", text)
    text = EMAIL_PATTERN.sub(" correo ", text)
    text = MENTION_PATTERN.sub(" usuario ", text)
    text = PHONE_PATTERN.sub(" telefono ", text)
    text = REPEATED_CHARACTER_PATTERN.sub(r"\1\1\1", text)
    return WHITESPACE_PATTERN.sub(" ", text).strip()

