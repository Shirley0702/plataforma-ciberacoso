import json
import statistics
from collections import Counter
from pathlib import Path

from .dataset import TextDataset


EDA_REPORT_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "eda_report.json"
)
STOPWORDS = {
    "al",
    "algo",
    "como",
    "con",
    "cuando",
    "de",
    "del",
    "el",
    "ella",
    "en",
    "es",
    "esa",
    "ese",
    "esta",
    "este",
    "la",
    "las",
    "lo",
    "los",
    "me",
    "mi",
    "mis",
    "no",
    "para",
    "pero",
    "por",
    "que",
    "se",
    "si",
    "sin",
    "su",
    "sus",
    "un",
    "una",
    "y",
    "ya",
}


def _percentile(values: list[int], percentile: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def _length_summary(values: list[int]) -> dict[str, float | int]:
    return {
        "minimum": min(values),
        "maximum": max(values),
        "mean": round(statistics.fmean(values), 2),
        "median": round(statistics.median(values), 2),
        "percentile_95": round(_percentile(values, 0.95), 2),
    }


def _top_tokens(texts: list[str], labels: list[str], label: str) -> list[dict]:
    frequencies = Counter(
        token
        for text, current_label in zip(texts, labels, strict=True)
        if current_label == label
        for token in text.split()
        if len(token) >= 3 and token not in STOPWORDS and token.isalpha()
    )
    return [
        {"token": token, "frequency": frequency}
        for token, frequency in frequencies.most_common(20)
    ]


def build_eda_report(dataset: TextDataset) -> dict:
    class_counts = Counter(dataset.labels)
    total = len(dataset.texts)
    character_lengths = [len(text) for text in dataset.texts]
    word_lengths = [len(text.split()) for text in dataset.texts]
    return {
        "dataset_fingerprint": dataset.fingerprint,
        "records": total,
        "source_distribution": dict(sorted(dataset.source_sizes.items())),
        "class_distribution": {
            label: {
                "count": class_counts[label],
                "proportion": round(class_counts[label] / total, 4),
            }
            for label in sorted(class_counts)
        },
        "text_length": {
            "characters": _length_summary(character_lengths),
            "words": _length_summary(word_lengths),
        },
        "quality_checks": {
            "empty_texts": sum(not text.strip() for text in dataset.texts),
            "duplicate_normalized_texts": total - len(set(dataset.texts)),
            "unknown_labels": sorted(set(dataset.labels) - {"attention", "neutral"}),
        },
        "top_tokens_by_class": {
            label: _top_tokens(dataset.texts, dataset.labels, label)
            for label in sorted(class_counts)
        },
    }


def write_eda_report(
    dataset: TextDataset,
    path: Path | None = None,
) -> dict:
    report = build_eda_report(dataset)
    target_path = path or EDA_REPORT_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report
