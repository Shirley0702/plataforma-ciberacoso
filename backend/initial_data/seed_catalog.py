import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import CourseUnit, Lesson, ModuleQuizOption, ModuleQuizQuestion
from apps.diagnostics.models import DiagnosticOption, DiagnosticQuestion
from apps.resources.models import OrientationResource
from apps.users.models import UserProfile


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

    def _seed_questions(self):
        questions = [
            (
                "Cuando los profesores o tutores de tu carrera buscan que los estudiantes alcancen un alto nivel de excelencia, ¿cuál es la dinámica más común en las aulas o laboratorios?",
                "acoso-vertical",
                [
                    ("Se enfocan estrictamente en revisar los datos, la rúbrica y los entregables técnicos de los proyectos.", None, 0),
                    ("Utilizan la presión social o la exposición de los errores individuales frente al grupo como un método para forzarnos a mejorar.", "acoso-vertical", 10),
                    ('Mantienen una distancia absoluta; el estudiante debe resolver todo por su cuenta porque "ya es un adulto".', "acoso-vertical", 5),
                ],
            ),
            (
                "En los proyectos importantes o tesis, ¿cómo se percibe la disponibilidad y el compromiso que un estudiante debe demostrar hacia sus superiores?",
                "acoso-vertical",
                [
                    ("El compromiso se mide entregando los avances acordados dentro de las horas de jornada universitaria.", None, 0),
                    ("Se valora positivamente estar disponible para responder dudas o avanzar trabajo en cualquier momento (noches o fines de semana) si el proyecto lo requiere.", "acoso-vertical", 10),
                ],
            ),
            (
                "En tu facultad, cuando se forman los equipos de trabajo para los proyectos más complejos del semestre, las dinámicas de selección suelen basarse en:",
                "acoso-horizontal",
                [
                    ("Afinidades académicas, habilidades técnicas complementarias o sorteos directos del docente.", None, 0),
                    ("Ciertos grupos o líderes de la clase que deciden de antemano quiénes entran y quiénes quedan rezagados para asegurar sus notas.", "acoso-horizontal", 10),
                    ("Se permite el uso de apodos, sarcasmo o bromas pesadas dentro de los equipos como una forma natural de romper el hielo y liberar el estrés.", "acoso-horizontal", 10),
                ],
            ),
            (
                "Respecto a las tradiciones de bienvenida, novatadas o reuniones sociales organizadas por los alumnos de semestres superiores, la percepción general es que:",
                "acoso-horizontal",
                [
                    ("Son eventos puramente recreativos, opcionales y donde cualquiera se siente cómodo desde el primer minuto.", None, 0),
                    ("Son un filtro necesario; es normal pasar por momentos incómodos o retos pesados para demostrar que tienes el carácter para pertenecer a la facultad.", "acoso-horizontal", 10),
                ],
            ),
            (
                "Cuando revisas los grupos de WhatsApp académicos o las redes sociales donde interactúan los estudiantes de tu entorno universitario, el contenido que genera más interacción suele ser:",
                "acoso-tecnologico",
                [
                    ("Memes generales de internet, avisos de tareas, fechas de exámenes o enlaces de estudio.", None, 0),
                    ("Capturas de pantalla de errores que alguien cometió en clase, stickers basados en fotos de compañeros o debates intensos sobre la vida de otros.", "acoso-tecnologico", 10),
                    ("Suelo mantener estos grupos completamente silenciados o evito abrirlos a menos que sea estrictamente obligatorio para la nota.", "acoso-tecnologico", 10),
                ],
            ),
            (
                "Si alguien hace una pregunta redundante en los canales digitales oficiales o se equivoca en una exposición virtual, la respuesta colectiva en las redes paralelas suele ser:",
                "acoso-tecnologico",
                [
                    ("Ignorar el error o responder la duda de manera directa y respetuosa.", None, 0),
                    ("Convertir el momento en el tema de conversación o chiste de la semana a través de comentarios o canales secundarios.", "acoso-tecnologico", 10),
                ],
            ),
            (
                "En las interacciones individuales fuera del aula con profesores, ayudantes o personal administrativo, ¿cuál de los siguientes ambientes consideras que predomina?",
                "acoso-vulnerabilidad",
                [
                    ("Un trato estrictamente corporativo, plano y enfocado en resolver dudas puntuales de la materia.", None, 0),
                    ("Un trato muy cercano y personalizado, donde es común recibir elogios sobre la apariencia, comentarios informales o preguntas sobre la vida social o sentimental para generar confianza.", "acoso-vulnerabilidad", 10),
                ],
            ),
            (
                "Cuando se asignan oportunidades (como becas, ayudantías de cátedra o cupos en proyectos de investigación), la percepción estudiantil es que:",
                "acoso-vulnerabilidad",
                [
                    ("Se otorgan basándose única y transparentemente en el promedio académico y las competencias técnicas del alumno.", None, 0),
                    ('Influyen mucho ciertos perfiles sociales, asumiendo sutilmente que algunos estudiantes "encajan mejor" o tienen más facilidades que otros por su trasfondo o género.', "acoso-vulnerabilidad", 10),
                ],
            ),
        ]
        units = {unit.slug: unit for unit in CourseUnit.objects.filter(active=True)}
        DiagnosticQuestion.objects.exclude(order__in=range(1, 9)).update(active=False)
        for order, (text, unit_slug, options) in enumerate(questions, start=1):
            question, _ = DiagnosticQuestion.objects.update_or_create(
                order=order,
                defaults={
                    "text": text,
                    "primary_unit": units[unit_slug],
                    "active": True,
                },
            )
            kept_option_ids = []
            for option_order, (label, destination_slug, weight) in enumerate(options, start=1):
                option, _ = DiagnosticOption.objects.update_or_create(
                    question=question,
                    order=option_order,
                    defaults={
                        "label": label,
                        "destination_unit": units.get(destination_slug),
                        "weight": weight,
                    },
                )
                kept_option_ids.append(option.id)
            question.options.exclude(id__in=kept_option_ids).delete()

    def _seed_course(self):
        units = [
            {
                "slug": "acoso-vertical",
                "title": "Límites en Relaciones de Autoridad",
                "description": "Herramientas para reconocer y afrontar dinámicas asimétricas en el entorno académico.",
                "duration": 35,
                "lessons": [
                    ("Autoridad y límites saludables", "Diferencia una exigencia académica de una conducta intimidatoria.", "Una dinámica deja de ser saludable cuando una posición de autoridad se usa para humillar, amenazar, aislar o exigir conductas ajenas al proceso académico. Una retroalimentación legítima se enfoca en el trabajo, usa criterios conocidos y permite aclaraciones.", 6),
                    ("Señales que no deben normalizarse", "Reconoce humillaciones, represalias y solicitudes fuera de canales formales.", "Son alertas las ironías públicas, los ataques a la capacidad personal, las amenazas relacionadas con calificaciones y el contacto insistente fuera de horarios. Observa repetición, desequilibrio de poder e impacto.", 6),
                    ("Herramientas de afrontamiento", "Documenta los hechos y activa apoyo institucional.", "Conserva instrucciones, fechas y comunicaciones completas. Evita confrontaciones que aumenten el riesgo y acude a coordinación académica, bienestar estudiantil o la instancia institucional correspondiente.", 6),
                ],
                "activity": ("Simulación: retroalimentación intimidatoria", "Tu tutor ridiculiza tu avance frente al grupo y advierte que tu calificación puede verse afectada si presentas una queja. ¿Qué haces?"),
                "follow_up": (
                    "Plan personal ante una relación de autoridad",
                    "Organiza una respuesta segura y verificable.",
                    "Define tres elementos antes de actuar: qué evidencia conservarás, qué límite deseas comunicar y qué persona o instancia puede acompañarte. Utiliza hechos observables y evita asumir que debes afrontar la situación sin apoyo.",
                ),
            },
            {
                "slug": "acoso-horizontal",
                "title": "Convivencia y Presión entre Pares",
                "description": "Límites ante aislamiento, novatadas y dinámicas de exclusión grupal en el campus.",
                "duration": 35,
                "lessons": [
                    ("Conflictos y límites entre pares", "Distingue un desacuerdo aislado de un patrón repetido que causa daño.", "Entre personas con posiciones semejantes pueden aparecer exclusión coordinada, rumores, burlas repetidas o presión grupal. Un desacuerdo aislado no equivale a un patrón sostenido; importan la repetición, el impacto y la ausencia de consentimiento.", 6),
                    ("Señales de exclusión y novatadas", "Identifica cuándo una dinámica deja de ser voluntaria.", "La repetición, la coordinación para dejar a alguien fuera y la presión para realizar actos incómodos son señales relevantes. El consentimiento puede retirarse y pertenecer a un grupo no obliga a tolerar humillaciones.", 6),
                    ("Herramientas para romper el aislamiento", "Busca testigos y una red de apoyo confiable.", "Registra hechos concretos, identifica testigos y conversa con una persona de confianza. Solicita acompañamiento y deja constancia por canales universitarios formales.", 6),
                ],
                "activity": ("Árbol de decisión: presión grupal", "Durante una bienvenida te presionan para realizar un reto humillante y dicen que rechazarlo te excluirá del grupo. ¿Qué haces?"),
                "follow_up": (
                    "Plan para fortalecer tu red de apoyo",
                    "Identifica acompañamiento dentro y fuera del grupo.",
                    "Anota dos personas de confianza, un canal universitario y una acción que puedas realizar sin exponerte. Pedir acompañamiento no requiere demostrar primero que la situación es grave.",
                ),
            },
            {
                "slug": "acoso-tecnologico",
                "title": "Bienestar y Seguridad Digital",
                "description": "Herramientas ante exposición de datos, presión social y conductas digitales que cruzan límites.",
                "duration": 37,
                "lessons": [
                    ("Humor y límites digitales", "Reconoce cuándo memes, stickers o bromas cruzan un límite.", "El humor deja de ser compartido cuando una persona no consiente, pide que se detenga o sufre exposición y daño. La repetición, la audiencia y la pérdida de control sobre el contenido aumentan el impacto.", 6),
                    ("Propagación y rol de los grupos", "Comprende cómo una publicación amplifica el daño.", "Reenviar, reaccionar o guardar silencio ante una cadena hostil puede aumentar su alcance. Los grupos universitarios deben conservar una finalidad académica y reglas claras de convivencia.", 6),
                    ("Privacidad, evidencia y reporte", "Recupera control y conserva evidencia digital válida.", "Realiza capturas completas, conserva enlaces, fecha y plataforma sin editar el original. Revisa sesiones, activa verificación en dos pasos, limita etiquetas y reporta por canales institucionales y de la plataforma.", 7),
                ],
                "activity": ("Simulación: chat grupal hostil", "En el grupo de la facultad circula un sticker humillante sobre un compañero y varias personas lo reenvían. ¿Qué haces?"),
                "follow_up": (
                    "Plan de seguridad y privacidad digital",
                    "Revisa accesos, evidencia y canales de reporte.",
                    "Comprueba las sesiones abiertas, activa la verificación en dos pasos y revisa quién puede etiquetarte o ver tu contenido. Conserva la evidencia original y evita reenviarla a personas que no intervengan en la ayuda.",
                ),
            },
            {
                "slug": "acoso-vulnerabilidad",
                "title": "Respeto a la Diversidad e Identidad",
                "description": "Reconocimiento de sesgos y tratos relacionados con género, origen o condición personal.",
                "duration": 35,
                "lessons": [
                    ("Diversidad, identidad y trato digno", "Identifica conductas basadas en prejuicios sobre características personales.", "Estas conductas se apoyan en prejuicios relacionados con género, origen, discapacidad, orientación, condición económica u otras características. Pueden ser explícitas o aparecer como trato condescendiente y exclusión sistemática.", 6),
                    ("Señales encubiertas", "Observa invasión de límites y patrones de minimización.", "Un comentario aparentemente amable puede ser inapropiado si invade tu privacidad, se repite o genera incomodidad. También importan las oportunidades negadas o los comentarios minimizados por prejuicios.", 6),
                    ("Límites y redes de apoyo", "Comunica el límite de forma segura y registra la respuesta.", "Prioriza tu seguridad. Puedes pedir que la comunicación vuelva al ámbito académico, documentar patrones y buscar acompañamiento institucional o profesional.", 6),
                ],
                "activity": ("Árbol de decisión: comentario discriminatorio", "En una reunión minimizan repetidamente tus propuestas por tu origen o condición y el grupo guarda silencio. ¿Qué haces?"),
                "follow_up": (
                    "Plan de límites y trato digno",
                    "Prepara una respuesta centrada en hechos y apoyo.",
                    "Identifica la conducta concreta, su impacto y el límite que necesitas. Si expresarlo directamente no es seguro, registra el patrón y solicita que una persona de confianza o una instancia institucional te acompañe.",
                ),
            },
        ]
        activity_options = [
            {"id": "documentar-reportar", "label": "Conservar el contexto, apoyar a la persona afectada y reportar por un canal seguro.", "feedback": "Esta respuesta protege la evidencia, reduce la exposición y activa una red de apoyo."},
            {"id": "intervenir-sin-escalar", "label": "Intervenir con calma, marcar el límite y buscar apoyo si la conducta continúa.", "feedback": "Intervenir puede ayudar si es seguro; evita exponerte y acompaña la acción con evidencia y apoyo."},
            {"id": "ignorar", "label": "Ignorar la situación y esperar que termine por sí sola.", "feedback": "El silencio puede permitir que el patrón continúe. Prioriza tu seguridad, pero busca una forma segura de documentar o pedir ayuda."},
        ]
        for unit_order, data in enumerate(units, start=1):
            unit, _ = CourseUnit.objects.update_or_create(
                order=unit_order,
                defaults={
                    "slug": data["slug"],
                    "title": data["title"],
                    "description": data["description"],
                    "duration_minutes": data["duration"],
                    "active": True,
                },
            )
            kept_lesson_ids = []
            for lesson_order, (title, summary, content, duration) in enumerate(
                data["lessons"], start=1
            ):
                lesson, _ = Lesson.objects.update_or_create(
                    unit=unit,
                    order=lesson_order,
                    defaults={
                        "title": title,
                        "summary": summary,
                        "content": content,
                        "kind": "lesson",
                        "duration_minutes": duration,
                        "activity_prompt": "",
                        "activity_options": [],
                    },
                )
                kept_lesson_ids.append(lesson.id)
            activity_title, activity_prompt = data["activity"]
            activity, _ = Lesson.objects.update_or_create(
                unit=unit,
                order=4,
                defaults={
                    "title": activity_title,
                    "summary": "Aplica lo aprendido en una decisión contextual.",
                    "content": "Lee el caso y selecciona la respuesta que adoptarías. Después recibirás retroalimentación formativa.",
                    "kind": "activity",
                    "duration_minutes": 6,
                    "activity_prompt": activity_prompt,
                    "activity_options": activity_options,
                },
            )
            kept_lesson_ids.append(activity.id)
            follow_up_title, follow_up_summary, follow_up_content = data["follow_up"]
            follow_up, _ = Lesson.objects.update_or_create(
                unit=unit,
                order=5,
                defaults={
                    "title": follow_up_title,
                    "summary": follow_up_summary,
                    "content": follow_up_content,
                    "kind": "lesson",
                    "duration_minutes": 7,
                    "activity_prompt": "",
                    "activity_options": [],
                },
            )
            kept_lesson_ids.append(follow_up.id)
            unit.lessons.exclude(id__in=kept_lesson_ids).delete()
        CourseUnit.objects.exclude(order__in=range(1, 5)).update(active=False)
        self._seed_quizzes()

    def _seed_quizzes(self):
        question_templates = [
            ("¿Cuál es la señal más importante para distinguir una conducta problemática?", ["Que ocurra en la universidad", "La repetición, el impacto y la ausencia de consentimiento", "Que exista una captura de pantalla"], 1),
            ("¿Qué acción protege mejor la evidencia?", ["Editar la captura para resumirla", "Reenviar el contenido a más personas", "Guardar el contexto completo, la fecha y el enlace"], 2),
            ("Si intervenir directamente puede aumentar el riesgo, ¿qué conviene hacer?", ["Buscar apoyo y usar un canal seguro", "Responder con una amenaza", "Eliminar toda la evidencia"], 0),
            ("¿Qué significa desnormalizar una conducta?", ["Reconocer que una broma repetida puede causar daño y establecer límites", "Aceptar la conducta para evitar conflictos", "Publicarla para que otras personas opinen"], 0),
            ("¿Cuándo debe buscarse ayuda urgente?", ["Solo cuando el contenido se vuelve viral", "Cuando existe peligro inmediato o amenaza a la integridad", "Únicamente después de terminar el curso"], 1),
        ]
        for unit in CourseUnit.objects.filter(active=True):
            kept_question_ids = []
            for order, (text, options, correct_index) in enumerate(question_templates, start=1):
                question, _ = ModuleQuizQuestion.objects.update_or_create(
                    unit=unit,
                    order=order,
                    defaults={"text": text, "active": True},
                )
                kept_question_ids.append(question.id)
                kept_option_ids = []
                for option_order, label in enumerate(options, start=1):
                    option, _ = ModuleQuizOption.objects.update_or_create(
                        question=question,
                        order=option_order,
                        defaults={
                            "label": label,
                            "is_correct": option_order - 1 == correct_index,
                        },
                    )
                    kept_option_ids.append(option.id)
                question.options.exclude(id__in=kept_option_ids).delete()
            unit.quiz_questions.exclude(id__in=kept_question_ids).update(active=False)

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
