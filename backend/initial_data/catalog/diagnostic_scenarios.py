"""Escenarios del perfil de orientación educativa.

El banco usa lenguaje cotidiano y una sola situación por pregunta. Cada
dimensión contiene cuatro escenarios y cada escenario ofrece los cuatro
valores de la escala ordinal: 0 (trato respetuoso), 1 (hecho aislado),
2 (conducta repetida) y 3 (presión, amenaza o exposición grave). El orden de
los valores cambia entre preguntas y nunca se muestra al participante.
"""

DIAGNOSTIC_SCENARIOS = (
    {
        "unit_slug": "acoso-vertical",
        "text": "Un profesor revisa un trabajo que tiene errores. ¿Qué suele ocurrir?",
        "options": (
            ("Explica los errores y permite que el estudiante pregunte o corrija.", 0),
            ("Muestra varias veces los errores del mismo estudiante frente a toda la clase.", 2),
            ("Hace una crítica fuerte una vez, pero después explica cómo mejorar.", 1),
            ("Se burla del estudiante y le dice que su nota puede bajar si reclama.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vertical",
        "text": "Un tutor envía mensajes sobre un proyecto fuera del horario acordado. ¿Qué pasa normalmente?",
        "options": (
            ("Espera respuestas por la noche o los fines de semana casi siempre.", 2),
            ("Respeta el horario y acuerda con tiempo cualquier cambio urgente.", 0),
            ("Envía un mensaje fuera de horario alguna vez, pero acepta que respondan después.", 1),
            ("Amenaza con bajar la nota o quitar oportunidades si no le responden de inmediato.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vertical",
        "text": "Un estudiante no está de acuerdo con una decisión de su profesor. ¿Cómo responde el profesor?",
        "options": (
            ("Mantiene su decisión sin explicar mucho, pero permite que el estudiante pregunte.", 1),
            ("Escucha al estudiante y responde usando las reglas o criterios de la materia.", 0),
            ("Le advierte que seguir preguntando puede afectar su nota o sus oportunidades.", 3),
            ("Dice varias veces que el estudiante es incapaz o problemático por no estar de acuerdo.", 2),
        ),
    },
    {
        "unit_slug": "acoso-vertical",
        "text": "En una materia se reparten ayudantías, proyectos o responsabilidades. ¿Cómo se elige a los estudiantes?",
        "options": (
            ("Se usan reglas claras relacionadas con habilidades, interés y tiempo disponible.", 0),
            ("Se elige varias veces a quienes aceptan estar disponibles a cualquier hora.", 2),
            ("Se ofrece una oportunidad a cambio de aceptar una petición personal que no tiene relación con la materia.", 3),
            ("La elección es informal, pero cualquier estudiante puede pedir una explicación.", 1),
        ),
    },
    {
        "unit_slug": "acoso-horizontal",
        "text": "La clase debe formar equipos para un proyecto importante. ¿Qué suele pasar?",
        "options": (
            ("Los mismos grupos dejan varias veces a ciertos estudiantes sin equipo o con tareas menores.", 2),
            ("Se consideran las habilidades, las preferencias de todos o se realiza un sorteo.", 0),
            ("Además de excluir a un estudiante, se burlan de él o dificultan su trabajo.", 3),
            ("Algunos eligen primero a sus amigos, pero ayudan a que todos encuentren equipo.", 1),
        ),
    },
    {
        "unit_slug": "acoso-horizontal",
        "text": "En un grupo usan un apodo que incomoda a un compañero. ¿Qué ocurre cuando pide que no lo usen?",
        "options": (
            ("Dejan de usarlo y respetan su decisión.", 0),
            ("Siguen usando el apodo en varias ocasiones aunque ya conocen su incomodidad.", 2),
            ("Alguien lo usa una vez más por error, se disculpa y lo corrige.", 1),
            ("Todo el grupo se organiza para repetirlo, burlarse y presionar a otros para que participen.", 3),
        ),
    },
    {
        "unit_slug": "acoso-horizontal",
        "text": "En una actividad de bienvenida, un estudiante no quiere realizar uno de los retos. ¿Cómo reacciona el grupo?",
        "options": (
            ("Insiste un poco, pero finalmente acepta la decisión del estudiante.", 1),
            ("Le exige realizar un acto humillante o peligroso y lo amenaza si se niega.", 3),
            ("Aclara que participar es opcional y respeta la decisión sin hacer comentarios.", 0),
            ("Lo deja fuera de varias actividades por haberse negado.", 2),
        ),
    },
    {
        "unit_slug": "acoso-horizontal",
        "text": "Dos compañeros tienen un desacuerdo durante un trabajo. ¿Qué sucede después?",
        "options": (
            ("Hablan directamente o piden ayuda para resolverlo con respeto.", 0),
            ("Varias personas se organizan para aislar a uno de ellos o dañar su trabajo.", 3),
            ("Aparece un comentario molesto una vez, pero la situación no continúa.", 1),
            ("Durante varios días circulan rumores o dejan fuera al mismo compañero.", 2),
        ),
    },
    {
        "unit_slug": "acoso-tecnologico",
        "text": "En el grupo de WhatsApp o la red social de la carrera comparten contenido sobre otros estudiantes. ¿Qué se publica?",
        "options": (
            ("Una broma aislada que se elimina cuando alguien dice que le incomoda.", 1),
            ("Fotos o mensajes privados usados para amenazar o presionar a un estudiante.", 3),
            ("Avisos, material de estudio y contenido que no expone a ningún compañero.", 0),
            ("Capturas o stickers que se burlan varias veces del mismo estudiante.", 2),
        ),
    },
    {
        "unit_slug": "acoso-tecnologico",
        "text": "Un estudiante se equivoca durante una exposición virtual. ¿Qué ocurre en los chats después?",
        "options": (
            ("El error se convierte durante varios días en bromas sobre ese estudiante.", 2),
            ("Lo ayudan con respeto o continúan la clase sin compartir el error.", 0),
            ("Difunden el error en muchos grupos junto con insultos o amenazas.", 3),
            ("Alguien hace un comentario aislado y después lo retira.", 1),
        ),
    },
    {
        "unit_slug": "acoso-tecnologico",
        "text": "Alguien quiere compartir una foto, captura o mensaje de un compañero. ¿Qué hace antes de publicarlo?",
        "options": (
            ("Pide permiso y respeta la respuesta del compañero.", 0),
            ("Usa el contenido privado para pedir algo a cambio de no publicarlo.", 3),
            ("Lo publica sin preguntar, pero lo elimina cuando el compañero se lo pide.", 1),
            ("Lo mantiene publicado o lo vuelve a enviar aunque el compañero pidió retirarlo.", 2),
        ),
    },
    {
        "unit_slug": "acoso-tecnologico",
        "text": "Un estudiante pide que dejen de enviarle mensajes y que retiren una publicación sobre él. ¿Qué sucede?",
        "options": (
            ("Tardan en responder, pero después detienen los mensajes y eliminan la publicación.", 1),
            ("Los mensajes o la publicación aparecen otra vez en diferentes grupos.", 2),
            ("Respetan la petición de inmediato y no toman represalias.", 0),
            ("Crean cuentas falsas, publican más información o envían amenazas.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vulnerabilidad",
        "text": "La universidad entrega una beca, ayudantía o cupo para un proyecto. ¿Cómo toma la decisión?",
        "options": (
            ("Aplica reglas publicadas y relacionadas con los méritos o las necesidades del estudiante.", 0),
            ("Repite ideas como que ciertos estudiantes sirven menos por su género, origen o condición.", 2),
            ("La decisión no es muy clara, pero los estudiantes pueden pedir que se la expliquen.", 1),
            ("Excluye directamente a un estudiante por una característica personal.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vulnerabilidad",
        "text": "Durante una conversación académica, alguien hace comentarios sobre la apariencia o la vida personal de un estudiante. ¿Qué ocurre?",
        "options": (
            ("Repite los comentarios aunque el estudiante ya mostró incomodidad.", 2),
            ("Mantiene la conversación en el tema académico y respeta la privacidad.", 0),
            ("Hace comentarios sexuales o discriminatorios y presiona al estudiante para que responda.", 3),
            ("Hace un comentario aislado y cambia de tema cuando nota la incomodidad.", 1),
        ),
    },
    {
        "unit_slug": "acoso-vulnerabilidad",
        "text": "Un estudiante informa que necesita apoyo por una situación de salud, discapacidad o falta de recursos. ¿Cómo responden?",
        "options": (
            ("Le piden explicar lo mismo varias veces, pero finalmente atienden su solicitud.", 1),
            ("Se burlan o ponen en duda su situación delante de otras personas varias veces.", 2),
            ("Atienden la solicitud con respeto y sin contar información privada a otros.", 0),
            ("Le niegan oportunidades o lo amenazan por haber pedido el apoyo.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vulnerabilidad",
        "text": "En una reunión de grupo, un estudiante presenta una idea. ¿Cómo reaccionan los demás?",
        "options": (
            ("Escuchan la idea y la valoran por su contenido.", 0),
            ("La rechazan varias veces con comentarios sobre su género, origen o situación personal.", 2),
            ("Lo interrumpen una vez, se dan cuenta y le permiten continuar.", 1),
            ("Se organizan para callarlo, insultarlo o dejarlo fuera por una característica personal.", 3),
        ),
    },
)
