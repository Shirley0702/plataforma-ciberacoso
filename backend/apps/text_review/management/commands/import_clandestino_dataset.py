from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.text_review.ml.data_importer import import_clandestino_dataset


class Command(BaseCommand):
    help = "Importa, anonimiza y balancea el corpus CLANDESTINO para entrenamiento."

    def add_arguments(self, parser):
        parser.add_argument("source", type=Path)
        parser.add_argument("--output", type=Path, required=True)
        parser.add_argument("--metadata", type=Path, required=True)

    def handle(self, *args, **options):
        source = options["source"]
        if not source.is_file():
            raise CommandError(f"No existe el archivo de origen: {source}")
        try:
            metadata = import_clandestino_dataset(
                source,
                options["output"],
                options["metadata"],
            )
        except ValueError as error:
            raise CommandError(str(error)) from error
        statistics = metadata["statistics"]
        total = statistics["exported_per_class"] * 2
        self.stdout.write(
            self.style.SUCCESS(
                f"Corpus importado: {total} ejemplos anonimizados y balanceados."
            )
        )
