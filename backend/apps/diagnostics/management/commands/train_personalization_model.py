from django.core.management.base import BaseCommand

from apps.diagnostics.ml.model import train_and_save_model


class Command(BaseCommand):
    help = "Entrena y guarda el modelo de recomendación de rutas educativas."

    def handle(self, *args, **options):
        artifact = train_and_save_model()
        self.stdout.write(
            self.style.SUCCESS(
                "Modelo entrenado: "
                f"{artifact['version']} | "
                f"exactitud de validación sintética={artifact['validation_accuracy']:.3f}"
            )
        )
