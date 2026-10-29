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

from .dataset import load_dataset_provenance, load_training_dataset
from .preprocessing import normalize_spanish_text


MODEL_VERSION = "spanish-text-review-v2"
RANDOM_STATE = 20261029
POSITIVE_LABEL = "attention"


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


def train_and_save_classifier(model_path=None):
    target_path = model_path or settings.TEXT_REVIEW_MODEL_PATH
    dataset = load_training_dataset()
    provenance = load_dataset_provenance()
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        dataset.texts,
        dataset.labels,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=dataset.labels,
    )

    evaluations = {}
    candidates = _candidate_models()
    for name, candidate in candidates.items():
        candidate.fit(train_texts, train_labels)
        evaluations[name] = _metrics(test_labels, candidate.predict(test_texts))

    selected_name = max(
        evaluations,
        key=lambda name: (
            evaluations[name]["f1"],
            evaluations[name]["recall"],
            evaluations[name]["accuracy"],
        ),
    )
    selected_model = candidates[selected_name]
    selected_model.fit(dataset.texts, dataset.labels)
    artifact = {
        "model": selected_model,
        "version": MODEL_VERSION,
        "selected_algorithm": selected_name,
        "evaluations": evaluations,
        "class_order": list(selected_model.classes_),
        "dataset_fingerprint": dataset.fingerprint,
        "dataset_size": len(dataset.texts),
        "dataset_source_sizes": dataset.source_sizes,
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

