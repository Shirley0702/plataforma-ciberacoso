from functools import lru_cache

import joblib
from django.conf import settings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .features import CATEGORY_SLUGS, feature_vector
from .training_data import RANDOM_SEED, build_expert_bootstrap_dataset


MODEL_VERSION = "route-logistic-regression-v1"


def train_and_save_model(model_path=None):
    target_path = model_path or settings.DIAGNOSTIC_MODEL_PATH
    features, labels = build_expert_bootstrap_dataset()
    train_features, test_features, train_labels, test_labels = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=RANDOM_SEED,
        stratify=labels,
    )
    pipeline = Pipeline(
        [
            ("scale", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )
    pipeline.fit(train_features, train_labels)
    accuracy = accuracy_score(test_labels, pipeline.predict(test_features))
    artifact = {
        "model": pipeline,
        "version": MODEL_VERSION,
        "categories": CATEGORY_SLUGS,
        "validation_accuracy": float(accuracy),
        "training_source": "expert_bootstrap_synthetic",
    }
    target_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, target_path)
    load_model.cache_clear()
    return artifact


@lru_cache(maxsize=1)
def load_model():
    model_path = settings.DIAGNOSTIC_MODEL_PATH
    if not model_path.exists():
        return train_and_save_model(model_path)
    artifact = joblib.load(model_path)
    if artifact.get("version") != MODEL_VERSION:
        return train_and_save_model(model_path)
    return artifact


def predict_route(scores):
    artifact = load_model()
    model = artifact["model"]
    vector = [feature_vector(scores)]
    predicted_slug = str(model.predict(vector)[0])
    probabilities = model.predict_proba(vector)[0]
    confidence = float(max(probabilities))
    return {
        "slug": predicted_slug,
        "confidence": confidence,
        "version": artifact["version"],
    }
