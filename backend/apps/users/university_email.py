"""Identificación local de dominios pertenecientes a instituciones universitarias."""

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


@dataclass(frozen=True)
class UniversityIdentity:
    name: str
    country: str
    domain: str


def _normalize_domain(domain):
    normalized = domain.strip().lower().rstrip(".")
    try:
        return normalized.encode("idna").decode("ascii")
    except UnicodeError:
        return ""


@lru_cache(maxsize=1)
def university_domains():
    catalog_path = Path(settings.UNIVERSITY_DOMAINS_DATA_FILE)
    try:
        records = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ImproperlyConfigured(
            "No se pudo cargar el catálogo local de dominios universitarios."
        ) from error

    domains = {}
    for record in records:
        for domain in record.get("domains", ()):
            normalized = _normalize_domain(domain)
            if normalized:
                domains[normalized] = UniversityIdentity(
                    name=record.get("name", "Universidad reconocida"),
                    country=record.get("country", ""),
                    domain=normalized,
                )

    for domain in settings.ADDITIONAL_UNIVERSITY_EMAIL_DOMAINS:
        normalized = _normalize_domain(domain)
        if normalized:
            domains[normalized] = UniversityIdentity(
                name="Universidad configurada",
                country="",
                domain=normalized,
            )
    return domains


def find_university(email_domain):
    """Devuelve la institución del dominio exacto o de uno de sus subdominios."""

    normalized = _normalize_domain(email_domain)
    if not normalized:
        return None

    catalog = university_domains()
    labels = normalized.split(".")
    for index in range(len(labels) - 1):
        candidate = ".".join(labels[index:])
        if candidate in catalog:
            return catalog[candidate]
    return None
