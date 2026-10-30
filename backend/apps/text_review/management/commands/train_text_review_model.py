from django.core.management.base import BaseCommand

from apps.text_review.ml import train_and_save_classifier


class Command(BaseCommand):
    help = "Entrena, compara y guarda los modelos de clasificación textual."

    def handle(self, *args, **options):
        artifact = train_and_save_classifier()
        metrics = artifact["test_metrics"]
        self.stdout.write(
            self.style.SUCCESS(
                "Clasificador textual entrenado: "
                f"{artifact['selected_algorithm']} | "
                f"F1 de prueba={metrics['f1']:.3f} | "
                f"recall={metrics['recall']:.3f} | "
                f"precision={metrics['precision']:.3f}"
            )
        )
