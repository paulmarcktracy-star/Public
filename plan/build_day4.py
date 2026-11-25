"""Videos 8, 9, 10, 11. Hooks verbatim. Natural spoken Spanish. Cinematic camera."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbkit import cam, crowd, fig, prop, sb, scene, shot, stage, text, write  # noqa: E402

CTA = lambda q, last="Te leo en los comentarios.", word="Te leo": scene("I", "cta", [  # noqa: E731
    shot(q, stage(figure=fig("lookUp", 540, path="flat"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.3)])),
    shot(last, stage(texts=[text(word, family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
])

# ------------------------------------------------------------------ 008 present bias / future self
v8 = sb(
    "008-sesgo-presente", "El sesgo del presente: tu yo del futuro es casi un desconocido", 2,
    [
        {"citation": "Ersner-Hershfield, H., Wimmer, G. E., & Knutson, B. (2009). Saving for the future self: Neural measures of future self-continuity predict temporal discounting. Social Cognitive and Affective Neuroscience, 4(1), 85–92.",
         "doi": "10.1093/scan/nsn042", "supports": "Pensar en el yo futuro se parece, en el cerebro, a pensar en otra persona; quienes muestran más distancia son más impacientes con el dinero."},
        {"citation": "Hershfield, H. E., et al. (2011). Increasing saving behavior through age-progressed renderings of the future self. Journal of Marketing Research, 48(SPL), S23–S37.",
         "doi": "10.1509/jmkr.48.SPL.S23", "supports": "Ver una imagen envejecida de uno mismo aumentó la asignación al ahorro en una decisión de prueba."},
    ],
    [
        scene("A", "hook", [
            shot("Para tu cerebro, tu yo del futuro es casi un desconocido.", stage(
                spotlight={"x": 380, "snap": True}, figure=fig("stand", 380, path="fade", pathTo=980),
                extras=[fig("stand", 820, facing=-1, opacity=0.25)], texts=[text("Tu yo del futuro", emphasis=["futuro"])], camera=cam(1.0, 1.06)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Por qué le dejas los problemas al tú de mañana, como si fuera otra persona?", stage(
                figure=fig("reach", 380, path="flat"), extras=[fig("slump", 800, facing=-1, opacity=0.3)],
                props=[prop("book", 600, 640, size=110, enter="pop", to={"x": 760, "y": 640, "at": 0.4})])),
        ]),
        scene("C", "mechanism", [
            shot("Se llama sesgo del presente: lo de hoy pesa más que lo de mañana.", stage(
                props=[prop("balance", 540, 720, size=240, enter="none", to={"state": "down", "at": 0.3})],
                texts=[text("Hoy", x=420, y=540, family="sans", size=40), text("Mañana", x=660, y=540, family="sans", size=40), text("Sesgo del presente", family="sans", size=50)])),
            shot("En un estudio con resonancia magnética, pensar en tu yo futuro", stage(
                props=[prop("brain", 540, 600, size=220, state="glow", enter="draw")])),
            shot("activaba el cerebro de forma más parecida a pensar en otra persona.", stage(
                figure=fig("stand", 360), extras=[fig("stand", 720, facing=-1, opacity=0.35)],
                props=[prop("brain", 540, 440, size=110, state="glow", enter="pop")], texts=[text("Como otra persona", family="sans", size=52, emphasis=["otra"])])),
        ]),
        scene("D", "demonstration", [
            shot("Y quienes sentían más lejos a ese desconocido eran más impacientes con el dinero.", stage(
                figure=fig("reach", 400), props=[prop("coins", 640, 640, size=130, enter="pop"), prop("clock", 820, 480, size=90, state="spin", enter="pop", delay=0.5)])),
        ]),
        scene("E", "retention", [
            shot("Entonces, ¿qué pasa si conoces a ese desconocido?", stage(
                figure=fig("stand", 380, path="fade", pathTo=980), extras=[fig("stand", 760, facing=-1, opacity=0.35)],
                props=[prop("question", 760, 440, size=80, enter="pop", delay=0.4)])),
        ]),
        scene("F", "reveal", [
            shot("En otro experimento, algunas personas vieron una imagen envejecida de sí mismas.", stage(
                figure=fig("stand", 400), extras=[fig("stand", 680, facing=-1, opacity=0.9, scale=0.95)],
                props=[prop("phone", 540, 500, size=110, enter="pop", delay=0.3)])),
            shot("Y en una decisión de prueba, destinaron más dinero al ahorro.", stage(
                props=[prop("piggy", 540, 640, size=190, enter="drop", accent="reward"), prop("coins", 540, 420, size=90, enter="drop", delay=0.6)],
                texts=[text("Más ahorro", emphasis=["ahorro"])])),
        ]),
        scene("G", "action", [
            shot("Así que haz visible a tu yo futuro: escríbele una carta, con fecha.", stage(
                figure=fig("phone", 420, holding="phone"), props=[prop("calendar", 740, 600, size=140, label="2036", enter="draw")])),
            shot("Y antes de decidir, pregúntate: ¿qué le estoy dejando?", stage(
                figure=fig("walk", 300, toX=520, path="rise"), extras=[fig("stand", 800, facing=-1, opacity=0.7)],
                texts=[text("¿Qué le estoy dejando?", family="sans", size=52)])),
        ]),
        scene("H", "closer", [
            shot("Tu yo del futuro no es un extraño.", stage(
                figure=fig("stand", 380, path="flat", pathTo=760), extras=[fig("stand", 760, facing=-1, opacity=0.6)])),
            shot("Es la persona en la que te vas a convertir.", stage(
                figure=fig("walk", 360, toX=520, path="flat", pathTo=760), extras=[fig("walk", 760, toX=600, facing=-1, opacity=1)],
                texts=[text("No es un extraño", emphasis=["extraño"])], camera=cam(1.0, 1.08))),
        ]),
        CTA("Si pudieras dejarle un mensaje a tu yo de dentro de diez años, ¿qué le dirías?", "Escríbelo abajo.", "Escríbelo"),
    ],
    "Para tu cerebro, tu yo del futuro es casi un desconocido 🧠 Y hay una forma sencilla de presentarte a esa persona.",
    ["#psicologia", "#futuro", "#ahorro", "#habitos", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 009 two-minute rule
v9 = sb(
    "009-regla-dos-minutos", "La regla de los dos minutos: cómo vencer la resistencia a empezar", 2,
    [
        {"citation": "Steel, P. (2007). The nature of procrastination: A meta-analytic and theoretical review of quintessential self-regulatory failure. Psychological Bulletin, 133(1), 65–94.",
         "doi": "10.1037/0033-2909.133.1.65", "supports": "Postergamos más las tareas que nos resultan desagradables (aversión a la tarea)."},
        {"citation": "Sirois, F., & Pychyl, T. (2013). Procrastination and the priority of short-term mood regulation. Social and Personality Psychology Compass, 7(2), 115–127.",
         "doi": "10.1111/spc3.12011", "supports": "La procrastinación funciona como reparación del ánimo a corto plazo."},
        {"citation": "Gollwitzer, P. M., & Sheeran, P. (2006). Implementation intentions and goal achievement: A meta-analysis of effects and processes. Advances in Experimental Social Psychology, 38, 69–119.",
         "doi": "10.1016/S0065-2601(06)38002-1", "supports": "Planes «si–entonces»: efecto de tamaño medio a grande en 94 estudios."},
    ],
    [
        scene("A", "hook", [
            shot("Llevas diez días evitando una tarea que podrías empezar en solo dos minutos.", stage(
                spotlight={"x": 360, "snap": True}, figure=fig("slump", 360, path="flat"),
                props=[prop("calendar", 700, 520, size=130, label="10", enter="none"), prop("clock", 700, 760, size=110, state="spin", enter="pop", delay=1.6)],
                texts=[text("10 días… para 2 minutos", family="sans", size=52, emphasis=["2 minutos"])], camera=cam(1.0, 1.06)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Por qué empezar cuesta tanto más que hacer?", stage(
                figure=fig("stand", 400, path="rise"), props=[prop("door", 720, 600, size=170, state="closed", enter="pop"), prop("question", 720, 420, size=70, enter="pop", delay=0.6)])),
        ]),
        scene("C", "mechanism", [
            shot("Un metaanálisis sobre la procrastinación encontró que postergamos más lo que nos resulta desagradable.", stage(
                props=[prop("checklist", 540, 640, size=190, state="closed", enter="draw")], texts=[text("Lo desagradable, para después", family="sans", size=46)])),
            shot("Y otros investigadores lo explican así: evitas la tarea para no sentir esa incomodidad ahora.", stage(
                figure=fig("phone", 420, holding="phone"), props=[prop("phone", 720, 600, size=130, state="typing", enter="pop")])),
        ]),
        scene("D", "demonstration", [
            shot("La regla de los dos minutos ataca justo eso.", {"type": "kineticTitle", "kicker": "La regla", "lines": ["De los dos", "minutos"], "emphasis": ["minutos"]}, "impact"),
            shot("Si algo toma menos de dos minutos, hazlo ya.", stage(
                figure=fig("reach", 400), props=[prop("checklist", 700, 600, size=150, state="normal", enter="pop", mark="check", markAt=0.6)])),
            shot("Y si es grande, haz solo los primeros dos: abre el documento, escribe una línea.", stage(
                figure=fig("walk", 300, toX=500, path="rise"), props=[prop("book", 760, 620, size=140, state="open", enter="draw", delay=0.5)])),
        ]),
        scene("E", "retention", [
            shot("Pero ojo, ¿la ciencia la respalda?", stage(
                props=[prop("clock", 540, 620, size=180, enter="pop"), prop("question", 540, 420, size=80, enter="pop", delay=0.4)])),
        ]),
        scene("F", "reveal", [
            shot("La regla, tal cual, no se ha probado en experimentos.", stage(
                props=[prop("chart", 540, 640, size=180, enter="draw", mark="question", markAt=0.5)], texts=[text("No probada tal cual", family="sans", size=50)])),
            shot("Pero se apoya en algo que sí: decidir de antemano cuándo y dónde vas a empezar.", stage(
                figure=fig("think", 380), props=[prop("calendar", 700, 600, size=130, label="7:00", enter="draw")])),
            shot("En 94 estudios, esos planes de «si pasa esto, hago aquello» funcionaron bien.", stage(
                counters=[{"from": 0, "to": 94, "x": 540, "y": 560, "size": 140, "seconds": 1.2, "suffix": " estudios", "accent": "reward"}],
                texts=[text("«Si son las 7, empiezo»", y=760, family="sans", size=44)])),
        ]),
        scene("G", "action", [
            shot("Hoy, elige una tarea que llevas días evitando.", stage(
                figure=fig("think", 400, path="flat"), props=[prop("checklist", 720, 600, size=150, state="closed", enter="pop")])),
            shot("Escribe: «si son las siete, hago los primeros dos minutos». Solo dos.", stage(
                figure=fig("walk", 300, toX=520, path="rise"), props=[prop("clock", 780, 560, size=110, enter="pop")],
                counters=[{"from": 0, "to": 2, "x": 780, "y": 760, "size": 90, "seconds": 0.4, "suffix": " min"}])),
        ]),
        scene("H", "closer", [
            shot("No necesitas motivación para empezar. Necesitas que empezar sea más fácil que evitarlo.",
                 {"type": "closer", "line": "Haz que empezar sea más fácil que evitarlo.", "emphasis": ["empezar"], "source": "Steel, 2007 · Gollwitzer y Sheeran, 2006"}, "shimmer"),
        ]),
        CTA("¿Qué tarea vas a empezar con tus dos minutos?", "Escríbela en los comentarios.", "Escríbela"),
    ],
    "Llevas días evitando algo que podrías empezar en 2 minutos ⏱️ La regla funciona, pero no por la razón que crees.",
    ["#psicologia", "#procrastinacion", "#productividad", "#habitos", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 010 halo effect
v10 = sb(
    "010-efecto-halo", "El efecto halo: cómo una primera impresión lo cambia todo", 3,
    [
        {"citation": "Willis, J., & Todorov, A. (2006). First impressions: Making up your mind after a 100-ms exposure to a face. Psychological Science, 17(7), 592–598.",
         "doi": "10.1111/j.1467-9280.2006.01750.x", "supports": "Una décima de segundo basta para formarse una impresión de una cara."},
        {"citation": "Thorndike, E. L. (1920). A constant error in psychological ratings. Journal of Applied Psychology, 4(1), 25–29.",
         "doi": "10.1037/h0071663", "supports": "Calificaciones de oficiales sospechosamente uniformes: el efecto halo."},
        {"citation": "Langlois, J. H., et al. (2000). Maxims or myths of beauty? A meta-analytic and theoretical review. Psychological Bulletin, 126(3), 390–423.",
         "doi": "10.1037/0033-2909.126.3.390", "supports": "Metaanálisis: a las personas atractivas se les atribuyen otras cualidades positivas."},
        {"citation": "Nisbett, R. E., & Wilson, T. D. (1977). The halo effect: Evidence for unconscious alteration of judgments. Journal of Personality and Social Psychology, 35(4), 250–256.",
         "doi": "10.1037/0022-3514.35.4.250", "supports": "Profesor cálido vs frío: cambia la evaluación de apariencia, gestos y acento; los estudiantes negaron la influencia e incluso la invirtieron."},
    ],
    [
        scene("A", "hook", [
            shot("Te basta una décima de segundo para juzgar a alguien.", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("stand", 540, path="flat"),
                counters=[{"from": 0, "to": 100, "suffix": " ms", "x": 540, "y": 460, "size": 90, "seconds": 0.5}], camera=cam(1.0, 1.06)), "impact"),
            shot("Y ese juicio contamina todo lo demás.", stage(
                figure=fig("stand", 540), props=[prop("lightbulb", 540, 420, size=110, state="glow", enter="pop")],
                texts=[text("Contamina todo", emphasis=["todo"])])),
        ]),
        scene("B", "question", [
            shot("¿Por qué, si alguien nos cae bien, también nos parece más inteligente?", stage(
                figure=fig("stand", 540), props=[prop("brain", 760, 480, size=100, state="glow", enter="pop", delay=0.5), prop("question", 340, 480, size=70, enter="pop", delay=0.9)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1920, Edward Thorndike notó algo raro en cómo unos oficiales calificaban a sus soldados.", stage(
                extras=crowd([240, 390, 540, 690, 840], opacity=0.6, scale=0.7), texts=[text("Thorndike · 1920", family="sans", size=46)])),
            shot("Si uno parecía bueno en algo, lo calificaban bien en todo.", stage(
                props=[prop("chart", 540, 620, size=200, state="up", enter="draw")], texts=[text("Bueno en algo = bueno en todo", family="sans", size=46)])),
            shot("Lo llamó efecto halo.", {"type": "kineticTitle", "kicker": "Lo llamó", "lines": ["Efecto", "halo"], "emphasis": ["halo"]}, "impact"),
        ]),
        scene("D", "demonstration", [
            shot("Y un metaanálisis encontró que a las personas atractivas también se les atribuyen otras virtudes.", stage(
                figure=fig("stand", 540), props=[prop("lightbulb", 380, 480, size=80, state="glow", enter="pop", delay=0.4), prop("book", 700, 480, size=90, enter="pop", delay=0.8)])),
        ]),
        scene("E", "retention", [
            shot("Pero lo más inquietante no es el sesgo.", stage(
                figure=fig("stand", 540, path="fade"), props=[prop("question", 540, 420, size=80, enter="pop", delay=0.3)], camera=cam(1.0, 1.08))),
        ]),
        scene("F", "reveal", [
            shot("En 1977, unos estudiantes vieron a un profesor ser amable o frío.", stage(
                figure=fig("point", 380), extras=[fig("point", 720, facing=-1, opacity=0.5)],
                texts=[text("Amable", x=380, y=560, family="sans", size=40), text("Frío", x=720, y=560, family="sans", size=40, accent="red")])),
            shot("Con el profesor amable, hasta su acento les pareció más agradable.", stage(
                figure=fig("point", 540), props=[prop("bubble", 720, 480, size=110, enter="pop", delay=0.3)])),
            shot("Y lo más fuerte: negaron que la simpatía hubiera influido. Creían que había sido al revés.", stage(
                props=[prop("balance", 540, 720, size=230, enter="none", to={"state": "up", "at": 0.3}), prop("question", 540, 440, size=80, enter="pop", delay=1.0, accent="reward")],
                texts=[text("No lo notaron", emphasis=["No"])])),
        ]),
        scene("G", "action", [
            shot("Así que, antes de juzgar algo importante, como una entrevista o una cita,", stage(
                figure=fig("think", 400), extras=[fig("stand", 720, facing=-1, opacity=0.8)])),
            shot("evalúa cada cualidad por separado, como si fueran personas distintas.", stage(
                props=[prop("checklist", 540, 640, size=180, state="open", enter="draw")], texts=[text("Una cualidad a la vez", family="sans", size=50)])),
        ]),
        scene("H", "closer", [
            shot("La primera impresión no es una foto. Es un filtro.",
                 {"type": "closer", "line": "La primera impresión no es una foto. Es un filtro.", "emphasis": ["filtro"], "source": "Thorndike, 1920 · Nisbett y Wilson, 1977"}, "shimmer"),
        ]),
        CTA("¿Alguna vez tu primera impresión de alguien estuvo totalmente equivocada?", "Cuéntamelo en los comentarios.", "Cuéntamelo"),
    ],
    "Te basta una décima de segundo para juzgar a alguien 👀 Y lo más inquietante es que no te das cuenta de cuánto te influye.",
    ["#psicologia", "#primeraimpresion", "#sesgos", "#relaciones", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 011 reciprocity
v11 = sb(
    "011-reciprocidad", "La reciprocidad: por qué un favor pequeño te hace decir que sí", 3,
    [
        {"citation": "Gouldner, A. W. (1960). The norm of reciprocity: A preliminary statement. American Sociological Review, 25(2), 161–178.",
         "doi": "10.2307/2092623", "supports": "La reciprocidad como norma presente en muchas culturas."},
        {"citation": "Regan, D. T. (1971). Effects of a favor and liking on compliance. Journal of Experimental Social Psychology, 7(6), 627–639.",
         "doi": "10.1016/0022-1031(71)90025-4", "supports": "Tras recibir una gaseosa, los participantes compraron más boletos; con favor de por medio, el agrado casi no cambiaba la compra."},
    ],
    [
        scene("A", "hook", [
            shot("¿Alguna vez aceptaste algo solo porque alguien te había hecho un favor?", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("reach", 400, path="flat", pathTo=760), extras=[fig("reach", 680, facing=-1, opacity=0.9)],
                props=[prop("bubble", 540, 480, size=100, enter="none")], texts=[text("Solo por un favor", emphasis=["favor"])], camera=cam(1.0, 1.06)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Por qué sentimos que hay que devolver un favor, aunque no lo hayamos pedido?", stage(
                figure=fig("think", 400), extras=[fig("stand", 700, facing=-1, opacity=0.8)], props=[prop("question", 540, 440, size=80, enter="pop", delay=0.5)])),
        ]),
        scene("C", "mechanism", [
            shot("El sociólogo Alvin Gouldner lo describió como una regla que aparece en muchas culturas:", stage(
                extras=crowd([220, 380, 540, 700, 860], opacity=0.6, scale=0.72))),
            shot("si alguien te da algo, le debes algo.", stage(
                props=[prop("balance", 540, 720, size=230, enter="none", to={"state": "down", "at": 0.3})],
                texts=[text("Te dan → debes", family="sans", size=54, emphasis=["debes"])])),
        ]),
        scene("D", "demonstration", [
            shot("En 1971, en un experimento, un desconocido le regalaba una gaseosa a un participante.", stage(
                figure=fig("reach", 400), extras=[fig("reach", 680, facing=-1, opacity=0.9)], props=[prop("phone", 540, 560, size=60, enter="pop", to={"x": 450, "y": 560, "at": 0.5})])),
            shot("Después le pedía que le comprara boletos para una rifa.", stage(
                props=[prop("tag", 540, 620, size=160, label="RIFA", enter="draw")])),
            shot("Y quienes habían recibido la gaseosa compraron más boletos.", stage(
                props=[prop("tag", 380, 640, size=110, label="RIFA", enter="none"), prop("chart", 700, 600, size=150, state="up", enter="draw", delay=0.3)])),
        ]),
        scene("E", "retention", [
            shot("Parece lógico: les caía bien. Pero no.", stage(
                figure=fig("stand", 540), props=[prop("bubble", 540, 440, size=100, enter="pop", mark="cross", markAt=0.6)])),
        ]),
        scene("F", "reveal", [
            shot("Con el favor de por medio, que esa persona les cayera bien o mal", stage(
                figure=fig("stand", 400), extras=[fig("stand", 700, facing=-1, opacity=0.8)], props=[prop("gauge", 550, 460, size=110, state="spin", enter="pop")])),
            shot("casi no cambiaba lo que compraban.", stage(
                props=[prop("gauge", 380, 560, size=130, state="spin", enter="pop"), prop("tag", 720, 600, size=120, label="RIFA", enter="pop", delay=0.4)],
                texts=[text("El agrado casi no importaba", family="sans", size=46)])),
            shot("La deuda pesaba más que la simpatía.", stage(
                props=[prop("balance", 540, 720, size=250, enter="none", to={"state": "down", "at": 0.25})],
                texts=[text("Deuda", x=420, y=540, family="sans", size=40, accent="reward"), text("Simpatía", x=660, y=540, family="sans", size=40)], camera=cam(1.0, 1.1))),
        ]),
        scene("G", "action", [
            shot("Así que, cuando recibas algo «gratis» seguido de una petición, haz una pausa.", stage(
                figure=fig("stand", 400), props=[prop("tag", 700, 560, size=130, label="GRATIS", enter="pop")])),
            shot("Pregúntate: ¿lo haría si no me hubieran dado nada?", stage(
                figure=fig("think", 540, path="fork"), texts=[text("¿Lo haría igual?", family="sans", size=54)])),
            shot("Y úsala para bien: da primero, sin esperar nada.", stage(
                figure=fig("walk", 300, toX=480, path="flat"), extras=[fig("stand", 760, facing=-1, opacity=0.9)])),
        ]),
        scene("H", "closer", [
            shot("La reciprocidad construyó la confianza entre humanos.", stage(
                extras=crowd([300, 440, 640, 780], opacity=0.7, scale=0.8, facing=[1, 1, -1, -1]))),
            shot("Asegúrate de usarla tú… y de que no te usen a ti.",
                 {"type": "closer", "line": "Úsala tú. Que no te usen a ti.", "emphasis": ["tú"], "source": "Gouldner, 1960 · Regan, 1971"}, "shimmer"),
        ]),
        CTA("¿Cuál es el favor más pequeño que te hizo sentir en deuda?", "Cuéntame en los comentarios.", "Cuéntame"),
    ],
    "Un favor pequeño puede hacerte decir que sí a algo que no querías 🎁 Y no es porque te caiga bien.",
    ["#psicologia", "#persuasion", "#relaciones", "#ventas", "#aprendeentiktok"],
)

write(v8, v9, v10, v11)
