"""Day 2 storyboards (videos 16, 14, 5). Hooks are the owner's, verbatim. Natural, spoken Spanish."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbkit import cam, crowd, fig, prop, sb, scene, shot, stage, text, write  # noqa: E402

# ------------------------------------------------------------------ 016 Zeigarnik (myth vs evidence)
v016 = sb(
    "016-efecto-zeigarnik",
    "El efecto Zeigarnik: lo que dejas a medias no ocupa tu mente por la razón que crees",
    1,
    [
        {"citation": "Ghibellini, R., & Meier, B. (2025). Interruption, recall and resumption: A meta-analysis of the Zeigarnik and Ovsiankina effects. Humanities and Social Sciences Communications, 12.",
         "doi": "10.1057/s41599-025-05000-w",
         "supports": "Casi un siglo de estudios: no hay una ventaja general de memoria para tareas interrumpidas (Zeigarnik); sí una tendencia general a retomarlas (Ovsiankina)."},
    ],
    [
        scene("A", "hook", [
            shot("Lo que dejas sin terminar puede seguir ocupando tu mente.", stage(
                spotlight={"x": 600, "snap": True}, figure=fig("think", 380, path="flat"),
                props=[prop("checklist", 660, 640, size=200, state="normal", enter="none")],
                texts=[text("Lo que dejas a medias", emphasis=["a medias"])], camera=cam(1.0, 1.08)), "impact"),
            shot("Pero no por la razón que crees.", stage(
                figure=fig("think", 380, path="flat"), props=[prop("checklist", 660, 640, size=200, enter="none", mark="question", markAt=0.4)],
                texts=[text("No por lo que crees", family="sans", size=56, emphasis=["No"])])),
        ]),
        scene("B", "question", [
            shot("Entonces, ¿por qué lo pendiente no te deja tranquilo?", stage(
                figure=fig("slump", 540, path="flat"), props=[prop("bubble", 700, 500, size=130, enter="pop", delay=0.3), prop("question", 700, 360, size=80, enter="pop", delay=0.8)],
                texts=[text("¿Por qué no te suelta?", family="sans", size=56)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1927, la psicóloga Bluma Zeigarnik interrumpía a personas mientras hacían tareas pequeñas.", stage(
                figure=fig("reach", 320), props=[prop("checklist", 640, 620, size=180, enter="draw"), prop("clock", 860, 460, size=100, enter="pop", delay=0.6)],
                texts=[text("Bluma Zeigarnik · 1927", family="sans", size=46)])),
            shot("Después, parecían recordar mejor las tareas que no habían terminado.", stage(
                props=[prop("checklist", 400, 640, size=170, state="open", enter="pop"), prop("checklist", 700, 640, size=170, state="normal", enter="pop", delay=0.3, accent="white")],
                texts=[text("Terminadas", x=400, y=800, family="sans", size=34), text("A medias", x=700, y=800, family="sans", size=34),
                       text("¿Se recuerda mejor lo pendiente?", family="sans", size=48)])),
            shot("Así nació el famoso efecto Zeigarnik.", {"type": "kineticTitle", "kicker": "Así nació", "lines": ["El efecto", "Zeigarnik"], "emphasis": ["Zeigarnik"]}, "impact"),
        ]),
        scene("D", "retention", [
            shot("Seguro lo has visto en libros y en videos.", stage(
                props=[prop("book", 300, 640, size=130, enter="pop"), prop("phone", 540, 640, size=130, enter="pop", delay=0.3), prop("lightbulb", 780, 640, size=120, enter="pop", delay=0.6)])),
            shot("Pero cuando otros científicos intentaron repetirlo, no siempre funcionó.", stage(
                props=[prop("chart", 540, 640, size=200, state="down", enter="draw", mark="cross", markAt=0.6)],
                texts=[text("No siempre se repetía", family="sans", size=52, emphasis=["No siempre"])])),
        ]),
        scene("E", "reveal", [
            shot("En 2025, un metaanálisis revisó casi cien años de estudios.", stage(
                counters=[{"from": 1927, "to": 2025, "x": 540, "y": 600, "size": 130, "seconds": 1.4}],
                texts=[text("casi un siglo de estudios", y=740, family="sans", size=40), text("Metaanálisis · 2025", family="sans", size=48)])),
            shot("Y no encontró que recordemos mejor lo inacabado.", stage(
                props=[prop("checklist", 540, 640, size=190, enter="none", mark="cross", markAt=0.35)],
                texts=[text("Mito", emphasis=["Mito"])])),
            shot("Encontró otra cosa: una tendencia clara a volver a lo que quedó a medias.", stage(
                figure=fig("walk", 260, toX=560, path="rise"), props=[prop("checklist", 790, 600, size=150, enter="pop", accent="reward")],
                texts=[text("Volvemos a lo pendiente", family="sans", size=50, emphasis=["Volvemos"])])),
            shot("Se llama efecto Ovsiankina, por una colega de Zeigarnik.", {"type": "kineticTitle", "kicker": "Se llama", "lines": ["Efecto", "Ovsiankina"], "emphasis": ["Ovsiankina"]}, "impact"),
        ]),
        scene("F", "demonstration", [
            shot("O sea, lo pendiente no se queda en tu memoria. Te empuja a regresar.", stage(
                figure=fig("walk", 300, toX=520, path="flat", pathTo=900), props=[prop("checklist", 760, 600, size=150, enter="none")],
                camera=cam(1.0, 1.06, 600, 780))),
        ]),
        scene("G", "action", [
            shot("Úsalo a tu favor: cuando termines de trabajar hoy, no cierres al final de algo.", stage(
                figure=fig("phone", 420, holding="phone"), props=[prop("book", 720, 620, size=140, state="open", enter="pop")],
                texts=[text("No cierres al final", family="sans", size=52)])),
            shot("Déjalo a mitad de una idea que sepas continuar.", stage(
                figure=fig("walk", 300, toX=470, path="fade"), props=[prop("checklist", 720, 600, size=150, state="normal", enter="pop")],
                texts=[text("Déjalo a mitad", emphasis=["a mitad"])])),
        ]),
        scene("H", "closer", [
            shot("Tu mente no guarda una lista de lo que dejaste a medias.",
                 {"type": "closer", "line": "Tu mente no guarda lo pendiente.", "emphasis": ["pendiente"], "source": "Ghibellini y Meier, 2025"}, "shimmer"),
            shot("Pero sí tiene ganas de volver.", stage(
                figure=fig("walk", 320, toX=560, path="rise"), props=[prop("checklist", 780, 580, size=140, state="open", enter="pop", delay=0.6)],
                texts=[text("Ganas de volver", emphasis=["volver"])])),
        ]),
        scene("I", "cta", [
            shot("¿Qué dejaste a medias que no te deja tranquilo?", stage(
                figure=fig("lookUp", 540, path="fade"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.3)])),
            shot("Cuéntamelo en los comentarios.", stage(texts=[text("Cuéntamelo", family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "¿Recordamos mejor lo que dejamos a medias? 🧠 Casi cien años de estudios dicen otra cosa… y la respuesta real es más útil.",
    ["#psicologia", "#productividad", "#procrastinacion", "#mitos", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 014 anchoring
v014 = sb(
    "014-efecto-anclaje",
    "El efecto anclaje: el primer número que ves cambia tu decisión",
    4,
    [
        {"citation": "Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. Science, 185(4157), 1124–1131.",
         "doi": "10.1126/science.185.4157.1124", "supports": "Experimento de la ruleta (10 o 65) y estimación del porcentaje de países africanos en la ONU: el número al azar arrastra la respuesta."},
        {"citation": "Klein, R. A., et al. (2014). Investigating variation in replicability: A \"Many Labs\" replication project. Social Psychology, 45(3), 142–152.",
         "doi": "10.1027/1864-9335/a000178", "supports": "El efecto anclaje se replicó con fuerza en laboratorios de varios países."},
        {"citation": "Englich, B., Mussweiler, T., & Strack, F. (2006). Playing dice with criminal sentences: The influence of irrelevant anchors on experts' judicial decision making. Personality and Social Psychology Bulletin, 32(2), 188–200.",
         "doi": "10.1177/0146167205282152", "supports": "Jueces con experiencia: la condena propuesta en un caso ficticio se vio influida por el número de unos dados (cargados) que ellos mismos lanzaron."},
    ],
    [
        scene("A", "hook", [
            shot("El primer precio que ves puede cambiar cuánto estás dispuesto a pagar.", stage(
                spotlight={"x": 600, "snap": True}, figure=fig("think", 300, path="flat"),
                props=[prop("tag", 620, 560, size=220, label="$200", enter="none"), prop("tag", 700, 800, size=130, label="$80", enter="pop", delay=1.4)],
                texts=[text("El primer precio manda", emphasis=["primer"])], camera=cam(1.0, 1.08)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿De verdad un número cualquiera puede mover tus decisiones?", stage(
                figure=fig("lookUp", 400, path="flat"), props=[prop("question", 680, 520, size=110, enter="pop", delay=0.3)],
                texts=[text("¿Un número cualquiera?", family="sans", size=56)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1974, Tversky y Kahneman giraron una ruleta arreglada.", stage(
                props=[prop("wheel", 540, 620, size=230, state="spin", enter="pop")],
                texts=[text("Tversky y Kahneman · 1974", family="sans", size=44)])),
            shot("Solo podía caer en 10 o en 65.", stage(
                props=[prop("wheel", 540, 600, size=180, enter="none")],
                counters=[{"from": 0, "to": 10, "x": 330, "y": 860, "size": 110, "seconds": 0.5}, {"from": 0, "to": 65, "x": 750, "y": 860, "size": 110, "seconds": 0.7, "delay": 0.4}])),
            shot("Después preguntaban qué porcentaje de países africanos estaba en la ONU.", stage(
                figure=fig("think", 540), props=[prop("question", 700, 480, size=90, enter="pop", delay=0.4)],
                texts=[text("¿Qué % de países africanos está en la ONU?", family="sans", size=44)])),
            shot("Quienes vieron el 65 respondían números mucho más altos.", stage(
                props=[prop("chart", 540, 640, size=200, state="up", enter="draw")],
                texts=[text("Vieron 65 → respondieron más", family="sans", size=48, emphasis=["más"])])),
            shot("A eso se le llama efecto anclaje.", {"type": "kineticTitle", "kicker": "Se llama", "lines": ["Efecto", "anclaje"], "emphasis": ["anclaje"]}, "impact"),
        ]),
        scene("D", "demonstration", [
            shot("Y no fue casualidad: un gran proyecto con laboratorios de varios países lo volvió a encontrar.", stage(
                extras=crowd([220, 380, 540, 700, 860], pose="think", opacity=0.55, scale=0.7),
                props=[prop("chart", 540, 480, size=130, state="up", enter="pop", mark="check", markAt=0.6)],
                texts=[text("Se repitió en varios países", family="sans", size=48)])),
        ]),
        scene("E", "retention", [
            shot("Pero eso le pasa a cualquiera… ¿o los expertos se salvan?", stage(
                figure=fig("stand", 540, path="flat"), props=[prop("balance", 760, 560, size=140, enter="pop"), prop("question", 540, 440, size=90, enter="pop", delay=0.6)],
                texts=[text("¿Y los expertos?", emphasis=["expertos"])])),
        ]),
        scene("F", "reveal", [
            shot("En un estudio, jueces con experiencia leyeron un caso ficticio y antes lanzaron unos dados.", stage(
                figure=fig("reach", 360), props=[prop("dice", 640, 720, size=120, state="spin", enter="pop", label="9"), prop("balance", 820, 520, size=130, enter="pop", delay=0.4)],
                texts=[text("Jueces con experiencia", family="sans", size=48)])),
            shot("Los dados estaban cargados.", stage(
                props=[prop("dice", 440, 640, size=150, enter="pop", label="3"), prop("dice", 640, 640, size=150, enter="pop", delay=0.3, label="9")],
                texts=[text("Cargados", emphasis=["Cargados"])], camera=cam(1.0, 1.1))),
            shot("Y aun así, la condena que proponían se movía según el número que salía.", stage(
                props=[prop("dice", 360, 560, size=110, enter="none", label="9"), prop("balance", 640, 700, size=240, enter="none", to={"state": "up", "at": 0.3})],
                texts=[text("El dado movió la condena", family="sans", size=50, emphasis=["dado"])])),
        ]),
        scene("G", "action", [
            shot("Así que, antes de negociar un precio o un sueldo, escribe tu número primero.", stage(
                figure=fig("think", 360, path="flat"), props=[prop("tag", 720, 600, size=170, label="TU $", enter="draw")],
                texts=[text("Tu número, primero", family="sans", size=54, emphasis=["primero"])])),
            shot("Y si puedes, sé tú quien dice la primera cifra.", stage(
                figure=fig("point", 360), extras=[fig("stand", 720, facing=-1, opacity=0.8)],
                props=[prop("tag", 540, 500, size=140, label="$", enter="pop", delay=0.3, accent="reward")])),
        ]),
        scene("H", "closer", [
            shot("Tu mente nunca empieza desde cero. Empieza desde el primer número que alguien le pone enfrente.",
                 {"type": "closer", "line": "Tu mente nunca empieza desde cero.", "emphasis": ["cero"], "source": "Tversky y Kahneman, 1974 · Englich et al., 2006"}, "shimmer"),
        ]),
        scene("I", "cta", [
            shot("¿Te ha pasado con un precio de «antes» tachado?", stage(
                props=[prop("tag", 540, 600, size=180, label="$̶9̶9̶", enter="pop"), prop("bubble", 760, 460, size=110, enter="pop", delay=0.5)])),
            shot("Cuéntame en los comentarios.", stage(texts=[text("Cuéntame", family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "El primer precio que ves cambia lo que estás dispuesto a pagar 💸 Hasta a jueces expertos les pasa. Mira cómo protegerte la próxima vez que negocies.",
    ["#psicologia", "#dinero", "#negociacion", "#sesgos", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 005 need for approval
v005 = sb(
    "005-necesidad-aprobacion",
    "La necesidad de aprobación: tu autoestima es un medidor, no una nota",
    3,
    [
        {"citation": "Baumeister, R. F., & Leary, M. R. (1995). The need to belong: Desire for interpersonal attachments as a fundamental human motivation. Psychological Bulletin, 117(3), 497–529.",
         "doi": "10.1037/0033-2909.117.3.497", "supports": "Pertenecer es una necesidad humana fundamental."},
        {"citation": "Leary, M. R., Tambor, E. S., Terdal, S. K., & Downs, D. L. (1995). Self-esteem as an interpersonal monitor: The sociometer hypothesis. Journal of Personality and Social Psychology, 68(3), 518–530.",
         "doi": "10.1037/0022-3514.68.3.518", "supports": "Teoría del sociómetro: la autoestima funciona como un indicador de aceptación social; la exclusión la reduce."},
        {"citation": "Boothby, E. J., Cooney, G., Sandstrom, G. M., & Clark, M. S. (2018). The liking gap in conversations: Do people like us more than we think? Psychological Science, 29(11), 1742–1756.",
         "doi": "10.1177/0956797618783714", "supports": "Tras conversar, la gente subestima cuánto agradó (el medidor exagera)."},
    ],
    [
        scene("A", "hook", [
            shot("Necesitar la aprobación de los demás no es debilidad.", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("stand", 540, path="flat"),
                props=[prop("gauge", 540, 600, size=200, state="spin", enter="none")],
                texts=[text("No es debilidad", emphasis=["debilidad"])], camera=cam(1.0, 1.06)), "impact"),
            shot("Es un sistema de alarma.", stage(
                figure=fig("lookUp", 540, path="flat"), props=[prop("gauge", 540, 600, size=220, state="normal", enter="none", to={"state": "down", "at": 0.2})],
                texts=[text("Es una alarma", emphasis=["alarma"])])),
        ]),
        scene("B", "question", [
            shot("Entonces, ¿por qué un comentario pequeño puede arruinarte el día entero?", stage(
                figure=fig("slump", 460, path="fall"), props=[prop("bubble", 720, 520, size=120, enter="pop", delay=0.3)],
                texts=[text("Un comentario pequeño…", family="sans", size=54)])),
        ]),
        scene("C", "mechanism", [
            shot("Los psicólogos Roy Baumeister y Mark Leary propusieron que pertenecer es una necesidad humana básica.", stage(
                figure=fig("stand", 540), extras=crowd([300, 420, 660, 780], opacity=0.6, scale=0.8, facing=[1, 1, -1, -1]),
                texts=[text("Pertenecer es una necesidad", family="sans", size=50, emphasis=["necesidad"])])),
            shot("Durante casi toda nuestra historia, quedarse solo era peligroso.", stage(
                figure=fig("walk", 520, toX=820, path="fade"), extras=crowd([180, 300, 420], opacity=0.5, scale=0.75),
                texts=[text("Solo = peligro", emphasis=["peligro"])])),
        ]),
        scene("D", "demonstration", [
            shot("En sus experimentos, Leary vio algo muy claro:", stage(
                figure=fig("think", 540), extras=crowd([260, 820], opacity=0.5, scale=0.8, facing=[1, -1]),
                props=[prop("lightbulb", 540, 460, size=110, state="glow", enter="pop", delay=0.3)])),
            shot("cuando alguien se sentía excluido, su autoestima bajaba.", stage(
                figure=fig("slump", 760), extras=crowd([200, 320, 440], opacity=0.5, scale=0.75, facing=[1, 1, 1]),
                props=[prop("gauge", 760, 520, size=140, state="normal", enter="pop", to={"state": "down", "at": 0.55})])),
        ]),
        scene("E", "retention", [
            shot("Eso cambia la pregunta: ¿qué está midiendo de verdad tu autoestima?", stage(
                props=[prop("gauge", 540, 640, size=240, state="spin", enter="pop"), prop("question", 540, 420, size=90, enter="pop", delay=0.6)],
                camera=cam(1.0, 1.12))),
        ]),
        scene("F", "reveal", [
            shot("Según la teoría del sociómetro, tu autoestima no mide cuánto vales.", stage(
                props=[prop("gauge", 540, 640, size=220, enter="pop")],
                texts=[text("No mide cuánto vales", family="sans", size=52, emphasis=["No"])])),
            shot("Mide cuánto sientes que te aceptan.", stage(
                figure=fig("stand", 540), extras=crowd([300, 780], opacity=0.7, scale=0.85, facing=[1, -1]),
                props=[prop("gauge", 540, 460, size=150, state="normal", enter="none", to={"state": "up", "at": 0.3})],
                texts=[text("Mide aceptación", emphasis=["aceptación"])])),
            shot("Y ese medidor suele exagerar.", stage(
                props=[prop("gauge", 540, 640, size=220, state="spin", enter="none")],
                texts=[text("El medidor exagera", emphasis=["exagera"])])),
            shot("Después de conversar, la gente cree que cayó peor de lo que realmente cayó.", stage(
                figure=fig("stand", 400), extras=[fig("stand", 680, facing=-1, opacity=0.9)],
                props=[prop("gauge", 400, 500, size=110, state="down", enter="pop"), prop("gauge", 680, 500, size=110, state="up", enter="pop", delay=0.5)],
                texts=[text("Creíste", x=400, y=380, family="sans", size=38), text("Sintió", x=680, y=380, family="sans", size=38)])),
        ]),
        scene("G", "action", [
            shot("Así que, cuando sientas que necesitas aprobación, pregúntate: ¿la opinión de quién me importa de verdad?", stage(
                figure=fig("think", 400), props=[prop("checklist", 720, 600, size=170, state="closed", enter="draw")],
                texts=[text("¿Quién me importa de verdad?", family="sans", size=48)])),
            shot("Haz una lista corta. Lo demás es ruido.", stage(
                props=[prop("checklist", 540, 640, size=200, state="open", enter="none")],
                extras=crowd([180, 900], opacity=0.25, scale=0.7),
                texts=[text("Lo demás es ruido", emphasis=["ruido"])])),
        ]),
        scene("H", "closer", [
            shot("No se trata de dejar de necesitar a los demás.", stage(
                figure=fig("stand", 540, path="flat"), extras=crowd([360, 720], opacity=0.7, scale=0.9, facing=[1, -1]))),
            shot("Se trata de elegir a quién le das el control del medidor.", stage(
                figure=fig("reach", 460), extras=[fig("stand", 700, facing=-1, opacity=0.9)],
                props=[prop("gauge", 580, 480, size=150, state="normal", enter="pop", accent="reward")],
                texts=[text("Tú eliges quién", emphasis=["Tú"])])),
        ]),
        scene("I", "cta", [
            shot("¿La opinión de quién te importa más de lo que quisieras?", stage(
                figure=fig("lookUp", 540, path="fade"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.3)])),
            shot("Te leo en los comentarios.", stage(texts=[text("Te leo", family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "Necesitar aprobación no es debilidad: es una alarma 🧠 La ciencia dice que tu autoestima no mide cuánto vales… mide otra cosa.",
    ["#psicologia", "#autoestima", "#relaciones", "#crecimientopersonal", "#aprendeentiktok"],
)

write(v016, v014, v005)
