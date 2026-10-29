import csv
import hashlib
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from .preprocessing import normalize_spanish_text


HARM_QUESTION = "Question 1: In your opinion, will this text be harmful to anyone?"
PII_QUESTION = "Question 7: Does this sentence contain personally-identifiable information?"
SOURCE_NAME = "CLANDESTINO"
SOURCE_VERSION = "0.0.1"
SOURCE_URL = "https://github.com/microsoft/Clandestino"
SOURCE_LICENSE = "MIT"
MAX_EXAMPLES_PER_CLASS = 5000


@dataclass
class ImportStatistics:
    source_records: int = 0
    human_records: int = 0
    excluded_ai: int = 0
    excluded_pii: int = 0
    excluded_ambiguous: int = 0
    excluded_invalid: int = 0
    excluded_duplicate: int = 0
    attention_candidates: int = 0
    neutral_candidates: int = 0
    exported_per_class: int = 0


def _is_human_generated(record):
    value = record.get("IsAIGenerated", False)
    if isinstance(value, bool):
        return not value
    return str(value).strip().lower() == "false"


def _has_no_personal_information(annotations):
    answers = [
        str(annotation.get(PII_QUESTION, "")).strip().lower()
        for annotation in annotations
    ]
    return bool(answers) and all(answer == "no" for answer in answers)


def _binary_label(annotations):
    scores = []
    for annotation in annotations:
        try:
            scores.append(float(annotation[HARM_QUESTION]))
        except (KeyError, TypeError, ValueError):
            return None
    average = sum(scores) / len(scores) if scores else 0
    if average >= 3.5:
        return "attention"
    if average <= 2.0:
        return "neutral"
    return None


def _source_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_order(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def import_clandestino_dataset(
    source_path,
    output_path,
    metadata_path,
    *,
    minimum_examples_per_class=100,
    max_examples_per_class=MAX_EXAMPLES_PER_CLASS,
):
    source_path = Path(source_path)
    output_path = Path(output_path)
    metadata_path = Path(metadata_path)
    statistics = ImportStatistics()
    examples = defaultdict(dict)

    with source_path.open(encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            statistics.source_records += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                statistics.excluded_invalid += 1
                continue
            if not _is_human_generated(record):
                statistics.excluded_ai += 1
                continue
            statistics.human_records += 1
            annotations = record.get("Annotators") or []
            if not _has_no_personal_information(annotations):
                statistics.excluded_pii += 1
                continue
            label = _binary_label(annotations)
            if label is None:
                statistics.excluded_ambiguous += 1
                continue
            text = normalize_spanish_text(str(record.get("Sentence", "")))
            if len(text) < 15:
                statistics.excluded_invalid += 1
                continue
            other_label = "neutral" if label == "attention" else "attention"
            if text in examples[other_label]:
                statistics.excluded_duplicate += 1
                continue
            examples[label][text] = None

    statistics.attention_candidates = len(examples["attention"])
    statistics.neutral_candidates = len(examples["neutral"])
    balanced_size = min(
        statistics.attention_candidates,
        statistics.neutral_candidates,
        max_examples_per_class,
    )
    if balanced_size < minimum_examples_per_class:
        raise ValueError("El corpus no contiene suficientes ejemplos seguros por clase.")
    statistics.exported_per_class = balanced_size

    selected = []
    for label in ("attention", "neutral"):
        ordered_texts = sorted(examples[label], key=_stable_order)[:balanced_size]
        selected.extend((text, label) for text in ordered_texts)
    selected.sort(key=lambda item: _stable_order(f"{item[1]}:{item[0]}"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(("text", "label"))
        writer.writerows(selected)

    metadata = {
        "source": {
            "name": SOURCE_NAME,
            "version": SOURCE_VERSION,
            "url": SOURCE_URL,
            "license": SOURCE_LICENSE,
            "license_file": "clandestino_license.txt",
            "sha256": _source_sha256(source_path),
        },
        "generated_at": datetime.now(UTC).isoformat(),
        "filters": {
            "human_generated_only": True,
            "personal_information_rule": "all_annotators_must_answer_no",
            "attention_mean_harm_score": ">=3.5",
            "neutral_mean_harm_score": "<=2.0",
            "ambiguous_scores": "excluded",
            "anonymization": ["mentions", "emails", "urls", "phone_numbers"],
            "class_balancing": True,
        },
        "statistics": asdict(statistics),
    }
    with metadata_path.open("w", encoding="utf-8") as target:
        json.dump(metadata, target, ensure_ascii=False, indent=2)
        target.write("\n")
    return metadata

