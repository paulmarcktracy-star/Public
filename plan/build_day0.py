"""Videos 1, 2, 3 (first day of the owner's order). Hooks verbatim. Natural spoken Spanish."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbkit import cam, crowd, fig, prop, sb, scene, shot, stage, text, write  # noqa: E402

# ------------------------------------------------------------------ 001 overthinking
v1 = sb(
    "001-pensar-demasiado",
    "Pensar demasiado: por qué darle vueltas puede impedirte actuar",
    1,
    [
        {"citation": "Wilson, T. D., & Schooler, J. W. (1991). Thinking too much: Introspection can reduce the quality of preferences and decisions. Journal of Personality and Social Psychology, 60(2), 181–192.",
         "doi": "10.1037/0022-3514.60.2.181", "supports": "Quienes analizaron por escrito sus razones sobre mermeladas terminaron con preferencias más alejadas de las de los expertos."},
        {"citation": "Watkins, E. R. (2008). Constructive and unconstructive repetitive thought. Psychological Bulletin, 134(2), 163–206.",
         "doi": "10.1037/0033-2909.134.2.163", "supports": "El pensamiento repetitivo abstracto (el porqué) es poco constructivo; el concreto (el cómo) ayuda a resolver."},
        {"citation": "Lyubomirsky, S., & Nolen-Hoeksema, S. (1995). Effects of self-focused rumination on negative thinking and interpersonal problem solving. Journal of Personality and Social Psychology, 69(1), 176–190.",
         "doi": "10.1037/0022-3514.69.1.176", "supports": "La rumiación empeora la resolución de problemas."},
    ],
    [
        scene("A", "hook", [
            shot("Cuanto más piensas en una decisión, más difícil puede volverse elegir.", stage(
                spotlight={"x": 420, "snap": True}, figure=fig("think", 420, path="fork"),
                props=[prop("bubble", 560, 430, size=110, enter="none"), prop("question", 700, 360, size=70, enter="pop", delay=0.8), prop("question", 610, 300, size=55, enter="pop", delay=1.3)],
                texts=[text("Pensar más, elegir peor", emphasis=["peor"])], camera=cam(1.0, 1.08)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Cómo puede ser que darle más vueltas te aleje de la respuesta?", stage(
                figure=fig("think", 540, path="fork"), props=[prop("clock", 760, 520, size=110, state="spin", enter="pop")],
                texts=[text("¿Más vueltas, menos respuesta?", family="sans", size=52)])),
        ]),
        scene("C", "mechanism", [
            shot("En un experimento clásico, unas personas probaron mermeladas y dijeron cuál preferían.", stage(
                figure=fig("reach", 300), props=[prop("jar", 560, 640, size=120, enter="pop"), prop("jar", 700, 640, size=120, enter="pop", delay=0.2), prop("jar", 840, 640, size=120, enter="pop", delay=0.4)])),
            shot("A otras se les pidió, además, escribir por qué.", stage(
                figure=fig("think", 320), props=[prop("book", 620, 640, size=170, state="open", enter="draw")],
                texts=[text("¿Por qué?", emphasis=["¿Por qué?"])])),
            shot("Y las que analizaron sus razones terminaron eligiendo peor, según los expertos.", stage(
                props=[prop("balance", 540, 720, size=240, enter="none", to={"state": "up", "at": 0.3})],
                texts=[text("Analizar", x=400, y=540, family="sans", size=38), text("Expertos", x=680, y=540, family="sans", size=38),
                       text("Eligieron peor", family="sans", size=54, emphasis=["peor"])])),
        ]),
        scene("D", "demonstration", [
            shot("Al buscar razones fáciles de explicar,", stage(
                figure=fig("think", 360), props=[prop("book", 680, 620, size=140, state="open", enter="pop")])),
            shot("le das peso a detalles que no son los importantes.", stage(
                props=[prop("jar", 540, 660, size=170, enter="pop"), prop("lightbulb", 780, 480, size=90, state="dim", enter="pop", delay=0.6)],
                texts=[text("Detalles que no importan", family="sans", size=48)])),
        ]),
        scene("E", "retention", [
            shot("Y cuando el pensamiento se vuelve un círculo, ¿y si sale mal?, ¿y si me equivoco?,", stage(
                figure=fig("slump", 540, path="flat"),
                props=[prop("question", 400, 470, size=70, enter="pop"), prop("question", 540, 410, size=70, enter="pop", delay=0.4), prop("question", 680, 470, size=70, enter="pop", delay=0.8)])),
            shot("ya no estás resolviendo nada. Estás rumiando.", stage(
                figure=fig("slump", 540), props=[prop("clock", 540, 470, size=120, state="spin", enter="none")],
                texts=[text("Rumiar", emphasis=["Rumiar"])])),
        ]),
        scene("F", "reveal", [
            shot("Pero la ciencia encontró algo que lo cambia todo:", stage(
                props=[prop("lightbulb", 540, 600, size=200, state="glow", enter="draw")], camera=cam(1.0, 1.1))),
            shot("el problema no es pensar. Es pensar en abstracto, en el porqué.", stage(
                figure=fig("think", 380, path="none"), props=[prop("question", 640, 480, size=110, enter="pop", mark="cross", markAt=0.6)],
                texts=[text("El porqué te atrapa", family="sans", size=52, emphasis=["porqué"])])),
            shot("Pensar en concreto, en el cómo, sí te ayuda a resolver.", stage(
                figure=fig("walk", 300, toX=560, path="rise"), props=[prop("checklist", 790, 580, size=140, state="open", enter="pop", delay=0.4, accent="reward")],
                texts=[text("El cómo te mueve", emphasis=["cómo"])])),
        ]),
        scene("G", "action", [
            shot("Así que, cuando notes el bucle, cambia la pregunta.", stage(
                figure=fig("think", 540, path="flat"), props=[prop("question", 540, 420, size=90, enter="pop")])),
            shot("En vez de «¿por qué me pasa esto?»,", stage(
                figure=fig("slump", 540, path="flat"), props=[prop("question", 540, 430, size=90, enter="pop", mark="cross", markAt=0.6)])),
            shot("pregúntate: «¿cuál es el siguiente paso que puedo dar hoy?»", stage(
                figure=fig("walk", 280, toX=520, path="rise"),
                texts=[text("¿Cuál es el siguiente paso?", family="sans", size=52, emphasis=["siguiente paso"])])),
        ]),
        scene("H", "closer", [
            shot("Pensar es una herramienta. Pero el mapa no camina por ti.",
                 {"type": "closer", "line": "El mapa no camina por ti.", "emphasis": ["camina"], "source": "Wilson y Schooler, 1991 · Watkins, 2008"}, "shimmer"),
        ]),
        scene("I", "cta", [
            shot("¿Sobre qué decisión llevas demasiado tiempo pensando?", stage(
                figure=fig("lookUp", 540, path="fork"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.3)])),
            shot("Cuéntamelo en los comentarios.", stage(texts=[text("Cuéntamelo", family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "Pensar más no siempre te hace decidir mejor 🧠 La ciencia descubrió qué tipo de pensamiento te atrapa… y cuál te saca del bucle.",
    ["#psicologia", "#sobrepensar", "#decisiones", "#mente", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 002 confirmation bias
v2 = sb(
    "002-sesgo-confirmacion",
    "El sesgo de confirmación: tu cerebro busca tener razón",
    1,
    [
        {"citation": "Wason, P. C. (1960). On the failure to eliminate hypotheses in a conceptual task. Quarterly Journal of Experimental Psychology, 12(3), 129–140.",
         "doi": "10.1080/17470216008416717", "supports": "Tarea 2-4-6: la mayoría prueba secuencias que confirman su hipótesis y casi nadie intenta refutarla."},
        {"citation": "Hart, W., Albarracín, D., Eagly, A. H., Brechan, I., Lindberg, M. J., & Merrill, L. (2009). Feeling validated versus being correct: A meta-analysis of selective exposure to information. Psychological Bulletin, 135(4), 555–588.",
         "doi": "10.1037/a0015701", "supports": "Metaanálisis: preferimos información que confirma lo que ya pensamos."},
        {"citation": "Stanovich, K. E., West, R. F., & Toplak, M. E. (2013). Myside bias, rational thinking, and intelligence. Current Directions in Psychological Science, 22(4), 259–264.",
         "doi": "10.1177/0963721413480174", "supports": "El sesgo de 'mi lado' es poco dependiente de la inteligencia."},
    ],
    [
        scene("A", "hook", [
            shot("Crees que buscas la verdad.", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("walk", 300, toX=520, path="fork"),
                texts=[text("Buscas la verdad…", family="sans", size=56)], camera=cam(1.0, 1.06)), "impact"),
            shot("Tu cerebro busca tener razón.", stage(
                figure=fig("stand", 540, path="fork"), props=[prop("brain", 540, 470, size=140, state="glow", enter="pop", mark="check", markAt=0.5)],
                texts=[text("Tu cerebro busca tener razón", emphasis=["razón"])])),
        ]),
        scene("B", "question", [
            shot("¿Y si la persona más fácil de engañar fueras tú?", stage(
                figure=fig("lookUp", 540, path="flat"), props=[prop("question", 540, 420, size=100, enter="pop", delay=0.3)],
                texts=[text("¿Y si fueras tú?", emphasis=["tú"])])),
        ]),
        scene("C", "mechanism", [
            shot("En 1960, Peter Wason le mostró a la gente tres números: 2, 4 y 6.", stage(
                counters=[{"from": 0, "to": 2, "x": 360, "y": 620, "size": 140, "seconds": 0.4}, {"from": 0, "to": 4, "x": 540, "y": 620, "size": 140, "seconds": 0.4, "delay": 0.5},
                          {"from": 0, "to": 6, "x": 720, "y": 620, "size": 140, "seconds": 0.4, "delay": 1.0}],
                texts=[text("Peter Wason · 1960", family="sans", size=46)])),
            shot("Tenían que adivinar la regla, probando otras secuencias.", stage(
                figure=fig("think", 540), props=[prop("question", 700, 460, size=90, enter="pop", delay=0.3)],
                texts=[text("¿Cuál es la regla?", family="sans", size=54)])),
            shot("Casi todos probaron números que confirmaban su idea, como 8, 10 y 12.", stage(
                counters=[{"from": 0, "to": 8, "x": 360, "y": 620, "size": 120, "seconds": 0.4}, {"from": 0, "to": 10, "x": 540, "y": 620, "size": 120, "seconds": 0.4, "delay": 0.4},
                          {"from": 0, "to": 12, "x": 720, "y": 620, "size": 120, "seconds": 0.4, "delay": 0.8}],
                texts=[text("Confirmar, confirmar, confirmar", family="sans", size=46)])),
            shot("Casi nadie intentó demostrar que estaba equivocado.", stage(
                figure=fig("stand", 540, path="fork"), props=[prop("question", 760, 520, size=80, enter="pop", mark="cross", markAt=0.5)],
                texts=[text("Nadie buscó el error", family="sans", size=52, emphasis=["error"])])),
        ]),
        scene("D", "retention", [
            shot("¿La regla? Simplemente, números que van subiendo.", stage(
                props=[prop("chart", 540, 640, size=200, state="up", enter="draw")],
                texts=[text("Solo: números que suben", emphasis=["suben"])], camera=cam(1.0, 1.08))),
        ]),
        scene("E", "demonstration", [
            shot("En la vida pasa igual.", stage(
                figure=fig("phone", 540, holding="phone"), props=[prop("phone", 760, 600, size=130, state="typing", enter="pop")])),
            shot("Una revisión de muchos estudios encontró que preferimos la información que nos da la razón.", stage(
                props=[prop("book", 360, 640, size=130, enter="pop", mark="check", markAt=0.5), prop("book", 720, 640, size=130, enter="pop", delay=0.3, state="dim")],
                texts=[text("Elegimos lo que nos da la razón", family="sans", size=46)])),
        ]),
        scene("F", "retention", [
            shot("Entonces, ¿la solución es ser más inteligente?", stage(
                props=[prop("brain", 540, 600, size=200, state="glow", enter="pop"), prop("question", 540, 400, size=80, enter="pop", delay=0.5)])),
        ]),
        scene("G", "reveal", [
            shot("No. Las investigaciones muestran que ser más inteligente no te protege de este sesgo.", stage(
                figure=fig("walk", 300, toX=540, path="fork"), props=[prop("brain", 760, 480, size=120, state="glow", enter="pop", mark="cross", markAt=0.6)],
                texts=[text("La inteligencia no te protege", family="sans", size=48, emphasis=["no"])])),
        ]),
        scene("H", "action", [
            shot("Hazte una sola pregunta: ¿qué tendría que ver para cambiar de opinión?", stage(
                figure=fig("think", 400, path="fork"), props=[prop("question", 620, 460, size=90, enter="pop")],
                texts=[text("¿Qué me haría cambiar de opinión?", family="sans", size=46)])),
            shot("Y después, búscalo a propósito.", stage(
                figure=fig("walk", 300, toX=560, path="fork"), props=[prop("lightbulb", 800, 500, size=110, state="glow", enter="pop", delay=0.4, accent="reward")],
                texts=[text("Búscalo a propósito", emphasis=["a propósito"])])),
        ]),
        scene("I", "closer", [
            shot("Tener razón se siente bien. Descubrir que no la tienes te hace más sabio.",
                 {"type": "closer", "line": "Tener razón se siente bien. Corregirte te hace sabio.", "emphasis": ["sabio"], "source": "Wason, 1960 · Hart et al., 2009"}, "shimmer"),
        ]),
        scene("J", "cta", [
            shot("¿Qué opinión cambiaste en los últimos años?", stage(
                figure=fig("lookUp", 540, path="rise"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.3)])),
            shot("Te leo en los comentarios.", stage(texts=[text("Te leo", family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "Crees que buscas la verdad, pero tu cerebro busca tener razón 🧠 Prueba el reto 2-4-6 antes de ver la respuesta.",
    ["#psicologia", "#sesgos", "#pensamientocritico", "#mente", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 003 paradox of choice
v3 = sb(
    "003-paradoja-eleccion",
    "La paradoja de la elección: ¿demasiadas opciones te paralizan?",
    4,
    [
        {"citation": "Iyengar, S. S., & Lepper, M. R. (2000). When choice is demotivating: Can one desire too much of a good thing? Journal of Personality and Social Psychology, 79(6), 995–1006.",
         "doi": "10.1037/0022-3514.79.6.995", "supports": "Mesa de 24 mermeladas frente a 6: la grande atrae más, pero en la pequeña compra mucha más gente (≈30 % frente a ≈3 %)."},
        {"citation": "Scheibehenne, B., Greifeneder, R., & Todd, P. M. (2010). Can there ever be too many options? A meta-analytic review of choice overload. Journal of Consumer Research, 37(3), 409–425.",
         "doi": "10.1086/651235", "supports": "Metaanálisis de 50 experimentos: efecto medio de sobrecarga prácticamente nulo."},
        {"citation": "Chernev, A., Böckenholt, U., & Goodman, J. (2015). Choice overload: A conceptual review and meta-analysis. Journal of Consumer Psychology, 25(2), 333–358.",
         "doi": "10.1016/j.jcps.2014.08.002", "supports": "La sobrecarga aparece bajo condiciones: opciones difíciles de comparar, preferencias poco claras, tarea compleja."},
    ],
    [
        scene("A", "hook", [
            shot("Tener 100 opciones puede hacer que elegir sea más difícil que tener solo 5.", stage(
                spotlight={"x": 400, "snap": True}, figure=fig("think", 400, path="fork"),
                counters=[{"from": 100, "to": 5, "x": 720, "y": 560, "size": 130, "seconds": 1.6, "delay": 1.0, "suffix": " opciones"}],
                texts=[text("100 opciones", emphasis=["100"])], camera=cam(1.0, 1.08)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Por qué a veces elegir entre muchas cosas te bloquea… y otras veces no?", stage(
                figure=fig("stand", 540, path="fork"), props=[prop("question", 540, 440, size=90, enter="pop", delay=0.3)],
                texts=[text("¿Siempre te bloquea?", family="sans", size=54)])),
        ]),
        scene("C", "mechanism", [
            shot("En el año 2000, en un supermercado, una mesa ofrecía 24 mermeladas y otra, solo 6.", stage(
                props=[prop("jar", 300, 640, size=90, enter="pop"), prop("jar", 380, 640, size=90, enter="pop", delay=0.1), prop("jar", 460, 640, size=90, enter="pop", delay=0.2),
                       prop("jar", 740, 640, size=90, enter="pop", delay=0.5)],
                counters=[{"from": 0, "to": 24, "x": 380, "y": 800, "size": 90, "seconds": 0.8}, {"from": 0, "to": 6, "x": 740, "y": 800, "size": 90, "seconds": 0.5, "delay": 0.5}])),
            shot("La mesa grande atraía a más gente.", stage(
                extras=crowd([200, 300, 400, 500], opacity=0.6, scale=0.72), props=[prop("jar", 350, 520, size=90, enter="pop")],
                texts=[text("24: más curiosos", family="sans", size=50)])),
            shot("Pero en la pequeña compraban muchas más personas: cerca del 30 % frente al 3 %.", stage(
                props=[prop("cart", 720, 520, size=130, enter="pop")],
                counters=[{"from": 0, "to": 30, "suffix": "%", "x": 720, "y": 720, "size": 120, "seconds": 1.0}, {"from": 0, "to": 3, "suffix": "%", "x": 360, "y": 720, "size": 120, "seconds": 0.6}],
                texts=[text("24", x=360, y=840, family="sans", size=36), text("6", x=720, y=840, family="sans", size=36)])),
            shot("Así nació la famosa paradoja de la elección.", {"type": "kineticTitle", "kicker": "Así nació", "lines": ["La paradoja", "de la elección"], "emphasis": ["elección"]}, "impact"),
        ]),
        scene("D", "retention", [
            shot("Pero cuando otros científicos repitieron estos experimentos…", stage(
                extras=crowd([220, 380, 540, 700, 860], pose="think", opacity=0.55, scale=0.7),
                props=[prop("question", 540, 440, size=90, enter="pop", delay=0.5)])),
        ]),
        scene("E", "reveal", [
            shot("un metaanálisis de 50 experimentos encontró que, en promedio, el efecto era casi cero.", stage(
                props=[prop("balance", 540, 760, size=240, state="down", enter="none", to={"state": "normal", "at": 0.35})],
                counters=[{"from": 50, "to": 0, "x": 540, "y": 520, "size": 130, "seconds": 1.4, "delay": 0.8}],
                texts=[text("Efecto promedio ≈ 0", family="sans", size=52)])),
            shot("Elegir entre muchas opciones sí te puede bloquear, pero en casos concretos:", stage(
                figure=fig("think", 540, path="fork"), props=[prop("lightbulb", 760, 480, size=100, state="glow", enter="pop", delay=0.4)])),
            shot("cuando las opciones son difíciles de comparar y cuando no sabes bien qué quieres.", stage(
                props=[prop("jar", 380, 640, size=130, enter="pop", mark="question", markAt=0.4), prop("jar", 700, 640, size=130, enter="pop", delay=0.3, mark="question", markAt=0.6)],
                texts=[text("Difícil de comparar · no sé qué quiero", family="sans", size=40)])),
        ]),
        scene("F", "action", [
            shot("Así que no necesitas menos opciones. Necesitas un criterio.", stage(
                figure=fig("stand", 540, path="fork"), texts=[text("Necesitas un criterio", emphasis=["criterio"])])),
            shot("Antes de elegir, escribe las dos cosas que más te importan", stage(
                figure=fig("think", 360, path="flat"), props=[prop("checklist", 700, 600, size=150, state="closed", enter="draw")])),
            shot("y descarta todo lo que no las cumpla.", stage(
                figure=fig("walk", 300, toX=540, path="flat"), props=[prop("checklist", 780, 580, size=150, state="open", enter="draw", accent="reward")],
                texts=[text("Dos criterios. Lo demás, fuera.", family="sans", size=48)])),
        ]),
        scene("G", "closer", [
            shot("El problema casi nunca es el menú. Es no saber de qué tienes hambre.",
                 {"type": "closer", "line": "El problema no es el menú. Es no saber de qué tienes hambre.", "emphasis": ["hambre"], "source": "Scheibehenne et al., 2010 · Chernev et al., 2015"}, "shimmer"),
        ]),
        scene("H", "cta", [
            shot("¿Dónde te bloquean más las opciones: comida, ropa, series o tu carrera?", stage(
                figure=fig("lookUp", 540, path="fork"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.3)])),
            shot("Cuéntame.", stage(texts=[text("Cuéntame", family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "¿Demasiadas opciones te paralizan? 🛒 El famoso experimento de las mermeladas no cuenta toda la historia. Mira lo que encontró la ciencia después.",
    ["#psicologia", "#decisiones", "#consumo", "#mitos", "#aprendeentiktok"],
)

write(v1, v2, v3)
