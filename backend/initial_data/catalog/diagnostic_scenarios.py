"""Banco de escenarios del perfil de orientación educativa.

Cada dimensión contiene cuatro escenarios y cada alternativa utiliza la misma
escala ordinal: 0 (dinámica saludable), 1 (situación aislada o ambigua),
2 (patrón repetido) y 3 (situación de mayor intensidad). Estos valores nunca
se exponen al participante.
"""

DIAGNOSTIC_SCENARIOS = (
    {
        "unit_slug": "acoso-vertical",
        "text": "Cuando una persona docente revisa un trabajo con errores, ¿qué suele ocurrir en tu entorno?",
        "options": (
            ("Explica los criterios en privado y permite hacer preguntas o correcciones.", 0),
            ("Da una respuesta brusca en alguna ocasión, pero luego aclara los criterios.", 1),
            ("Expone con frecuencia los errores individuales frente al grupo para presionar.", 2),
            ("Ridiculiza a la persona o relaciona el error con amenazas sobre su calificación.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vertical",
        "text": "En un proyecto con tutoría, ¿cómo se maneja normalmente la disponibilidad fuera del horario acordado?",
        "options": (
            ("Se respetan los horarios y las urgencias se acuerdan con anticipación.", 0),
            ("A veces llega una solicitud fuera de horario, pero no responder de inmediato no genera consecuencias.", 1),
            ("Se espera con frecuencia una respuesta nocturna o de fin de semana como señal de compromiso.", 2),
            ("No responder de inmediato provoca amenazas, represalias o cambios negativos en la evaluación.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vertical",
        "text": "Si un estudiante no está de acuerdo con una decisión académica, ¿cómo suele desarrollarse la conversación?",
        "options": (
            ("Puede explicar su punto de vista y recibe una respuesta basada en criterios conocidos.", 0),
            ("La decisión se mantiene sin mucha explicación, pero no hay consecuencias por preguntar.", 1),
            ("Se cuestiona repetidamente su capacidad o actitud por haber expresado el desacuerdo.", 2),
            ("Se le advierte que insistir puede afectar su nota, permanencia u oportunidades.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vertical",
        "text": "Cuando se asignan responsabilidades u oportunidades dentro de una cátedra, ¿qué dinámica observas?",
        "options": (
            ("Se usan criterios transparentes relacionados con habilidades, interés y disponibilidad acordada.", 0),
            ("Algunas decisiones son informales, aunque se pueden pedir aclaraciones sin problema.", 1),
            ("Se favorece repetidamente a quienes aceptan una cercanía o disponibilidad sin límites.", 2),
            ("Una oportunidad se condiciona a aceptar presiones personales o conductas ajenas al trabajo académico.", 3),
        ),
    },
    {
        "unit_slug": "acoso-horizontal",
        "text": "Cuando se forman equipos para un proyecto importante, ¿cómo se decide quién participa?",
        "options": (
            ("Se consideran habilidades complementarias, preferencias abiertas o un sorteo.", 0),
            ("Predomina la afinidad personal, pero se buscan alternativas para quienes quedan fuera.", 1),
            ("Los mismos grupos dejan repetidamente a ciertas personas sin equipo o con tareas menores.", 2),
            ("La exclusión se acompaña de burlas, rumores o acciones que perjudican el rendimiento académico.", 3),
        ),
    },
    {
        "unit_slug": "acoso-horizontal",
        "text": "En tu grupo aparecen apodos o bromas sobre una persona. ¿Qué pasa si muestra incomodidad?",
        "options": (
            ("La broma solo continúa si todas las personas están cómodas y se detiene al primer límite.", 0),
            ("Ocurre una vez y quien la hizo se disculpa o corrige su conducta.", 1),
            ("La broma continúa en varias ocasiones aunque la persona ya pidió que se detenga.", 2),
            ("El grupo coordina burlas o humillaciones y presiona a otras personas para que participen.", 3),
        ),
    },
    {
        "unit_slug": "acoso-horizontal",
        "text": "En una actividad de bienvenida organizada por estudiantes, ¿cómo se trata a quien no desea participar en un reto?",
        "options": (
            ("La participación es opcional y la decisión se respeta sin comentarios ni consecuencias.", 0),
            ("Hay cierta insistencia, pero el rechazo finalmente se acepta.", 1),
            ("Negarse provoca exclusión repetida de actividades o del grupo.", 2),
            ("Se exigen actos humillantes o riesgosos y se amenaza con consecuencias si alguien se niega.", 3),
        ),
    },
    {
        "unit_slug": "acoso-horizontal",
        "text": "Después de un desacuerdo entre compañeros, ¿qué sucede habitualmente?",
        "options": (
            ("Las personas conversan directamente o buscan una mediación respetuosa.", 0),
            ("Aparece algún comentario aislado, pero no se mantiene en el tiempo.", 1),
            ("Circulan rumores o se excluye repetidamente a una persona de las actividades.", 2),
            ("Varias personas coordinan ataques, aislamiento o interferencias con su trabajo académico.", 3),
        ),
    },
    {
        "unit_slug": "acoso-tecnologico",
        "text": "En los grupos digitales de tu entorno académico, ¿qué tipo de contenido sobre estudiantes suele circular?",
        "options": (
            ("Avisos, material de estudio y contenido general que no identifica ni expone a nadie.", 0),
            ("Alguna broma aislada que no señala a una persona y se elimina si incomoda.", 1),
            ("Capturas o stickers basados repetidamente en errores o fotografías de compañeros.", 2),
            ("Contenido privado, íntimo o amenazante difundido para avergonzar o controlar a alguien.", 3),
        ),
    },
    {
        "unit_slug": "acoso-tecnologico",
        "text": "Si alguien se equivoca durante una actividad virtual, ¿cómo reaccionan los canales digitales paralelos?",
        "options": (
            ("Se responde con respeto o se continúa con la actividad sin amplificar el error.", 0),
            ("Aparece un comentario aislado que luego se retira o no vuelve a repetirse.", 1),
            ("El error se convierte durante varios días en bromas dirigidas a la misma persona.", 2),
            ("Se difunde de forma masiva junto con insultos, amenazas o llamados a atacar a la persona.", 3),
        ),
    },
    {
        "unit_slug": "acoso-tecnologico",
        "text": "Antes de compartir una fotografía, captura o mensaje de otra persona, ¿qué práctica predomina?",
        "options": (
            ("Se pide autorización explícita y se respeta la respuesta.", 0),
            ("Alguien asume que puede compartirlo, pero lo retira de inmediato al recibir una solicitud.", 1),
            ("Se comparte sin permiso y permanece disponible aunque la persona pida retirarlo.", 2),
            ("Se usa contenido privado para amenazar, presionar o exigir algo a cambio.", 3),
        ),
    },
    {
        "unit_slug": "acoso-tecnologico",
        "text": "Cuando una persona pide que dejen de contactarla o que retiren una publicación, ¿qué ocurre?",
        "options": (
            ("El contacto se detiene y el contenido se elimina sin represalias.", 0),
            ("La respuesta tarda, pero finalmente se respeta la solicitud.", 1),
            ("El contenido o los mensajes reaparecen en otros canales de manera repetida.", 2),
            ("La situación aumenta mediante cuentas falsas, amenazas o divulgación de más información.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vulnerabilidad",
        "text": "Al asignar becas, ayudantías o cupos, ¿qué criterios parecen influir en la decisión?",
        "options": (
            ("Se aplican criterios publicados y relacionados con méritos o necesidades verificables.", 0),
            ("Existen apreciaciones subjetivas, pero la decisión puede revisarse o explicarse.", 1),
            ("Los estereotipos sobre origen, género o condición influyen repetidamente en las oportunidades.", 2),
            ("Se excluye de forma explícita a una persona por una característica personal.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vulnerabilidad",
        "text": "En conversaciones académicas individuales, ¿cómo se manejan los comentarios sobre la vida o apariencia personal?",
        "options": (
            ("La conversación se mantiene en el ámbito académico y respeta la privacidad.", 0),
            ("Surge un comentario aislado y se detiene cuando la persona cambia de tema o marca un límite.", 1),
            ("Se repiten preguntas o comentarios personales aunque ya causaron incomodidad.", 2),
            ("Se realizan comentarios sexuales o discriminatorios, o se presiona para obtener una respuesta personal.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vulnerabilidad",
        "text": "Si alguien necesita una adaptación por discapacidad, salud o situación económica, ¿cómo responde el entorno?",
        "options": (
            ("La necesidad se gestiona con respeto, privacidad y los canales disponibles.", 0),
            ("La persona debe explicar su necesidad más de una vez, pero finalmente recibe atención.", 1),
            ("Su situación se cuestiona o ridiculiza repetidamente delante de otras personas.", 2),
            ("Se le niegan oportunidades o se le amenaza debido a esa condición.", 3),
        ),
    },
    {
        "unit_slug": "acoso-vulnerabilidad",
        "text": "Durante reuniones o trabajos grupales, ¿cómo se reciben las ideas de personas con experiencias distintas?",
        "options": (
            ("Las ideas se valoran por su contenido y se distribuyen los turnos de participación.", 0),
            ("Hay interrupciones ocasionales, pero se corrigen y la persona puede continuar.", 1),
            ("Sus aportes se minimizan repetidamente mediante comentarios sobre su identidad o procedencia.", 2),
            ("El grupo coordina el silenciamiento, la hostilidad o la exclusión por una característica personal.", 3),
        ),
    },
)
