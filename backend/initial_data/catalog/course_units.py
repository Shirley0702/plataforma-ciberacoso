"""Contenido formativo interactivo de las rutas de aprendizaje."""


def _guided(title, summary, content, cards, duration=6):
    return {
        "title": title,
        "summary": summary,
        "content": content,
        "duration": duration,
        "interaction_type": "guided",
        "interaction_prompt": f"Encuentra en la escena tres señales relacionadas con «{title}» y abre cada marcador para comprender qué observar.",
        "interaction_config": {
            "cards": cards,
            "completion_message": "Puedes volver a estas ideas cuando necesites comprobar una situación con calma.",
        },
    }


def _video(
    title,
    summary,
    content,
    video_id,
    source_label,
    duration=5,
):
    return {
        "title": title,
        "summary": summary,
        "content": content,
        "duration": duration,
        "interaction_type": "video",
        "interaction_prompt": "Mira el video completo antes de continuar con los puzzles de la unidad.",
        "interaction_config": {
            "video_url": f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&modestbranding=1",
            "video_watch_url": f"https://www.youtube.com/watch?v={video_id}",
            "video_title": title,
            "source_label": source_label,
        },
    }


def _choice(interaction_type, title, summary, content, prompt, options, duration=7):
    return {
        "title": title,
        "summary": summary,
        "content": content,
        "duration": duration,
        "interaction_type": interaction_type,
        "interaction_prompt": prompt,
        "interaction_config": {"options": options},
    }


def _item_activity(
    interaction_type,
    title,
    summary,
    content,
    prompt,
    items,
    completion_feedback,
    duration=6,
    privacy_note="",
):
    return {
        "title": title,
        "summary": summary,
        "content": content,
        "duration": duration,
        "interaction_type": interaction_type,
        "interaction_prompt": prompt,
        "interaction_config": {
            "items": items,
            "completion_feedback": completion_feedback,
            "privacy_note": privacy_note,
        },
    }


def _option(option_id, label, feedback, recommended=False):
    option = {
        "id": option_id,
        "label": label,
        "feedback": feedback,
    }
    if recommended:
        option["recommended"] = True
    return option


def _item(item_id, label, detail, visual=""):
    item = {"id": item_id, "label": label, "detail": detail}
    if visual:
        item["visual"] = visual
    return item


def _quiz(text, options, correct_index):
    return {"text": text, "options": options, "correct_index": correct_index}


COMMON_QUIZ = (
    _quiz(
        "Si actuar directamente puede aumentar el riesgo, ¿qué opción es más segura?",
        (
            "Responder de inmediato y sin acompañamiento",
            "Buscar apoyo y usar un canal seguro",
            "Eliminar toda la información disponible",
        ),
        1,
    ),
    _quiz(
        "¿Cuándo se debe pedir ayuda urgente?",
        (
            "Cuando existe peligro inmediato o una amenaza a la integridad",
            "Solo después de completar todo el curso",
            "Únicamente cuando muchas personas conocen la situación",
        ),
        0,
    ),
)


COURSE_UNITS = (
    {
        "slug": "acoso-vertical",
        "title": "Límites en Relaciones de Autoridad",
        "description": "Practica cómo reconocer límites, conservar hechos y pedir acompañamiento ante una relación de autoridad.",
        "duration": 41,
        "learning_items": (
            _guided(
                "Exigencia académica o trato que cruza un límite",
                "Compara una corrección válida con una conducta que causa daño.",
                "Una calificación baja o una corrección exigente no significan por sí solas que exista un problema. Importa cómo se usa la autoridad, si la conducta se repite y si puedes preguntar sin recibir represalias.",
                (
                    {"title": "Se centra en el trabajo", "body": "Una corrección saludable explica criterios, señala el producto académico y permite aclaraciones."},
                    {"title": "Ataca a la persona", "body": "Insultos, burlas públicas o comentarios sobre tu capacidad no son una forma necesaria de enseñar."},
                    {"title": "Usa el poder para presionar", "body": "Amenazar con notas u oportunidades para obtener obediencia personal es una señal importante."},
                ),
            ),
            _choice(
                "decision",
                "Decide sin exponerte",
                "Observa las consecuencias de tres respuestas posibles.",
                "No tienes que reaccionar de inmediato. Una respuesta segura protege tu bienestar y conserva opciones para pedir ayuda.",
                "Un tutor ridiculiza un avance frente al grupo y advierte que reclamar puede afectar la nota. ¿Qué harías primero?",
                (
                    _option("responder-solo", "Enfrentarlo a solas y responder con otra amenaza.", "Puede aumentar el riesgo y dejarte sin acompañamiento. Tomar una pausa también es una decisión válida."),
                    _option("registrar-apoyo", "Anotar lo ocurrido, conservar mensajes y hablar con una persona de confianza.", "Esta opción conserva hechos y evita que tengas que afrontar la situación sin apoyo.", recommended=True),
                    _option("borrar-ignorar", "Borrar los mensajes y tratar de olvidar lo ocurrido.", "Alejarte puede darte calma momentánea, pero borrar la información limita tus opciones. Puedes conservarla sin revisarla constantemente."),
                ),
            ),
            _item_activity(
                "matching",
                "Mapa de señales observables",
                "Revisa hechos concretos sin culparte ni sacar conclusiones apresuradas.",
                "No necesitas decidir aquí cómo llamar a la situación. El objetivo es separar hechos observables de suposiciones.",
                "Marca cada elemento después de leer cómo puede ayudarte:",
                (
                    _item("criterio", "¿La corrección se basó en criterios conocidos?", "Permite distinguir una evaluación académica de un ataque personal.", "document"),
                    _item("repeticion", "¿La conducta ocurrió más de una vez?", "La repetición ayuda a reconocer un patrón, aunque un hecho grave también merece atención.", "repeat"),
                    _item("represalia", "¿Hubo amenaza sobre notas u oportunidades?", "Una posible represalia cambia el nivel de seguridad con el que conviene actuar.", "opportunity"),
                    _item("impacto", "¿Cambió tu forma de asistir, participar o estudiar?", "El impacto importa incluso cuando otras personas minimizan lo ocurrido.", "compass"),
                ),
                "Ya tienes cuatro preguntas concretas para ordenar la situación sin exigirte una respuesta inmediata.",
            ),
            _choice(
                "practice",
                "Ensaya una respuesta segura",
                "Elige una frase y observa qué protege.",
                "Poner un límite no siempre es seguro ni obligatorio. Puedes usar una frase, escribir por un canal formal o pedir que alguien te acompañe.",
                "Si fuera seguro responder, ¿qué frase mantiene el límite y se centra en hechos?",
                (
                    _option("amenaza", "Si vuelve a hacerlo, voy a perjudicarlo también.", "Una amenaza puede escalar la situación y alejar la conversación de los hechos."),
                    _option("limite", "Necesito que la retroalimentación se centre en mi trabajo y en los criterios de la materia.", "La frase describe el límite sin revelar información personal ni iniciar una confrontación.", recommended=True),
                    _option("culpa", "Seguramente todo es mi culpa; no volveré a preguntar.", "Tener dudas o pedir criterios no te convierte en responsable de un trato humillante."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Puzzle: responde sin quedar a solas",
                "Ordena una secuencia que conserva tu seguridad y tus opciones.",
                "Cuando una persona con autoridad cruza un límite, no tienes que resolverlo en una confrontación. Primero recupera calma; después conserva hechos y busca compañía.",
                "Ordena los pasos desde la primera acción hasta la última:",
                (
                    _item("pausa", "Pausa y sal de la conversación si no te sientes seguro.", "No estás obligado a responder en ese momento ni a permanecer a solas.", "pause"),
                    _item("evidencia", "Conserva los hechos sin difundirlos.", "Guarda fechas, instrucciones, correos o mensajes completos en un lugar privado.", "document"),
                    _item("persona", "Busca a una persona de confianza.", "El acompañamiento evita que tengas que ordenar la situación sin apoyo.", "support"),
                    _item("canal", "Consulta un canal universitario acompañado.", "Puedes pedir orientación antes de decidir si realizarás otra acción.", "compass"),
                ),
                "Construiste una secuencia que prioriza tu seguridad y evita que afrontes la situación a solas.",
                privacy_note="No guardes aquí nombres, capturas ni información personal.",
            ),
            _video(
                "Video: la convivencia también se aprende",
                "Observa cómo los acuerdos y el diálogo construyen relaciones educativas respetuosas.",
                "El video introduce una idea clave: la autoridad también participa en la creación de un entorno donde sea posible preguntar, disentir y aprender sin humillaciones.",
                "cfEJ1XRWMvk",
                "Ministerio de Educación de Chile",
            ),
        ),
        "quiz": (
            _quiz("¿Qué caracteriza una retroalimentación académica saludable?", ("Se enfoca en criterios y permite aclaraciones", "Expone errores para avergonzar", "Exige disponibilidad sin límites"), 0),
            _quiz("¿Qué dato ayuda a reconocer un patrón en una relación de autoridad?", ("La popularidad del profesor", "La repetición y las posibles represalias", "El tamaño del aula"), 1),
            _quiz("¿Qué acción conserva mejor tus opciones?", ("Borrar los mensajes", "Publicar todo de inmediato", "Guardar el contexto y buscar acompañamiento"), 2),
            *COMMON_QUIZ,
        ),
    },
    {
        "slug": "acoso-horizontal",
        "title": "Convivencia y Presión entre Pares",
        "description": "Practica límites, apoyo entre compañeros y respuestas seguras ante exclusión o presión grupal.",
        "duration": 40,
        "learning_items": (
            _guided(
                "Del desacuerdo a un patrón de presión",
                "Distingue un conflicto puntual de acciones repetidas contra una persona.",
                "No todos los desacuerdos entre compañeros son iguales. La repetición, la coordinación del grupo, la falta de consentimiento y el impacto permiten observar cuándo una situación necesita apoyo.",
                (
                    {"title": "Conflicto puntual", "body": "Hay una diferencia concreta y ambas personas pueden explicar lo ocurrido o buscar mediación."},
                    {"title": "Exclusión repetida", "body": "La misma persona queda fuera, recibe tareas menores o pierde información en varias ocasiones."},
                    {"title": "Presión para pertenecer", "body": "Se exige aceptar bromas, retos o humillaciones para conservar un lugar en el grupo."},
                ),
            ),
            _choice(
                "decision",
                "Actúa como compañero seguro",
                "Practica una respuesta que apoye sin aumentar la exposición.",
                "Ayudar no significa enfrentarte solo al grupo. Puedes interrumpir la difusión, acercarte en privado y buscar apoyo.",
                "Un equipo comparte una burla sobre un compañero y le oculta información del proyecto. ¿Qué harías?",
                (
                    _option("reenviar", "Reenviar la burla para preguntar qué opinan otros.", "Aunque la intención sea consultar, reenviar aumenta la exposición."),
                    _option("apoyo-privado", "No difundirla, hablar en privado con el compañero y acordar juntos a quién pedir apoyo.", "Esta opción reduce la exposición y devuelve a la persona parte del control sobre los siguientes pasos.", recommended=True),
                    _option("enfrentar-grupo", "Insultar públicamente a todo el grupo.", "Puede aumentar el conflicto y el riesgo. Es posible marcar un límite sin responder con otra agresión."),
                ),
            ),
            _item_activity(
                "matching",
                "Señales de presión grupal",
                "Comprueba qué observar antes de actuar.",
                "Puedes usar esta lista tanto si la situación te ocurre a ti como si la observas en otra persona.",
                "Revisa cada señal:",
                (
                    _item("consentimiento", "La persona puede decir que no sin recibir castigo.", "El consentimiento deja de ser libre cuando negarse produce amenazas o exclusión.", "boundary"),
                    _item("repeticion", "La conducta se repite contra la misma persona.", "Un patrón repetido requiere una respuesta distinta a un comentario aislado.", "repeat"),
                    _item("coordinacion", "Varias personas participan o guardan información.", "La coordinación puede aumentar el aislamiento y el impacto académico.", "group"),
                    _item("salida", "Existe una forma segura de salir o pedir ayuda.", "Planear una salida evita que intervenir dependa solo de la confrontación.", "route"),
                ),
                "Ahora puedes observar el consentimiento, la repetición, la coordinación y una salida segura.",
            ),
            _choice(
                "practice",
                "Practica un límite entre compañeros",
                "Elige una frase breve que no culpe ni exponga.",
                "Una frase clara puede servir para detener una conducta o abrir una conversación privada. Si usarla no es seguro, busca apoyo.",
                "¿Qué frase respeta a la persona y marca un límite?",
                (
                    _option("normalizar", "No exageres, así nos llevamos todos.", "Minimizar puede hacer que la persona se sienta más aislada."),
                    _option("limite-grupo", "No voy a compartir eso. Si hay un problema con el proyecto, hablemos del trabajo.", "La frase detiene la difusión y devuelve la conversación a un asunto concreto.", recommended=True),
                    _option("exponer", "Voy a publicar quiénes hicieron esto para que aprendan.", "Publicar nombres puede escalar la situación y exponer también a la persona afectada."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Puzzle: corta la presión del grupo",
                "Ordena una forma de ayudar sin aumentar la exposición.",
                "Cuando una broma, exclusión o presión se repite, la persona puede sentirse obligada a aceptarla para pertenecer. Esta secuencia devuelve control sin enfrentar al grupo a solas.",
                "Ordena los pasos desde la primera acción hasta la última:",
                (
                    _item("cortar", "Detén el reenvío o la participación.", "No reaccionar, reenviar ni celebrar reduce el alcance de la presión.", "stop"),
                    _item("privado", "Acércate en privado y escucha.", "Evita pedir explicaciones frente al grupo o hablar en nombre de la persona.", "chat"),
                    _item("preguntar", "Pregunta qué apoyo desea.", "La persona decide si quiere compañía, registro de hechos o una consulta.", "help"),
                    _item("acompanar", "Acompaña al canal que elija.", "Un tutor, docente o profesional de bienestar puede orientar sin dejarla sola.", "compass"),
                ),
                "Ordenaste una respuesta que detiene la presión y devuelve control a la persona afectada.",
                privacy_note="Los nombres de tus contactos deben permanecer fuera de esta plataforma.",
            ),
            _video(
                "Video: comprender la presión y el daño entre pares",
                "Reconoce por qué participar, reenviar o guardar silencio puede sostener un patrón grupal.",
                "Este video ofrece una explicación visual de las dinámicas entre pares y sirve como punto de partida para practicar apoyo sin confrontaciones que aumenten el riesgo.",
                "SEC_dOWFN5M",
                "PantallasAmigas",
            ),
        ),
        "quiz": (
            _quiz("¿Qué diferencia un conflicto puntual de un patrón grupal?", ("Que ocurra entre estudiantes", "La repetición, coordinación e impacto", "Que suceda fuera del aula"), 1),
            _quiz("Si un compañero pide que una broma se detenga, ¿qué corresponde hacer?", ("Detenerla y respetar el límite", "Pedir que explique por qué", "Continuar si la mayoría se ríe"), 0),
            _quiz("¿Cómo se apoya sin aumentar la exposición?", ("Reenviando el contenido", "Publicando a los responsables", "Hablando en privado y acordando los siguientes pasos"), 2),
            *COMMON_QUIZ,
        ),
    },
    {
        "slug": "acoso-tecnologico",
        "title": "Bienestar y Seguridad Digital",
        "description": "Recupera control sobre contenido, cuentas y evidencia sin aumentar la difusión.",
        "duration": 43,
        "learning_items": (
            _guided(
                "Control, consentimiento y alcance digital",
                "Comprende por qué una acción pequeña puede amplificar el impacto.",
                "En internet importa quién autorizó el contenido, cuántas personas pueden verlo y si es posible detener su circulación. Reaccionar, guardar o reenviar también puede aumentar el alcance.",
                (
                    {"title": "Consentimiento", "body": "Compartir una foto o captura requiere permiso, incluso si llegó a un grupo privado."},
                    {"title": "Alcance", "body": "Cada reenvío crea una nueva copia y reduce el control de la persona sobre el contenido."},
                    {"title": "Evidencia segura", "body": "Conservar una copia completa para pedir ayuda es distinto de difundirla entre más personas."},
                ),
            ),
            _choice(
                "decision",
                "Detén la cadena sin perder evidencia",
                "Elige una primera acción ante contenido que expone a alguien.",
                "No necesitas investigar por tu cuenta ni descargar más copias de las necesarias. Prioriza detener la difusión y usar canales seguros.",
                "Recibes en un grupo una captura privada usada para burlarse de un estudiante. ¿Qué haces primero?",
                (
                    _option("reenviar-prueba", "Reenviarla a varios amigos para tener testigos.", "Genera más copias y aumenta la exposición, aunque busques ayuda."),
                    _option("guardar-reportar", "Conservar el contexto necesario, no reenviar y consultar con la persona afectada o un canal seguro.", "Reduce la difusión, conserva evidencia y respeta el control de la persona afectada.", recommended=True),
                    _option("responder-insulto", "Insultar en el grupo a quien la publicó.", "Puede escalar la conversación y no elimina el contenido."),
                ),
            ),
            _item_activity(
                "matching",
                "Protege evidencia y privacidad",
                "Revisa acciones digitales que mantienen opciones abiertas.",
                "No subas capturas a este curso. La lista sirve para recordar qué puedes hacer directamente en tu dispositivo.",
                "Lee y marca cada acción:",
                (
                    _item("contexto", "Conservar fecha, usuario, enlace y conversación completa.", "El contexto ayuda a comprender qué ocurrió sin editar el material original.", "document"),
                    _item("sesiones", "Revisar sesiones abiertas y cambiar accesos comprometidos.", "Cerrar sesiones desconocidas y usar verificación en dos pasos recupera control de la cuenta.", "sessions"),
                    _item("privacidad", "Revisar etiquetas, menciones y quién puede ver el contenido.", "Los ajustes reducen nuevas exposiciones mientras buscas apoyo.", "lock"),
                    _item("reporte", "Usar el reporte de la plataforma y un canal universitario.", "Los dos canales atienden partes distintas: retirar contenido y recibir acompañamiento.", "report"),
                ),
                "Tienes una secuencia que protege evidencia sin pedirte compartirla en esta plataforma.",
            ),
            _choice(
                "practice",
                "Practica una respuesta en un chat",
                "Elige un mensaje breve que reduzca la difusión.",
                "Responder con calma puede cortar la participación del grupo. Si hacerlo te expone, sal del chat y pide apoyo.",
                "¿Qué mensaje ayuda a detener la cadena?",
                (
                    _option("curiosidad", "¿Alguien tiene la captura completa? Envíenmela por interno.", "Solicitar más copias aumenta la difusión."),
                    _option("corte", "No compartamos contenido de otra persona sin permiso. Voy a detener el reenvío.", "El mensaje marca el límite y no repite el contenido.", recommended=True),
                    _option("amenaza", "Si no borran esto, publicaré información de todos.", "Responder con otra exposición puede aumentar el daño y el riesgo."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Puzzle: recupera el control digital",
                "Ordena una respuesta que protege la cuenta, la evidencia y tu bienestar.",
                "Una exposición digital puede hacerte sentir que perdiste todo control. Actuar en orden evita crear más copias y separa la seguridad de la cuenta del acompañamiento que también puedes necesitar.",
                "Ordena los pasos desde la primera acción hasta la última:",
                (
                    _item("acceso", "Protege el acceso a la cuenta.", "Cierra sesiones desconocidas, cambia la clave y activa un segundo factor.", "lock"),
                    _item("copia", "Conserva una copia privada con contexto.", "Guarda fecha, usuario y conversación sin reenviar el contenido.", "document"),
                    _item("plataforma", "Reporta y bloquea en la aplicación.", "Bloquear reduce el contacto; reportar solicita revisar o retirar el contenido.", "report"),
                    _item("apoyo", "Pide acompañamiento para decidir lo siguiente.", "Una persona de confianza o un servicio universitario puede ayudarte.", "support"),
                ),
                "Ordenaste una recuperación digital que evita nuevas copias y conserva opciones de apoyo.",
                privacy_note="Nunca escribas aquí contraseñas, usuarios, enlaces privados ni el contenido recibido.",
            ),
            _video(
                "Video: privacidad y consentimiento al compartir",
                "Observa cómo una publicación aparentemente pequeña puede afectar a otra persona.",
                "El video permite analizar el consentimiento antes de publicar imágenes o información y prepara la práctica de decisiones digitales seguras.",
                "ELDlQj1aLmo",
                "PantallasAmigas",
            ),
        ),
        "quiz": (
            _quiz("¿Qué acción aumenta la difusión de contenido privado?", ("Conservar una copia privada", "Reenviarlo para conseguir testigos", "Usar el reporte de la plataforma"), 1),
            _quiz("¿Qué debe incluir una evidencia digital útil?", ("Solo una frase recortada", "Una versión editada", "Contexto, fecha, usuario y enlace cuando exista"), 2),
            _quiz("¿Qué ayuda a recuperar el control de una cuenta?", ("Cerrar sesiones desconocidas y activar un segundo factor", "Compartir la contraseña con amigos", "Responder públicamente con más información"), 0),
            *COMMON_QUIZ,
        ),
    },
    {
        "slug": "acoso-vulnerabilidad",
        "title": "Respeto a la Diversidad e Identidad",
        "description": "Practica cómo responder a prejuicios, proteger la privacidad y buscar un trato digno.",
        "duration": 41,
        "learning_items": (
            _guided(
                "Trato digno en situaciones cotidianas",
                "Reconoce comentarios y decisiones que se apoyan en prejuicios.",
                "Una conducta puede parecer pequeña y aun así repetirse o limitar oportunidades. Observa si se trata a la persona de forma distinta por su género, origen, discapacidad, orientación o situación económica.",
                (
                    {"title": "Comentario aislado", "body": "Puede corregirse cuando se marca el límite y no vuelve a repetirse."},
                    {"title": "Patrón de minimización", "body": "Las ideas de la misma persona se ignoran o ridiculizan por una característica personal."},
                    {"title": "Barrera concreta", "body": "Se niega una oportunidad, adaptación o participación debido a un prejuicio."},
                ),
            ),
            _choice(
                "decision",
                "Apoya sin hablar por la otra persona",
                "Practica una intervención que devuelve control.",
                "Apoyar no significa revelar información privada ni decidir por otra persona. Pregunta qué necesita y respeta su respuesta.",
                "En una reunión rechazan varias veces las ideas de una compañera con comentarios sobre su origen. ¿Qué harías?",
                (
                    _option("decidir-por-ella", "Presentar una queja con todos sus datos sin consultarle.", "La intención puede ser positiva, pero usar sus datos sin permiso le quita control."),
                    _option("devolver-idea", "Volver a la idea, pedir que se evalúe por su contenido y hablar con ella en privado después.", "Interrumpe el prejuicio sin exponer información adicional y permite acordar el siguiente paso.", recommended=True),
                    _option("broma", "Hacer otra broma sobre el grupo para equilibrar la situación.", "Responder con otro prejuicio mantiene una dinámica que puede dañar a más personas."),
                ),
            ),
            _item_activity(
                "matching",
                "Observa el trato, no la intención",
                "Usa hechos para reconocer barreras y patrones.",
                "No necesitas demostrar qué pensaba otra persona. Puedes observar la conducta y su efecto.",
                "Revisa cada pregunta:",
                (
                    _item("comparacion", "¿A otras personas se les trata de la misma manera?", "Comparar situaciones semejantes permite observar diferencias de trato.", "balance"),
                    _item("repeticion", "¿El comentario o la exclusión se repite?", "La repetición muestra que no fue solo un error corregido.", "repeat"),
                    _item("oportunidad", "¿Se perdió una oportunidad o participación?", "Las consecuencias concretas ayudan a explicar el impacto.", "opportunity"),
                    _item("privacidad", "¿Se compartió información personal sin permiso?", "La identidad, salud o situación económica pertenecen a la persona.", "lock"),
                ),
                "Ahora puedes describir el trato y su impacto sin tener que adivinar intenciones.",
            ),
            _choice(
                "practice",
                "Practica una intervención respetuosa",
                "Elige una frase que se centre en el aporte y no exponga a nadie.",
                "Una intervención breve puede devolver el turno o pedir criterios. Si intervenir te pone en riesgo, registra el hecho y busca apoyo.",
                "¿Qué frase ayuda a restablecer un trato justo?",
                (
                    _option("ataque", "Ustedes siempre discriminan y son malas personas.", "Etiquetar a todo el grupo puede cerrar la conversación y alejarla del hecho concreto."),
                    _option("hecho", "Quisiera que revisemos su propuesta por el contenido y que pueda terminar de explicarla.", "La frase devuelve la participación y se centra en una acción observable.", recommended=True),
                    _option("silencio", "Mejor no digamos nada para que ella no se sienta incómoda.", "El silencio puede dejar sola a la persona. También puedes acercarte después si intervenir no es seguro."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Puzzle: devuelve control sin exponer la identidad",
                "Ordena una intervención centrada en hechos, consentimiento y apoyo.",
                "Cuando un prejuicio limita la participación o expone información personal, el daño no depende de que puedas demostrar la intención. Esta secuencia permite reconocer el hecho y apoyar sin decidir por otra persona.",
                "Ordena los pasos desde la primera acción hasta la última:",
                (
                    _item("hechos", "Observa la conducta y su efecto.", "Describe palabras, decisiones y oportunidades perdidas sin adivinar intenciones.", "observe"),
                    _item("privado", "Habla en privado con la persona.", "Escucha sin pedirle que justifique su identidad o cuente más de lo que desea.", "chat"),
                    _item("acompanamiento", "Pregunta qué apoyo quiere recibir.", "Acompañar no significa decidir ni revelar información por ella.", "support"),
                    _item("canal", "Consulta el canal que la persona elija.", "Puede pedir información primero, sin presentar inmediatamente una queja formal.", "compass"),
                ),
                "Construiste una respuesta que reconoce el trato desigual y mantiene el control en la persona.",
                privacy_note="No registres aquí diagnósticos, identidad, orientación, origen ni otros datos sensibles.",
            ),
            _video(
                "Video: convivir respetando las diferencias",
                "Reflexiona sobre el valor de las diferencias y el trato digno en un grupo.",
                "El video presenta la diversidad como parte normal de la convivencia. Después podrás practicar cómo intervenir sin revelar información privada ni hablar por otra persona.",
                "xXL2LSyAqDY",
                "Recurso educativo de convivencia escolar",
            ),
        ),
        "quiz": (
            _quiz("¿Qué permite observar una diferencia de trato?", ("Comparar situaciones semejantes y sus consecuencias", "Adivinar la intención", "Contar cuántas personas estaban presentes"), 0),
            _quiz("¿Cómo se apoya sin quitar control?", ("Publicando la situación", "Preguntando qué necesita y respetando su decisión", "Presentando datos sin permiso"), 1),
            _quiz("¿Qué frase se centra en hechos?", ("Todos ustedes son iguales", "Seguramente fue una broma", "Revisemos la propuesta por su contenido y permitamos que termine"), 2),
            *COMMON_QUIZ,
        ),
    },
    {
        "slug": "fundamentos-preventivos",
        "title": "Convivencia y Autocuidado Preventivo",
        "description": "Fortalece acuerdos, privacidad, límites y redes de apoyo antes de una situación difícil.",
        "duration": 39,
        "learning_items": (
            _guided(
                "Acuerdos que crean un espacio seguro",
                "Identifica prácticas sencillas para estudiar y colaborar con respeto.",
                "Los acuerdos reducen confusiones y permiten establecer límites antes de un problema. Deben poder revisarse y aplicarse a todas las personas del grupo.",
                (
                    {"title": "Horarios", "body": "Definir cuándo se espera una respuesta evita convertir la disponibilidad permanente en una obligación."},
                    {"title": "Permiso", "body": "Preguntar antes de compartir fotos, mensajes o datos mantiene el control en cada persona."},
                    {"title": "Salida", "body": "Toda actividad debe permitir decir que no o retirarse sin castigo ni humillación."},
                ),
            ),
            _choice(
                "decision",
                "Construye un acuerdo de equipo",
                "Elige reglas que previenen presión y exposición.",
                "Un acuerdo funciona cuando es claro, realista y puede revisarse entre todos.",
                "Un equipo nuevo organizará su comunicación. ¿Qué propuesta protege mejor a sus integrantes?",
                (
                    _option("siempre-disponibles", "Todos deben responder a cualquier hora para demostrar compromiso.", "La disponibilidad permanente puede generar presión y no considera las circunstancias de cada persona."),
                    _option("acuerdo-claro", "Definir horarios, un canal principal y pedir permiso antes de compartir contenido personal.", "Establece expectativas concretas y protege la privacidad desde el inicio.", recommended=True),
                    _option("sin-reglas", "No acordar nada; cada persona sabrá qué hacer.", "Sin acuerdos es más difícil marcar un límite o resolver un malentendido."),
                ),
            ),
            _item_activity(
                "matching",
                "Revisión preventiva de bienestar digital",
                "Comprueba configuraciones antes de necesitarlas.",
                "Realiza la revisión en tus propias aplicaciones. Esta plataforma no solicita credenciales ni acceso a tus cuentas.",
                "Lee cada acción y márcala cuando sepas dónde realizarla:",
                (
                    _item("privacidad", "Revisar quién puede ver y compartir mis publicaciones.", "Limitar la audiencia reduce exposiciones no deseadas.", "lock"),
                    _item("etiquetas", "Elegir quién puede etiquetarme o mencionarme.", "Revisar etiquetas antes de publicarlas mantiene mayor control.", "tag"),
                    _item("segundo-factor", "Activar un segundo factor de autenticación.", "Añade una barrera aunque alguien conozca tu contraseña.", "key"),
                    _item("sesiones", "Saber dónde revisar y cerrar sesiones abiertas.", "Permite responder rápido si un dispositivo se pierde o un acceso parece extraño.", "sessions"),
                ),
                "Completaste una revisión preventiva sin compartir datos de tus cuentas.",
            ),
            _choice(
                "practice",
                "Practica decir que no",
                "Elige una respuesta breve y clara.",
                "No necesitas dar una explicación extensa para poner un límite. Puedes repetirlo, cambiar de canal o pedir apoyo.",
                "Un compañero pide compartir una captura privada en el grupo. ¿Qué responderías?",
                (
                    _option("ceder", "Está bien, pero bórrenla después.", "Una vez enviada pueden existir nuevas copias y perderse el control."),
                    _option("limite", "No tengo permiso para compartirla. Podemos explicar el tema sin publicar la captura.", "Marca el límite y ofrece una alternativa que no expone a nadie.", recommended=True),
                    _option("ataque", "Si insistes, publicaré algo tuyo.", "Responder con otra amenaza crea un nuevo riesgo."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Puzzle: prepara una red antes de necesitarla",
                "Ordena acciones preventivas desde el cuidado cotidiano hasta la urgencia.",
                "Reconocer límites y preparar apoyos antes de una situación difícil reduce la presión de decidir cuando hay miedo o confusión.",
                "Ordena los pasos desde la preparación cotidiana hasta una emergencia:",
                (
                    _item("privacidad", "Revisa privacidad, accesos y permisos.", "Prevenir incluye controlar quién ve contenido y proteger las cuentas.", "lock"),
                    _item("persona", "Identifica una persona de confianza.", "Puede escuchar, acompañar o ayudarte a ordenar opciones.", "support"),
                    _item("universidad", "Conoce el servicio de orientación universitario.", "Puedes consultar cómo funciona antes de necesitarlo.", "university"),
                    _item("emergencia", "Ante peligro inmediato, usa el canal de emergencia.", "En Ecuador, el número único de emergencias es 9-1-1.", "emergency"),
                ),
                "Ordenaste una red gradual: prevención, confianza, orientación y respuesta urgente.",
                privacy_note="Mantén nombres, teléfonos personales y detalles sensibles fuera de la plataforma.",
            ),
            _video(
                "Video: protege tu cuenta con un segundo paso",
                "Comprende de forma visual por qué una contraseña no siempre es suficiente.",
                "El video introduce una medida concreta de autocuidado digital que puedes activar antes de una situación de riesgo.",
                "6nWOijDWOag",
                "Computer Hoy",
            ),
        ),
        "quiz": (
            _quiz("¿Qué hace útil un acuerdo de equipo?", ("Que exija disponibilidad total", "Que sea claro, realista y revisable", "Que no se escriba"), 1),
            _quiz("¿Qué protege el consentimiento digital?", ("Pedir permiso antes de compartir contenido", "Borrar después de reenviar", "Compartir solo en grupos cerrados"), 0),
            _quiz("¿Qué configuración protege una cuenta aunque se conozca la contraseña?", ("Las etiquetas automáticas", "Una cuenta pública", "El segundo factor de autenticación"), 2),
            *COMMON_QUIZ,
        ),
    },
)
