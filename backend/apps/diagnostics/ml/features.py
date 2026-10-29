from collections import defaultdict


CATEGORY_SLUGS = (
    "acoso-vertical",
    "acoso-horizontal",
    "acoso-tecnologico",
    "acoso-vulnerabilidad",
)


def aggregate_option_scores(options):
    scores = defaultdict(int)
    for option in options:
        if option.destination_unit:
            scores[option.destination_unit.slug] += option.weight
    return {slug: scores[slug] for slug in CATEGORY_SLUGS}


def feature_vector(scores):
    return [scores.get(slug, 0) for slug in CATEGORY_SLUGS]
