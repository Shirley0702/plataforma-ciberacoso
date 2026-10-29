import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .preprocessing import normalize_spanish_text


DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "training_examples.csv"
DOMAIN_DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "domain_examples.csv"
PROVENANCE_PATH = Path(__file__).resolve().parent.parent / "data" / "dataset_provenance.json"
ALLOWED_LABELS = {"attention", "neutral"}


@dataclass(frozen=True)
class TextDataset:
    texts: list[str]
    labels: list[str]
    fingerprint: str
    source_sizes: dict[str, int]


def load_training_dataset(path: Path | None = None) -> TextDataset:
    rows: dict[str, str] = {}
    source_paths = [path] if path else [DATASET_PATH, DOMAIN_DATASET_PATH]
    source_sizes = {}
    digest = hashlib.sha256()
    for source_path in source_paths:
        source_path = Path(source_path)
        source_count = 0
        digest.update(source_path.name.encode("utf-8"))
        digest.update(source_path.read_bytes())
        with source_path.open(encoding="utf-8", newline="") as source:
            for row in csv.DictReader(source):
                text = normalize_spanish_text(row.get("text", ""))
                label = row.get("label", "").strip().lower()
                if len(text) < 15 or label not in ALLOWED_LABELS:
                    raise ValueError("El conjunto de entrenamiento contiene una fila inválida.")
                if text in rows and rows[text] != label:
                    raise ValueError("Un mismo texto no puede tener etiquetas contradictorias.")
                if text not in rows:
                    source_count += 1
                rows[text] = label
        source_sizes[source_path.name] = source_count

    labels = list(rows.values())
    if len(rows) < 40 or any(labels.count(label) < 15 for label in ALLOWED_LABELS):
        raise ValueError("El conjunto de entrenamiento no tiene cobertura mínima por clase.")

    return TextDataset(list(rows.keys()), labels, digest.hexdigest(), source_sizes)


def load_dataset_provenance(path: Path | None = None):
    source_path = path or PROVENANCE_PATH
    with source_path.open(encoding="utf-8") as source:
        provenance = json.load(source)
    required_source_fields = {"name", "version", "url", "license", "sha256"}
    if not required_source_fields.issubset(provenance.get("source", {})):
        raise ValueError("La procedencia del conjunto de entrenamiento está incompleta.")
    return provenance

