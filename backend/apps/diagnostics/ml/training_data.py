import random

from .features import CATEGORY_SLUGS


RANDOM_SEED = 20261029
SAMPLES_PER_CATEGORY = 500


def build_expert_bootstrap_dataset():
    """Genera patrones reproducibles para arrancar antes de tener datos reales validados."""
    generator = random.Random(RANDOM_SEED)
    features = []
    labels = []
    for target_index, target_slug in enumerate(CATEGORY_SLUGS):
        for _ in range(SAMPLES_PER_CATEGORY):
            target_score = generator.randint(10, 50)
            sample = [generator.randint(0, max(0, target_score - 4)) for _ in CATEGORY_SLUGS]
            sample[target_index] = target_score
            features.append(sample)
            labels.append(target_slug)
    return features, labels
