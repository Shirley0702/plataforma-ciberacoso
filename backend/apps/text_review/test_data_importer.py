import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

from .ml.data_importer import (
    HARM_QUESTION,
    PII_QUESTION,
    import_clandestino_dataset,
)


def _record(sentence, harm_score, *, ai_generated=False, pii="No"):
    return {
        "Sentence": sentence,
        "IsAIGenerated": str(ai_generated),
        "Annotators": [
            {
                HARM_QUESTION: harm_score,
                PII_QUESTION: pii,
            }
        ],
    }


class ClandestinoImporterTests(SimpleTestCase):
    def test_import_keeps_only_human_non_identifiable_balanced_examples(self):
        records = [
            _record(
                "@persona te escribiré al 099 123 4567, revisa https://ejemplo.test",
                5,
            ),
            _record("La conversación fue respetuosa y terminó con un acuerdo", 1),
            _record("Texto generado por una herramienta", 5, ai_generated=True),
            _record("El registro menciona información privada", 5, pii="Yes"),
        ]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "source.jsonl"
            output_path = root / "training.csv"
            metadata_path = root / "metadata.json"
            source_path.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records),
                encoding="utf-8",
            )

            metadata = import_clandestino_dataset(
                source_path,
                output_path,
                metadata_path,
                minimum_examples_per_class=1,
                max_examples_per_class=10,
            )

            with output_path.open(encoding="utf-8", newline="") as source:
                rows = list(csv.DictReader(source))
            self.assertEqual(len(rows), 2)
            self.assertEqual({row["label"] for row in rows}, {"attention", "neutral"})
            combined_text = " ".join(row["text"] for row in rows)
            self.assertNotIn("@persona", combined_text)
            self.assertNotIn("https://", combined_text)
            self.assertNotIn("099 123 4567", combined_text)
            self.assertIn("usuario", combined_text)
            self.assertIn("telefono", combined_text)
            self.assertEqual(metadata["statistics"]["excluded_ai"], 1)
            self.assertEqual(metadata["statistics"]["excluded_pii"], 1)
