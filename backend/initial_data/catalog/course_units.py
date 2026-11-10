"""Contenido formativo interactivo de las rutas de aprendizaje."""


def _guided(title, summary, content, cards, duration=6):
    return {
        "title": title,
        "summary": summary,
        "content": content,
        "duration": duration,
        "interaction_type": "guided",
        "interaction_prompt": "Descubre todas las pistas y construye la idea paso a paso.",
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
    activity_prompt = (
        "Conecta cada idea con la explicación que le corresponde."
        if interaction_type == "matching"
        else prompt
    )
    return {
        "title": title,
        "summary": summary,
        "content": content,
        "duration": duration,
        "interaction_type": interaction_type,
        "interaction_prompt": activity_prompt,
        "interaction_config": {
            "items": items,
            "completion_feedback": completion_feedback,
            "privacy_note": privacy_note,
        },
    }


def _option(option_id, label, feedback):
    return {
        "id": option_id,
        "label": label,
        "feedback": feedback,
    }


def _item(item_id, label, detail):
    return {"id": item_id, "label": label, "detail": detail}


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
                    _option("registrar-apoyo", "Anotar lo ocurrido, conservar mensajes y hablar con una persona de confianza.", "Esta opción conserva hechos y evita que tengas que afrontar la situación sin apoyo."),
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
                    _item("criterio", "¿La corrección se basó en criterios conocidos?", "Permite distinguir una evaluación académica de un ataque personal."),
                    _item("repeticion", "¿La conducta ocurrió más de una vez?", "La repetición ayuda a reconocer un patrón, aunque un hecho grave también merece atención."),
                    _item("represalia", "¿Hubo amenaza sobre notas u oportunidades?", "Una posible represalia cambia el nivel de seguridad con el que conviene actuar."),
                    _item("impacto", "¿Cambió tu forma de asistir, participar o estudiar?", "El impacto importa incluso cuando otras personas minimizan lo ocurrido."),
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
                    _option("limite", "Necesito que la retroalimentación se centre en mi trabajo y en los criterios de la materia.", "La frase describe el límite sin revelar información personal ni iniciar una confrontación."),
                    _option("culpa", "Seguramente todo es mi culpa; no volveré a preguntar.", "Tener dudas o pedir criterios no te convierte en responsable de un trato humillante."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Tu plan de apoyo en cuatro pasos",
                "Prepara opciones sin escribir nombres ni detalles sensibles.",
                "Este plan guarda únicamente los pasos marcados. No solicita nombres, mensajes ni una descripción de lo ocurrido.",
                "Marca cada paso cuando tengas una opción en mente:",
                (
                    _item("evidencia", "Sé qué información conservaría.", "Fechas, instrucciones, correos o mensajes completos pueden ayudarte a explicar los hechos."),
                    _item("persona", "Tengo una persona con quien podría hablar.", "Puede ser alguien de confianza dentro o fuera de la universidad."),
                    _item("canal", "Identifiqué un canal universitario de orientación.", "Bienestar estudiantil, coordinación o la instancia definida por tu universidad son posibles puntos de inicio."),
                    _item("pausa", "Sé cómo salir o pausar si no me siento seguro.", "No estás obligado a continuar una conversación o actividad que te exponga."),
                ),
                "Tu plan básico está preparado. Puedes cambiarlo cuando lo necesites y pedir acompañamiento antes de actuar.",
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
                    _option("apoyo-privado", "No difundirla, hablar en privado con el compañero y acordar juntos a quién pedir apoyo.", "Esta opción reduce la exposición y devuelve a la persona parte del control sobre los siguientes pasos."),
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
                    _item("consentimiento", "La persona puede decir que no sin recibir castigo.", "El consentimiento deja de ser libre cuando negarse produce amenazas o exclusión."),
                    _item("repeticion", "La conducta se repite contra la misma persona.", "Un patrón repetido requiere una respuesta distinta a un comentario aislado."),
                    _item("coordinacion", "Varias personas participan o guardan información.", "La coordinación puede aumentar el aislamiento y el impacto académico."),
                    _item("salida", "Existe una forma segura de salir o pedir ayuda.", "Planear una salida evita que intervenir dependa solo de la confrontación."),
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
                    _option("limite-grupo", "No voy a compartir eso. Si hay un problema con el proyecto, hablemos del trabajo.", "La frase detiene la difusión y devuelve la conversación a un asunto concreto."),
                    _option("exponer", "Voy a publicar quiénes hicieron esto para que aprendan.", "Publicar nombres puede escalar la situación y exponer también a la persona afectada."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Red de apoyo sin datos personales",
                "Prepara alternativas antes de una situación difícil.",
                "No tienes que escribir nombres. El sistema guarda solo qué pasos ya consideraste.",
                "Marca cada paso cuando tengas una opción:",
                (
                    _item("aliado", "Puedo identificar a un compañero seguro.", "Una persona aliada puede acompañar, confirmar hechos o ayudar a no quedar aislado."),
                    _item("adulto", "Conozco una persona responsable en la universidad.", "Un docente de confianza, tutor o profesional de bienestar puede orientar."),
                    _item("registro", "Sé qué hechos concretos anotaría.", "Fechas, mensajes y cambios en el trabajo ayudan a explicar un patrón."),
                    _item("salida", "Tengo una forma de salir de una actividad incómoda.", "Puedes retirarte, llamar a alguien o pedir acompañamiento sin justificarte ante el grupo."),
                ),
                "Tu red básica está identificada sin guardar información sensible.",
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
                    _option("guardar-reportar", "Conservar el contexto necesario, no reenviar y consultar con la persona afectada o un canal seguro.", "Reduce la difusión, conserva evidencia y respeta el control de la persona afectada."),
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
                    _item("contexto", "Conservar fecha, usuario, enlace y conversación completa.", "El contexto ayuda a comprender qué ocurrió sin editar el material original."),
                    _item("sesiones", "Revisar sesiones abiertas y cambiar accesos comprometidos.", "Cerrar sesiones desconocidas y usar verificación en dos pasos recupera control de la cuenta."),
                    _item("privacidad", "Revisar etiquetas, menciones y quién puede ver el contenido.", "Los ajustes reducen nuevas exposiciones mientras buscas apoyo."),
                    _item("reporte", "Usar el reporte de la plataforma y un canal universitario.", "Los dos canales atienden partes distintas: retirar contenido y recibir acompañamiento."),
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
                    _option("corte", "No compartamos contenido de otra persona sin permiso. Voy a detener el reenvío.", "El mensaje marca el límite y no repite el contenido."),
                    _option("amenaza", "Si no borran esto, publicaré información de todos.", "Responder con otra exposición puede aumentar el daño y el riesgo."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Plan digital de recuperación",
                "Prepara pasos que puedes realizar sin subir información.",
                "La plataforma guarda solo las casillas completadas, nunca tus contraseñas, capturas o nombres de usuario.",
                "Marca cada paso cuando sepas cómo realizarlo:",
                (
                    _item("acceso", "Sé cómo cerrar sesiones y cambiar mi contraseña.", "Usa una clave única y activa un segundo factor cuando esté disponible."),
                    _item("copia", "Sé dónde conservar una copia privada de la evidencia.", "Evita carpetas compartidas o dispositivos a los que otras personas tengan acceso."),
                    _item("plataforma", "Sé cómo reportar y bloquear en la aplicación utilizada.", "Bloquear reduce el contacto; reportar solicita una revisión de la plataforma."),
                    _item("apoyo", "Tengo un canal para pedir acompañamiento.", "Una persona de confianza o un servicio universitario puede ayudarte a decidir los siguientes pasos."),
                ),
                "Tu plan digital básico está listo y no contiene datos privados.",
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
                    _option("devolver-idea", "Volver a la idea, pedir que se evalúe por su contenido y hablar con ella en privado después.", "Interrumpe el prejuicio sin exponer información adicional y permite acordar el siguiente paso."),
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
                    _item("comparacion", "¿A otras personas se les trata de la misma manera?", "Comparar situaciones semejantes permite observar diferencias de trato."),
                    _item("repeticion", "¿El comentario o la exclusión se repite?", "La repetición muestra que no fue solo un error corregido."),
                    _item("oportunidad", "¿Se perdió una oportunidad o participación?", "Las consecuencias concretas ayudan a explicar el impacto."),
                    _item("privacidad", "¿Se compartió información personal sin permiso?", "La identidad, salud o situación económica pertenecen a la persona."),
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
                    _option("hecho", "Quisiera que revisemos su propuesta por el contenido y que pueda terminar de explicarla.", "La frase devuelve la participación y se centra en una acción observable."),
                    _option("silencio", "Mejor no digamos nada para que ella no se sienta incómoda.", "El silencio puede dejar sola a la persona. También puedes acercarte después si intervenir no es seguro."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Plan de trato digno y apoyo",
                "Define opciones sin registrar tu identidad o situación personal.",
                "Solo se guardan los pasos seleccionados. No debes explicar aquí ninguna característica personal.",
                "Marca cada paso cuando tengas una opción:",
                (
                    _item("limite", "Tengo una frase de límite que podría usar si fuera seguro.", "Puedes pedir que vuelvan al tema académico o que respeten tu privacidad."),
                    _item("acompanamiento", "Sé quién podría acompañarme.", "El acompañamiento puede ser emocional, académico o institucional."),
                    _item("hechos", "Sé cómo describir hechos sin justificar mi identidad.", "Anota palabras, decisiones, fechas y consecuencias observables."),
                    _item("canal", "Conozco un canal que atienda igualdad, bienestar o inclusión.", "Puedes pedir información primero sin presentar una queja formal."),
                ),
                "Tu plan protege la privacidad y deja abiertas varias formas de pedir apoyo.",
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
                    _option("acuerdo-claro", "Definir horarios, un canal principal y pedir permiso antes de compartir contenido personal.", "Establece expectativas concretas y protege la privacidad desde el inicio."),
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
                    _item("privacidad", "Revisar quién puede ver y compartir mis publicaciones.", "Limitar la audiencia reduce exposiciones no deseadas."),
                    _item("etiquetas", "Elegir quién puede etiquetarme o mencionarme.", "Revisar etiquetas antes de publicarlas mantiene mayor control."),
                    _item("segundo-factor", "Activar un segundo factor de autenticación.", "Añade una barrera aunque alguien conozca tu contraseña."),
                    _item("sesiones", "Saber dónde revisar y cerrar sesiones abiertas.", "Permite responder rápido si un dispositivo se pierde o un acceso parece extraño."),
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
                    _option("limite", "No tengo permiso para compartirla. Podemos explicar el tema sin publicar la captura.", "Marca el límite y ofrece una alternativa que no expone a nadie."),
                    _option("ataque", "Si insistes, publicaré algo tuyo.", "Responder con otra amenaza crea un nuevo riesgo."),
                ),
            ),
            _item_activity(
                "safety_plan",
                "Plan preventivo de apoyo",
                "Prepara recursos que puedas usar más adelante.",
                "El plan no solicita detalles personales. Solo registra que identificaste cada tipo de recurso.",
                "Marca cada paso cuando tengas una opción:",
                (
                    _item("persona", "Tengo una persona de confianza.", "Puede escuchar, acompañar o ayudarte a ordenar opciones."),
                    _item("universidad", "Conozco un servicio de orientación de mi universidad.", "Puedes consultar cómo funciona antes de necesitarlo."),
                    _item("salida", "Sé cómo salir rápidamente de la plataforma.", "La tecla Escape y el botón de salida rápida protegen tu privacidad."),
                    _item("emergencia", "Sé a quién llamar ante un peligro inmediato.", "En Ecuador, el número único de emergencias es 9-1-1."),
                ),
                "Tu plan preventivo básico está listo y puedes revisarlo cuando cambien tus circunstancias.",
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
