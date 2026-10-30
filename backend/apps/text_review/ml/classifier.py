from dataclasses import dataclass
from functools import lru_cache

import joblib
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import FeatureUnion, Pipeline

from .analysis import write_eda_report
from .dataset import load_dataset_provenance, load_training_dataset
from .preprocessing import normalize_spanish_text


MODEL_VERSION = "spanish-text-review-v3"
RANDOM_STATE = 20261029
POSITIVE_LABEL = "attention"


@dataclass(frozen=True)
class DatasetSplit:
    train_texts: list[str]
    train_labels: list[str]
    validation_texts: list[str]
    validation_labels: list[str]
    test_texts: list[str]
    test_labels: list[str]


def _pipeline(classifier):
    return Pipeline(
        [
            (
                "features",
                FeatureUnion(
                    [
                        (
                            "words",
                            TfidfVectorizer(
                                preprocessor=normalize_spanish_text,
                                lowercase=False,
                                ngram_range=(1, 2),
                                sublinear_tf=True,
                                max_features=10000,
                            ),
                        ),
                        (
                            "characters",
                            TfidfVectorizer(
                                preprocessor=normalize_spanish_text,
                                lowercase=False,
                                analyzer="char_wb",
                                ngram_range=(3, 5),
                                min_df=2,
                                sublinear_tf=True,
                                max_features=12000,
                            ),
                        ),
                    ]
                ),
            ),
            ("classifier", classifier),
        ]
    )


def _candidate_models():
    return {
        "logistic_regression": _pipeline(
            LogisticRegression(
                class_weight="balanced",
                max_iter=2500,
                random_state=RANDOM_STATE,
            )
        ),
        "complement_naive_bayes": _pipeline(ComplementNB(alpha=0.6)),
        "sgd_logistic": _pipeline(
            SGDClassifier(
                loss="log_loss",
                class_weight="balanced",
                max_iter=2500,
                random_state=RANDOM_STATE,
                tol=1e-4,
            )
        ),
    }


def _metrics(expected, predicted):
    return {
        "accuracy": float(accuracy_score(expected, predicted)),
        "precision": float(
            precision_score(expected, predicted, pos_label=POSITIVE_LABEL, zero_division=0)
        ),
        "recall": float(
            recall_score(expected, predicted, pos_label=POSITIVE_LABEL, zero_division=0)
        ),
        "f1": float(f1_score(expected, predicted, pos_label=POSITIVE_LABEL, zero_division=0)),
        "confusion_matrix": confusion_matrix(
            expected,
            predicted,
            labels=["neutral", POSITIVE_LABEL],
        ).tolist(),
    }


def _select(items, indexes):
    return [items[index] for index in indexes]


def split_dataset(dataset) -> DatasetSplit:
    indexes = list(range(len(dataset.texts)))
    train_indexes, holdout_indexes = train_test_split(
        indexes,
        test_size=0.40,
        random_state=RANDOM_STATE,
        stratify=dataset.labels,
    )
    holdout_labels = _select(dataset.labels, holdout_indexes)
    validation_indexes, test_indexes = train_test_split(
        holdout_indexes,
        test_size=0.50,
        random_state=RANDOM_STATE,
        stratify=holdout_labels,
    )
    return DatasetSplit(
        train_texts=_select(dataset.texts, train_indexes),
        train_labels=_select(dataset.labels, train_indexes),
        validation_texts=_select(dataset.texts, validation_indexes),
        validation_labels=_select(dataset.labels, validation_indexes),
        test_texts=_select(dataset.texts, test_indexes),
        test_labels=_select(dataset.labels, test_indexes),
    )


def train_and_save_classifier(model_path=None):
    target_path = model_path or settings.TEXT_REVIEW_MODEL_PATH
    dataset = load_training_dataset()
    provenance = load_dataset_provenance()
    eda_report = write_eda_report(dataset)
    split = split_dataset(dataset)

    validation_evaluations = {}
    candidates = _candidate_models()
    for name, candidate in candidates.items():
        candidate.fit(split.train_texts, split.train_labels)
        validation_evaluations[name] = _metrics(
            split.validation_labels,
            candidate.predict(split.validation_texts),
        )

    selected_name = max(
        validation_evaluations,
        key=lambda name: (
            validation_evaluations[name]["f1"],
            validation_evaluations[name]["recall"],
            validation_evaluations[name]["accuracy"],
        ),
    )
    selected_model = candidates[selected_name]
    development_texts = split.train_texts + split.validation_texts
    development_labels = split.train_labels + split.validation_labels
    selected_model.fit(development_texts, development_labels)
    test_metrics = _metrics(
        split.test_labels,
        selected_model.predict(split.test_texts),
    )
    artifact = {
        "model": selected_model,
        "version": MODEL_VERSION,
        "selected_algorithm": selected_name,
        "selection_metric": "validation_f1",
        "validation_evaluations": validation_evaluations,
        "test_metrics": test_metrics,
        "split_sizes": {
            "train": len(split.train_texts),
            "validation": len(split.validation_texts),
            "test": len(split.test_texts),
        },
        "class_order": list(selected_model.classes_),
        "dataset_fingerprint": dataset.fingerprint,
        "dataset_size": len(dataset.texts),
        "dataset_source_sizes": dataset.source_sizes,
        "eda_summary": eda_report,
        "training_source": provenance["source"],
        "supplemental_source": {
            "name": "expert_scenario_examples",
            "purpose": "Cobertura de amenazas indirectas, presión, exposición y repetición.",
            "records": dataset.source_sizes.get("domain_examples.csv", 0),
        },
        "import_statistics": provenance["statistics"],
    }
    target_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, target_path)
    load_classifier.cache_clear()
    return artifact


@lru_cache(maxsize=1)
def load_classifier():
    model_path = settings.TEXT_REVIEW_MODEL_PATH
    dataset = load_training_dataset()
    if not model_path.exists():
        return train_and_save_classifier(model_path)
    artifact = joblib.load(model_path)
    if (
        artifact.get("version") != MODEL_VERSION
        or artifact.get("dataset_fingerprint") != dataset.fingerprint
    ):
        return train_and_save_classifier(model_path)
    return artifact


def classify_text(text: str):
    artifact = load_classifier()
    model = artifact["model"]
    probabilities = model.predict_proba([text])[0]
    probability_by_label = dict(zip(model.classes_, probabilities, strict=True))
    attention_score = float(probability_by_label.get(POSITIVE_LABEL, 0.0))
    return {
        "label": POSITIVE_LABEL if attention_score >= 0.55 else "neutral",
        "attention_score": attention_score,
        "version": artifact["version"],
        "algorithm": artifact["selected_algorithm"],
    }

