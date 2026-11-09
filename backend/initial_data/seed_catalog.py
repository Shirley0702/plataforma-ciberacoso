import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import CourseUnit, Lesson, ModuleQuizOption, ModuleQuizQuestion
from apps.diagnostics.models import DiagnosticOption, DiagnosticQuestion
from apps.resources.models import OrientationResource
from apps.users.models import UserProfile
from initial_data.catalog.course_units import COURSE_UNITS
from initial_data.catalog.diagnostic_scenarios import DIAGNOSTIC_SCENARIOS


User = get_user_model()


class SeedInitialDataCommand(BaseCommand):
    help = "Crea usuarios y contenidos iniciales idempotentes para la demostración."

    def handle(self, *args, **options):
        self._synchronize_access_accounts()
        self._seed_course()
        self._seed_questions()
        self._seed_resources()
        self.stdout.write(self.style.SUCCESS("Contenidos iniciales listos."))

    def _synchronize_access_accounts(self):
        demo_password = os.getenv("DEMO_USER_PASSWORD")
        admin_password = os.getenv("DEMO_ADMIN_PASSWORD")
        if not demo_password or not admin_password:
            raise CommandError(
                "DEMO_USER_PASSWORD y DEMO_ADMIN_PASSWORD son obligatorias."
            )

        demo, _ = User.objects.get_or_create(
            username="demo", defaults={"email": "demo@cibersegura.local"}
        )
        demo.email = "demo@cibersegura.local"
        demo.is_staff = False
        demo.is_superuser = False
        demo.set_password(demo_password)
        demo.is_active = True
        demo.save()
        demo.groups.clear()
        demo.user_permissions.clear()
        UserProfile.objects.update_or_create(
            user=demo, defaults={"full_name": "Usuario de demostración"}
        )

        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@cibersegura.local",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.email = "admin@cibersegura.local"
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.set_password(admin_password)
        admin.save()
        admin.groups.clear()
        admin.user_permissions.clear()

    def _seed_course(self):
        active_unit_orders = range(1, len(COURSE_UNITS) + 1)
        for unit_order, unit_data in enumerate(COURSE_UNITS, start=1):
            unit, _ = CourseUnit.objects.update_or_create(
                order=unit_order,
                defaults={
                    "slug": unit_data["slug"],
                    "title": unit_data["title"],
                    "description": unit_data["description"],
                    "duration_minutes": unit_data["duration"],
                    "active": True,
                },
            )
            kept_lesson_ids = []
            for lesson_order, item in enumerate(unit_data["learning_items"], start=1):
                lesson, _ = Lesson.objects.update_or_create(
                    unit=unit,
                    order=lesson_order,
                    defaults={
                        "title": item["title"],
                        "summary": item["summary"],
                        "content": item["content"],
                        "interaction_type": item["interaction_type"],
                        "duration_minutes": item["duration"],
                        "interaction_prompt": item["interaction_prompt"],
                        "interaction_config": item["interaction_config"],
                    },
                )
                kept_lesson_ids.append(lesson.id)
            unit.lessons.exclude(id__in=kept_lesson_ids).delete()

        CourseUnit.objects.exclude(order__in=active_unit_orders).update(active=False)
        self._seed_quizzes()

    def _seed_quizzes(self):
        units_by_slug = CourseUnit.objects.filter(active=True).in_bulk(
            field_name="slug"
        )
        for unit_data in COURSE_UNITS:
            unit = units_by_slug[unit_data["slug"]]
            kept_question_ids = []
            for question_order, item in enumerate(unit_data["quiz"], start=1):
                question, _ = ModuleQuizQuestion.objects.update_or_create(
                    unit=unit,
                    order=question_order,
                    defaults={"text": item["text"], "active": True},
                )
                kept_question_ids.append(question.id)
                kept_option_ids = []
                for option_order, label in enumerate(item["options"], start=1):
                    option, _ = ModuleQuizOption.objects.update_or_create(
                        question=question,
                        order=option_order,
                        defaults={
                            "label": label,
                            "is_correct": option_order - 1 == item["correct_index"],
                        },
                    )
                    kept_option_ids.append(option.id)
                question.options.exclude(id__in=kept_option_ids).delete()
            unit.quiz_questions.exclude(id__in=kept_question_ids).update(active=False)

    def _seed_questions(self):
        units = {unit.slug: unit for unit in CourseUnit.objects.filter(active=True)}
        active_orders = range(1, len(DIAGNOSTIC_SCENARIOS) + 1)
        DiagnosticQuestion.objects.exclude(order__in=active_orders).update(active=False)
        for order, scenario in enumerate(DIAGNOSTIC_SCENARIOS, start=1):
            unit = units[scenario["unit_slug"]]
            question, _ = DiagnosticQuestion.objects.update_or_create(
                order=order,
                defaults={
                    "text": scenario["text"],
                    "primary_unit": unit,
                    "active": True,
                },
            )
            kept_option_ids = []
            for option_order, (label, weight) in enumerate(
                scenario["options"], start=1
            ):
                option, _ = DiagnosticOption.objects.update_or_create(
                    question=question,
                    order=option_order,
                    defaults={
                        "label": label,
                        "destination_unit": unit,
                        "weight": weight,
                    },
                )
                kept_option_ids.append(option.id)
            question.options.exclude(id__in=kept_option_ids).delete()

    def _seed_resources(self):
        resources = [
            {
                "name": "ECU 911",
                "description": "Línea única de emergencias en Ecuador. Úsala ante peligro inmediato o una amenaza a la integridad.",
                "url": "https://www.ecu911.gob.ec/servicio-integrado-de-seguridad-ecu-911/",
                "phone": "9-1-1",
                "emergency": True,
            },
            {
                "name": "Fiscalía General del Estado",
                "description": "Información y formulario oficial para hechos de violencia basada en género; el sitio también orienta sobre atención presencial.",
                "url": "https://www.fiscalia.gob.ec/denuncia-en-linea-de-violencia-basada-en-genero/",
                "phone": "1800-DELITO (335486)",
                "emergency": False,
            },
            {
                "name": "Ministerio de Educación - Protocolos de violencia",
                "description": "Protocolos y rutas de actuación del sistema educativo ecuatoriano frente a situaciones de violencia y riesgo en entornos presenciales o digitales.",
                "url": "https://educacion.gob.ec/wp-content/uploads/downloads/2022/10/Protocolos-situaciones-de-violencia.pdf",
                "phone": "",
                "emergency": False,
            },
        ]
        for order, item in enumerate(resources, start=1):
            OrientationResource.objects.update_or_create(
                name=item["name"],
                defaults={**item, "order": order, "active": True, "country": "Ecuador"},
            )
