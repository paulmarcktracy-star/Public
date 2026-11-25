"""Videos 6 and 7. Hooks verbatim. Natural spoken Spanish. Cinematic camera (default)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbkit import cam, crowd, fig, prop, sb, scene, shot, stage, text, write  # noqa: E402

v6 = sb(
    "006-efecto-camaleon",
    "El efecto camaleón: por qué imitamos sin darnos cuenta",
    3,
    [
        {"citation": "Chartrand, T. L., & Bargh, J. A. (1999). The chameleon effect: The perception–behavior link and social interaction. Journal of Personality and Social Psychology, 76(6), 893–910.",
         "doi": "10.1037/0022-3514.76.6.893", "supports": "Imitación inconsciente de gestos; ser imitado aumenta la fluidez y el agrado; las personas más empáticas imitan más."},
        {"citation": "Vicaria, I. M., & Dickens, L. (2016). Meta-analyses of the intra- and interpersonal outcomes of interpersonal coordination. Journal of Nonverbal Behavior, 40(4), 335–361.",
         "doi": "10.1007/s10919-016-0238-8", "supports": "Metaanálisis: la coordinación interpersonal se asocia con más agrado y conducta prosocial."},
        {"citation": "FORRT Replication Atlas — Chartrand & Bargh (1999): registro de réplicas.",
         "url": "https://forrt.org/flora-replication-atlas/doi/10.1037/0022-3514.76.6.893/", "supports": "Réplicas con efecto menor y no en todos los gestos (sonrisa sí; mover el pie, no de forma consistente)."},
    ],
    [
        scene("A", "hook", [
            shot("Sin darte cuenta, podrías estar copiando los gestos de la persona que tienes enfrente.", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("reach", 400, path="flat", pathTo=760), extras=[fig("reach", 680, facing=-1, opacity=0.9)],
                texts=[text("Copias sin darte cuenta", emphasis=["sin darte cuenta"])], camera=cam(1.0, 1.06)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Por qué copiamos gestos, posturas y hasta palabras de quien tenemos al frente?", stage(
                figure=fig("think", 400), extras=[fig("think", 680, facing=-1, opacity=0.9)],
                props=[prop("question", 540, 440, size=90, enter="pop", delay=0.4)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1999, los psicólogos Chartrand y Bargh lo pusieron a prueba.", stage(
                props=[prop("lightbulb", 540, 600, size=170, state="glow", enter="draw")], texts=[text("Chartrand y Bargh · 1999", family="sans", size=46)])),
            shot("Si la otra persona se tocaba la cara, los participantes también lo hacían más.", stage(
                figure=fig("think", 400), extras=[fig("think", 680, facing=-1, opacity=0.9)],
                texts=[text("Lo hacían más", family="sans", size=54, emphasis=["más"])])),
            shot("Sin darse cuenta.", stage(
                figure=fig("stand", 540, path="flat"), props=[prop("question", 540, 440, size=80, enter="pop")], camera=cam(1.0, 1.08))),
            shot("Lo llamaron efecto camaleón.", {"type": "kineticTitle", "kicker": "Lo llamaron", "lines": ["Efecto", "camaleón"], "emphasis": ["camaleón"]}, "impact"),
        ]),
        scene("D", "demonstration", [
            shot("Y cuando alguien los imitaba a ellos, sutilmente, la conversación les parecía más fluida.", stage(
                figure=fig("point", 400), extras=[fig("point", 680, facing=-1, opacity=0.9)],
                props=[prop("bubble", 470, 520, size=100, enter="pop"), prop("bubble", 610, 480, size=100, enter="pop", delay=0.6)])),
            shot("Esa persona les caía mejor.", stage(
                props=[prop("gauge", 540, 600, size=200, state="normal", enter="pop", to={"state": "up", "at": 0.3})],
                texts=[text("Les caía mejor", emphasis=["mejor"])])),
        ]),
        scene("E", "retention", [
            shot("Parece el truco perfecto para caer bien. Pero hay un detalle.", stage(
                figure=fig("stand", 540, path="fork"), props=[prop("lock", 540, 440, size=100, enter="pop", delay=0.5)],
                texts=[text("¿El truco perfecto?", family="sans", size=54)])),
        ]),
        scene("F", "reveal", [
            shot("Cuando otros científicos repitieron el estudio, el efecto fue más pequeño", stage(
                extras=crowd([220, 380, 540, 700, 860], pose="think", opacity=0.55, scale=0.7),
                props=[prop("chart", 540, 460, size=150, state="down", enter="draw")],
                texts=[text("Más pequeño", emphasis=["pequeño"])])),
            shot("y no apareció con todos los gestos.", stage(
                figure=fig("stand", 400), extras=[fig("stand", 680, facing=-1, opacity=0.9)],
                props=[prop("question", 540, 440, size=80, enter="pop", mark="cross", markAt=0.5)])),
            shot("La sonrisa sí se contagiaba. Mover el pie, no tanto.", stage(
                props=[prop("bubble", 380, 620, size=140, enter="pop", mark="check", markAt=0.3, accent="reward"), prop("question", 720, 620, size=120, enter="pop", delay=0.8, mark="cross", markAt=0.8)],
                texts=[text("Sonrisa", x=380, y=800, family="sans", size=40), text("Pie", x=720, y=800, family="sans", size=40)])),
        ]),
        scene("G", "action", [
            shot("Así que no copies a nadie a propósito. Se nota.", stage(
                figure=fig("point", 400), extras=[fig("stand", 700, facing=-1, opacity=0.8)],
                props=[prop("question", 700, 440, size=70, enter="pop", mark="cross", markAt=0.6)])),
            shot("Mejor escucha de verdad. La sintonía llega sola cuando prestas atención.", stage(
                figure=fig("stand", 420, path="flat", pathTo=720), extras=[fig("stand", 660, facing=-1, opacity=0.9)],
                props=[prop("bubble", 540, 480, size=110, enter="pop", delay=0.4)],
                texts=[text("Escucha de verdad", emphasis=["de verdad"])])),
        ]),
        scene("H", "closer", [
            shot("No imitamos para escondernos. Imitamos para conectar.",
                 {"type": "closer", "line": "No imitamos para escondernos. Imitamos para conectar.", "emphasis": ["conectar"], "source": "Chartrand y Bargh, 1999 · Vicaria y Dickens, 2016"}, "shimmer"),
        ]),
        scene("I", "cta", [
            shot("¿Te ha pasado que se te pegan las palabras o el acento de alguien?", stage(
                figure=fig("lookUp", 540, path="flat"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.3)])),
            shot("Cuéntame en los comentarios.", stage(texts=[text("Cuéntame", family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "Sin darte cuenta, podrías estar copiando a la persona que tienes enfrente 🦎 ¿Es el truco perfecto para caer bien? La ciencia tiene un matiz.",
    ["#psicologia", "#comunicacion", "#relaciones", "#lenguajecorporal", "#aprendeentiktok"],
)

v7 = sb(
    "007-gratificacion-instantanea",
    "La gratificación instantánea: lo que el test del dulce no te contó",
    2,
    [
        {"citation": "Watts, T. W., Duncan, G. J., & Quan, H. (2018). Revisiting the marshmallow test: A conceptual replication investigating links between early delay of gratification and later outcomes. Psychological Science, 29(7), 1159–1177.",
         "doi": "10.1177/0956797618761661", "supports": "Muestra mayor y diversa: al controlar el entorno familiar y habilidades tempranas, la relación con logros posteriores se reduce mucho."},
        {"citation": "Kidd, C., Palmeri, H., & Aslin, R. N. (2013). Rational snacking: Young children's decision-making on the marshmallow task is moderated by beliefs about environmental reliability. Cognition, 126(1), 109–114.",
         "doi": "10.1016/j.cognition.2012.08.004", "supports": "Los niños esperaron mucho más cuando el adulto había cumplido antes una promesa."},
    ],
    [
        scene("A", "hook", [
            shot("Un niño que espera por un dulce", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("stand", 420, scale=0.7, path="flat"),
                props=[prop("donut", 640, 900, size=90, enter="none"), prop("clock", 640, 640, size=100, state="spin", enter="none")],
                texts=[text("Esperar por un dulce", emphasis=["dulce"])], camera=cam(1.0, 1.06)), "impact"),
            shot("no necesariamente tendrá más éxito en la vida.", stage(
                figure=fig("walk", 420, toX=600, scale=0.7, path="fade"), props=[prop("mountain", 820, 560, size=140, enter="pop", mark="question", markAt=0.5)],
                texts=[text("¿Más éxito? No necesariamente", family="sans", size=48)])),
        ]),
        scene("B", "question", [
            shot("¿Esperar es cuestión de fuerza de voluntad… o de algo más?", stage(
                figure=fig("think", 540, scale=0.7, path="flat"), props=[prop("dumbbell", 380, 560, size=100, enter="pop"), prop("question", 720, 520, size=90, enter="pop", delay=0.6)])),
        ]),
        scene("C", "mechanism", [
            shot("Walter Mischel les ofreció a unos niños un dulce ahora, o dos si esperaban.", stage(
                figure=fig("stand", 360, scale=0.7), props=[prop("donut", 620, 860, size=80, enter="pop"), prop("donut", 760, 860, size=80, enter="pop", delay=1.2), prop("clock", 690, 620, size=100, state="spin", enter="pop", delay=0.6)])),
            shot("Años después, los que esperaron parecían tener mejores resultados en la escuela.", stage(
                figure=fig("walk", 300, toX=560, scale=0.85, path="rise"), props=[prop("book", 800, 560, size=120, enter="pop", delay=0.4)])),
            shot("Y nació una idea: el autocontrol lo decide todo.", stage(
                props=[prop("dumbbell", 540, 600, size=170, enter="draw", state="glow")], texts=[text("El autocontrol lo decide todo", family="sans", size=48)])),
        ]),
        scene("D", "retention", [
            shot("Pero en 2018, un estudio más grande repitió la prueba.", stage(
                extras=crowd([200, 330, 460, 620, 750, 880], opacity=0.6, scale=0.55),
                counters=[{"from": 1960, "to": 2018, "x": 540, "y": 520, "size": 110, "seconds": 1.2}])),
        ]),
        scene("E", "reveal", [
            shot("Al contar el entorno familiar, esa relación se hizo mucho más pequeña.", stage(
                props=[prop("chart", 540, 620, size=200, state="up", enter="none", to={"state": "down", "at": 0.4})],
                texts=[text("Mucho más pequeña", emphasis=["pequeña"])])),
            shot("Y otro experimento mostró algo todavía más revelador:", stage(
                props=[prop("lightbulb", 540, 600, size=170, state="glow", enter="draw")], camera=cam(1.0, 1.1))),
            shot("los niños esperaban mucho más cuando el adulto, antes, había cumplido una promesa.", stage(
                figure=fig("stand", 360, scale=0.7), extras=[fig("reach", 640, facing=-1, opacity=0.9)],
                props=[prop("bubble", 500, 480, size=110, enter="pop", mark="check", markAt=0.6)],
                texts=[text("Promesa cumplida", family="sans", size=50, emphasis=["cumplida"])])),
        ]),
        scene("F", "mechanism", [
            shot("Esperar no es solo voluntad. Es confianza.", {"type": "kineticTitle", "kicker": "No es solo voluntad", "lines": ["Es", "confianza"], "emphasis": ["confianza"]}, "impact"),
            shot("Si el futuro no suele cumplir, agarrar lo de ahora tiene lógica.", stage(
                figure=fig("reach", 420, scale=0.7, path="fade"), props=[prop("donut", 620, 880, size=80, enter="pop"), prop("bubble", 760, 520, size=100, enter="pop", delay=0.5, mark="cross", markAt=0.6)])),
        ]),
        scene("G", "action", [
            shot("Si te cuesta esperar, construye confianza contigo: hazte promesas pequeñas y cúmplelas.", stage(
                figure=fig("walk", 300, toX=520, path="rise"), props=[prop("checklist", 780, 580, size=140, state="open", enter="draw", delay=0.4)])),
            shot("Cinco minutos cumplidos valen más que un plan perfecto abandonado.", stage(
                props=[prop("checklist", 380, 640, size=150, state="open", enter="pop", mark="check", markAt=0.4), prop("book", 720, 640, size=150, state="dim", enter="pop", delay=0.4, mark="cross", markAt=0.7)],
                texts=[text("5 minutos cumplidos", family="sans", size=50)])),
        ]),
        scene("H", "closer", [
            shot("No eres impaciente. Quizás solo aprendiste que el futuro no siempre llega.", stage(
                figure=fig("walk", 300, toX=560, scale=0.85, path="rise"), props=[prop("donut", 800, 860, size=90, enter="pop", delay=1.0, accent="reward")],
                texts=[text("El futuro sí puede llegar", emphasis=["llegar"])], camera=cam(1.0, 1.06))),
        ]),
        scene("I", "cta", [
            shot("De niño, ¿te habrías comido el dulce o habrías esperado?", stage(
                figure=fig("lookUp", 540, scale=0.7, path="flat"), props=[prop("donut", 720, 880, size=80, enter="pop"), prop("bubble", 720, 520, size=120, enter="pop", delay=0.4)])),
            shot("Te leo en los comentarios.", stage(texts=[text("Te leo", family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "¿Esperar por un dulce predice tu éxito? 🍩 El famoso test se repitió con más niños… y la respuesta no es la que te contaron.",
    ["#psicologia", "#autocontrol", "#mitos", "#crianza", "#aprendeentiktok"],
)

write(v6, v7)
