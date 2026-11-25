"""Day 1 storyboards (videos 4, 19, 12). Writes storyboards/*.json. Hooks are the owner's, verbatim."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "storyboards"


def stage(**kw):
    kw["type"] = "stage"
    return kw


def fig(pose, x=540, **kw):
    return {"pose": pose, "x": x, **kw}


def crowd(xs, pose="stand", scale=0.78, opacity=0.5, facing=None, **kw):
    return [fig(pose, x, scale=scale, opacity=opacity, facing=(facing[i] if facing else (1 if i % 2 else -1)), **kw) for i, x in enumerate(xs)]


def prop(kind, x, y, **kw):
    return {"kind": kind, "x": x, "y": y, **kw}


def text(content, y=330, size=72, **kw):
    return {"content": content, "y": y, "size": size, **kw}


def cam(fz=1.0, tz=1.07, x=540, y=760, pan=0):
    return {"fromZoom": fz, "toZoom": tz, "x": x, "y": y, "panX": pan}


def shot(t, visual, sfx="none"):
    return {"text": t, "visual": visual, "sfx": sfx}


def scene(id_, beat, shots):
    return {"id": id_, "beat": beat, "narration": " ".join(s["text"] for s in shots), "shots": shots}


def sb(id_, title, pillar, sources, scenes, caption, hashtags):
    return {
        "id": id_, "title": title, "pillar": pillar, "format": "secondPerson", "evidenceLevel": "solid",
        "music": "intimo", "sources": sources, "scenes": scenes,
        "social": {"caption": caption, "hashtags": hashtags, "aiLabel": True},
    }


CROWD = [170, 290, 410, 670, 790, 910]

# ------------------------------------------------------------------ 004 bystander
v004 = sb(
    "004-efecto-espectador",
    "El efecto espectador: ¿más gente significa menos ayuda?",
    3,
    [
        {"citation": "Darley, J. M., & Latané, B. (1968). Bystander intervention in emergencies: Diffusion of responsibility. Journal of Personality and Social Psychology, 8(4), 377–383.",
         "doi": "10.1037/h0025589", "supports": "Quienes creían estar solos ayudaban más que quienes creían que otros también escuchaban (difusión de responsabilidad)."},
        {"citation": "Fischer, P., et al. (2011). The bystander-effect: A meta-analytic review on bystander intervention in dangerous and non-dangerous emergencies. Psychological Bulletin, 137(4), 517–537.",
         "doi": "10.1037/a0023304", "supports": "Metaanálisis: el efecto existe, pero se debilita en emergencias claramente peligrosas."},
        {"citation": "Philpot, R., Liebst, L. S., Levine, M., Bernasco, W., & Lindegaard, M. R. (2020). Would I be helped? Cross-national CCTV footage shows that intervention is the norm in public conflicts. American Psychologist, 75(1), 66–75.",
         "doi": "10.1037/amp0000469", "supports": "219 conflictos reales en tres países: en 9 de cada 10 al menos una persona intervino; más testigos, más probabilidad de ayuda."},
    ],
    [
        scene("A", "hook", [
            shot("Si te pasa algo en una calle llena de gente,", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("slump", 540, path="flat"),
                extras=crowd(CROWD), texts=[text("Una calle llena de gente", emphasis=["gente"])],
                camera=cam(1.0, 1.08)), "impact"),
            shot("tal vez nadie te ayude.", stage(
                figure=fig("slump", 540, path="flat"),
                extras=[fig("walk", 290, toX=150, facing=-1, scale=0.78, opacity=0.5), fig("stand", 410, scale=0.78, opacity=0.4, facing=-1),
                        fig("stand", 670, scale=0.78, opacity=0.4, facing=1), fig("walk", 790, toX=940, facing=1, scale=0.78, opacity=0.5)],
                texts=[text("…y nadie ayuda", emphasis=["nadie"])], camera=cam(1.08, 1.14))),
            shot("Eso nos enseñaron.", stage(
                props=[prop("book", 540, 690, size=200, enter="draw", label="LO QUE APRENDIMOS")],
                texts=[text("Eso nos enseñaron", family="sans", size=60)], camera=cam(1.0, 1.06))),
        ]),
        scene("B", "question", [
            shot("¿Más testigos significa menos ayuda?", stage(
                extras=crowd([300, 400, 500], opacity=0.6, scale=0.7),
                props=[prop("chart", 850, 680, size=150, state="down", label="AYUDA", enter="draw")],
                counters=[{"from": 1, "to": 30, "x": 380, "y": 560, "size": 120, "seconds": 1.4, "suffix": " testigos"}],
                texts=[text("¿Más testigos, menos ayuda?", family="sans", size=58, emphasis=["menos"])])),
        ]),
        scene("C", "mechanism", [
            shot("En los años 60, Darley y Latané simularon una emergencia.", stage(
                figure=fig("think", 360), props=[prop("bubble", 720, 640, size=190, enter="pop", delay=0.3, label="¡AYUDA!")],
                texts=[text("Darley y Latané · años 60", family="sans", size=46)])),
            shot("Quienes creían estar solos ayudaban más", stage(
                figure=fig("walk", 300, toX=600, path="rise"),
                props=[prop("bubble", 800, 600, size=150, label="¡AYUDA!", enter="none", mark="check", markAt=0.7)],
                texts=[text("Solos: ayudaban más", family="sans", size=52, emphasis=["más"])])),
            shot("que quienes creían que otros también escuchaban.", stage(
                figure=fig("stand", 540), extras=crowd([260, 380, 700, 820], opacity=0.45, scale=0.72),
                props=[prop("bubble", 800, 560, size=130, label="¡AYUDA!", enter="none", mark="question", markAt=0.5),
                       prop("clock", 300, 560, size=110, state="spin", enter="pop", delay=0.4)],
                texts=[text("Con otros: dudaban", family="sans", size=52, emphasis=["dudaban"])])),
            shot("Se llama difusión de responsabilidad:", {"type": "kineticTitle", "kicker": "Se llama", "lines": ["Difusión de", "responsabilidad"], "emphasis": ["responsabilidad"]}, "impact"),
            shot("si todos pueden ayudar, nadie se siente obligado.", stage(
                extras=crowd([200, 340, 480, 620, 760, 900], opacity=0.55, scale=0.72),
                texts=[text("Si todos pueden, nadie se siente obligado", family="sans", size=48, emphasis=["nadie"])], camera=cam(1.06, 1.0))),
        ]),
        scene("D", "demonstration", [
            shot("Un metaanálisis confirmó el efecto…", stage(
                props=[prop("chart", 540, 640, size=220, state="down", enter="draw", mark="check", markAt=0.6)],
                texts=[text("Metaanálisis", family="sans", size=56)])),
            shot("pero encontró que se debilita en emergencias claramente peligrosas.", stage(
                props=[prop("chart", 540, 640, size=220, state="down", enter="none", to={"state": "up", "at": 0.3}),
                       prop("lightbulb", 820, 500, size=110, state="glow", enter="pop", delay=0.5)],
                texts=[text("En el peligro real, se debilita", family="sans", size=50, emphasis=["se debilita"])])),
        ]),
        scene("E", "retention", [
            shot("Y entonces alguien hizo lo que casi nadie había hecho:", stage(
                figure=fig("walk", 300, toX=480, path="flat"), props=[prop("cctv", 760, 500, size=200, enter="draw")], camera=cam(1.0, 1.06))),
            shot("mirar la vida real.", stage(
                props=[prop("cctv", 760, 500, size=200, enter="none", state="glow")],
                texts=[text("La vida real", emphasis=["real"])], camera=cam(1.0, 1.22, 760, 520))),
        ]),
        scene("F", "reveal", [
            shot("Un equipo analizó más de 200 conflictos reales grabados por cámaras en tres países.", stage(
                props=[prop("cctv", 830, 470, size=120, enter="pop")],
                counters=[{"from": 0, "to": 200, "prefix": "+", "x": 500, "y": 620, "size": 150, "seconds": 1.6}],
                texts=[text("conflictos reales · 3 países", y=760, family="sans", size=42)])),
            shot("En 9 de cada 10, al menos una persona intervino.", stage(
                extras=crowd([200, 330, 460, 590, 720, 850], opacity=0.4, scale=0.66),
                counters=[{"from": 0, "to": 9, "suffix": " de 10", "x": 540, "y": 600, "size": 170, "seconds": 1.0, "accent": "reward"}],
                texts=[text("alguien ayudó", y=760, family="sans", size=46)])),
            shot("Y cuantas más personas había, más probable era que alguien ayudara.", stage(
                figure=fig("walk", 840, toX=600, facing=-1, path="flat"),
                extras=[fig("slump", 460, scale=0.9, opacity=0.9)] + crowd([180, 300, 900], opacity=0.4, scale=0.7),
                props=[prop("chart", 800, 470, size=120, state="up", enter="pop", delay=0.3, label="AYUDA")])),
        ]),
        scene("G", "action", [
            shot("Si necesitas ayuda, no le hables a la multitud: señala a una persona.", stage(
                figure=fig("point", 300),
                extras=[fig("stand", 580, scale=0.78, opacity=0.4, facing=-1), fig("stand", 700, scale=0.78, opacity=1, facing=-1),
                        fig("stand", 820, scale=0.78, opacity=0.4, facing=-1), fig("stand", 930, scale=0.78, opacity=0.4, facing=-1)],
                texts=[text("«Tú. Ayúdame.»", family="sans", size=54, emphasis=["Tú"])])),
            shot("Y si eres testigo, no esperes a que otro empiece.", stage(
                figure=fig("walk", 280, toX=560, path="rise"), extras=crowd([700, 820, 930], opacity=0.4, scale=0.72),
                texts=[text("No esperes", family="sans", size=56, emphasis=["No esperes"])])),
        ]),
        scene("H", "closer", [
            shot("La multitud no es indiferente.", stage(
                extras=crowd([200, 330, 460, 620, 750, 880], opacity=0.6, scale=0.75, facing=[1, 1, 1, -1, -1, -1]),
                texts=[text("No es indiferencia", emphasis=["indiferencia"])], camera=cam(1.0, 1.05))),
            shot("Solo está esperando que alguien dé el primer paso.", stage(
                figure=fig("walk", 380, toX=620, path="flat", pathTo=980),
                extras=[fig("walk", 220, toX=400, scale=0.75, opacity=0.5), fig("walk", 140, toX=300, scale=0.75, opacity=0.4)],
                texts=[text("El primer paso", emphasis=["primer paso"])], camera=cam(1.0, 1.08, 600, 800, 30))),
        ]),
        scene("I", "cta", [
            shot("¿Alguna vez ayudaste a un desconocido, o alguien te ayudó a ti?", stage(
                figure=fig("reach", 400), extras=[fig("stand", 680, facing=-1, scale=1, opacity=0.9)],
                props=[prop("bubble", 540, 560, size=150, enter="pop", delay=0.4)])),
            shot("Cuéntalo abajo.", stage(texts=[text("Cuéntalo abajo", family="sans", size=60, emphasis=["abajo"])],
                                          props=[prop("bubble", 540, 640, size=160, enter="pop")])),
        ]),
    ],
    "¿Más gente significa menos ayuda? 👀 Eso nos enseñaron… hasta que alguien revisó cámaras reales en tres países. El resultado te va a sorprender.",
    ["#psicologia", "#efectoespectador", "#comportamiento", "#ciencia", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 019 loss aversion
v019 = sb(
    "019-aversion-perdida",
    "La aversión a la pérdida: por qué perder duele más que ganar",
    4,
    [
        {"citation": "Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. Econometrica, 47(2), 263–291.",
         "doi": "10.2307/1914185", "supports": "Teoría prospectiva: resultados evaluados como ganancias o pérdidas desde un punto de referencia; las pérdidas pesan más."},
        {"citation": "Brown, A. L., Imai, T., Vieider, F. M., & Camerer, C. F. (2024). Meta-analysis of empirical estimates of loss aversion. Journal of Economic Literature, 62(2), 485–516.",
         "doi": "10.1257/jel.20221698", "supports": "607 estimaciones de 150 artículos; coeficiente medio ≈ 1,96 (casi el doble); varía según el diseño y el contexto."},
    ],
    [
        scene("A", "hook", [
            shot("Perder cien dólares duele más de lo que te alegra ganar cien.", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("think", 230, path="flat"),
                props=[prop("balance", 560, 760, size=260, enter="none", to={"state": "down", "at": 0.35})],
                counters=[{"from": 0, "to": 100, "prefix": "−$", "x": 420, "y": 560, "size": 96, "seconds": 0.6, "accent": "red"},
                          {"from": 0, "to": 100, "prefix": "+$", "x": 700, "y": 560, "size": 96, "seconds": 0.6}],
                texts=[text("Perder pesa más", emphasis=["Perder"])], camera=cam(1.0, 1.08)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Por qué perder pesa tanto?", stage(
                figure=fig("slump", 460, path="fall"),
                props=[prop("coins", 700, 520, size=130, enter="drop"), prop("question", 700, 360, size=90, enter="pop", delay=0.5)],
                texts=[text("¿Por qué pesa tanto?", family="sans", size=58)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1979, Daniel Kahneman y Amos Tversky propusieron", stage(
                props=[prop("lightbulb", 540, 620, size=180, state="glow", enter="draw")],
                texts=[text("Kahneman y Tversky · 1979", family="sans", size=48)])),
            shot("que evaluamos todo como ganancias o pérdidas desde un punto de referencia,", stage(
                figure=fig("stand", 540, path="flat", pathFrom=120, pathTo=960),
                texts=[text("← pérdidas", x=300, y=700, family="sans", size=40, accent="red"), text("ganancias →", x=780, y=700, family="sans", size=40),
                       text("Tu punto de referencia", family="sans", size=50, emphasis=["referencia"])], camera=cam(1.0, 1.05))),
            shot("y que las pérdidas pesan más.", stage(
                props=[prop("balance", 540, 720, size=280, enter="none", to={"state": "down", "at": 0.25})],
                texts=[text("−", x=420, y=520, size=90, family="sans", accent="red"), text("+", x=660, y=520, size=90, family="sans")])),
        ]),
        scene("D", "demonstration", [
            shot("Por eso muchas personas rechazan lanzar una moneda", stage(
                figure=fig("stand", 330, path="flat"), props=[prop("coins", 660, 640, size=150, state="spin", enter="pop", mark="cross", markAt=0.75)])),
            shot("en la que podrían ganar 120 y perder 100,", stage(
                props=[prop("coins", 540, 700, size=120, state="spin", enter="none")],
                counters=[{"from": 0, "to": 120, "prefix": "+$", "x": 720, "y": 540, "size": 104, "seconds": 0.8},
                          {"from": 0, "to": 100, "prefix": "−$", "x": 360, "y": 540, "size": 104, "seconds": 0.8, "accent": "red"}])),
            shot("aunque en promedio les convenga.", stage(
                counters=[{"from": 0, "to": 10, "prefix": "+$", "x": 540, "y": 600, "size": 140, "seconds": 0.7}],
                texts=[text("en promedio, por lanzamiento", y=740, family="sans", size=40)])),
        ]),
        scene("E", "retention", [
            shot("¿Y cuánto más pesa una pérdida?", stage(
                props=[prop("balance", 540, 720, size=260, state="down", enter="pop"), prop("question", 540, 440, size=100, enter="pop", delay=0.4)],
                camera=cam(1.0, 1.12))),
        ]),
        scene("F", "reveal", [
            shot("Un metaanálisis de 2024 reunió más de 600 estimaciones de 150 artículos.", stage(
                counters=[{"from": 0, "to": 607, "x": 360, "y": 600, "size": 120, "seconds": 1.4}, {"from": 0, "to": 150, "x": 740, "y": 600, "size": 120, "seconds": 1.4, "delay": 0.3}],
                texts=[text("estimaciones", x=360, y=720, family="sans", size=36), text("artículos", x=740, y=720, family="sans", size=36),
                       text("Metaanálisis · 2024", family="sans", size=48)])),
            shot("En promedio, una pérdida pesa casi el doble que una ganancia equivalente.", stage(
                props=[prop("balance", 540, 780, size=260, enter="none", to={"state": "down", "at": 0.2})],
                texts=[text("casi ×2", y=520, size=110, emphasis=["×2"])], camera=cam(1.0, 1.08))),
            shot("Pero es un promedio: varía según la persona y el contexto.", stage(
                props=[prop("balance", 260, 700, size=130, state="normal"), prop("balance", 540, 700, size=130, state="down", delay=0.2),
                       prop("balance", 820, 700, size=130, state="up", delay=0.4)],
                texts=[text("Varía según la persona", family="sans", size=48, emphasis=["persona"])])),
        ]),
        scene("G", "action", [
            shot("Cuando una decisión te dé miedo, añade una pregunta.", stage(
                figure=fig("think", 360, path="fork"), props=[prop("question", 360, 560, size=80, enter="pop", delay=0.5)])),
            shot("No solo ¿qué pierdo si lo hago?,", stage(
                texts=[text("¿Qué pierdo si lo hago?", family="sans", size=54, y=600)], props=[prop("balance", 540, 820, size=150, state="down")])),
            shot("también: ¿qué pierdo si no lo hago?", stage(
                figure=fig("walk", 300, toX=560, path="fork"),
                texts=[text("¿Qué pierdo si NO lo hago?", family="sans", size=54, emphasis=["NO"])])),
        ]),
        scene("H", "closer", [
            shot("A veces no eliges lo mejor. Eliges lo que menos te hace sentir que pierdes.",
                 {"type": "closer", "line": "No eliges lo mejor. Eliges lo que menos se siente como perder.", "emphasis": ["perder"], "source": "Kahneman y Tversky, 1979 · Brown et al., 2024"}, "shimmer"),
        ]),
        scene("I", "cta", [
            shot("¿Qué decisión estás evitando por miedo a perder?", stage(
                figure=fig("lookUp", 540, path="fade"), props=[prop("bubble", 700, 520, size=140, enter="pop", delay=0.3)])),
            shot("Cuéntame.", stage(texts=[text("Cuéntame", family="sans", size=62)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "¿Por qué perder 100 duele más que ganar 100? 🧠 Un metaanálisis con más de 600 estimaciones tiene la respuesta, y una pregunta que cambia cómo decides.",
    ["#psicologia", "#dinero", "#decisiones", "#economiaconductual", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 012 fear of rejection
v012 = sb(
    "012-miedo-rechazo",
    "El miedo al rechazo: le caes mejor a la gente de lo que crees",
    3,
    [
        {"citation": "Gilovich, T., Medvec, V. H., & Savitsky, K. (2000). The spotlight effect in social judgment: An egocentric bias in estimates of the salience of one's own actions and appearance. Journal of Personality and Social Psychology, 78(2), 211–222.",
         "doi": "10.1037/0022-3514.78.2.211", "supports": "Quienes llevaban una camiseta vergonzosa estimaron que cerca de la mitad lo notaría; en realidad, alrededor de uno de cada cuatro."},
        {"citation": "Boothby, E. J., Cooney, G., Sandstrom, G. M., & Clark, M. S. (2018). The liking gap in conversations: Do people like us more than we think? Psychological Science, 29(11), 1742–1756.",
         "doi": "10.1177/0956797618783714", "supports": "Tras conversar, las personas subestiman sistemáticamente cuánto le agradaron a su compañero (brecha de agrado)."},
    ],
    [
        scene("A", "hook", [
            shot("Después de conocer a alguien,", stage(
                figure=fig("reach", 400, path="flat", pathTo=760), extras=[fig("stand", 680, facing=-1, scale=1, opacity=0.9)],
                props=[prop("bubble", 540, 560, size=120, enter="none")],
                texts=[text("Después de conocer a alguien…", family="sans", size=54)]), "impact"),
            shot("crees que le caíste peor de lo que le caíste en realidad.", stage(
                figure=fig("walk", 400, toX=250, facing=-1, path="flat"), extras=[fig("walk", 680, toX=830, facing=1, opacity=0.9)],
                texts=[text("«Le caí mal»", x=280, y=560, family="sans", size=40, accent="red", delay=0.3),
                       text("«Me cayó bien»", x=800, y=560, family="sans", size=40, delay=0.9)])),
        ]),
        scene("B", "question", [
            shot("¿Por qué el miedo al juicio de los demás nos frena tanto?", stage(
                figure=fig("slump", 540, path="flat"), extras=crowd([200, 330, 750, 880], opacity=0.35, scale=0.72, facing=[1, 1, -1, -1]),
                props=[prop("question", 540, 480, size=90, enter="pop", delay=0.4)],
                texts=[text("¿Por qué nos frena?", family="sans", size=56)])),
        ]),
        scene("C", "mechanism", [
            shot("En un experimento, unos estudiantes entraron a una sala con una camiseta vergonzosa.", stage(
                spotlight={"x": 520}, figure=fig("walk", 240, toX=520, path="flat"), props=[prop("shirt", 800, 600, size=150, enter="draw", delay=0.4)],
                camera=cam(1.0, 1.06))),
            shot("Calcularon que cerca de la mitad de los presentes lo notaría.", stage(
                figure=fig("stand", 300), counters=[{"from": 0, "to": 50, "suffix": "%", "x": 660, "y": 580, "size": 150, "seconds": 1.0}],
                texts=[text("lo que creyeron", x=660, y=700, family="sans", size=38)])),
            shot("En realidad, lo notó alrededor de uno de cada cuatro.", stage(
                extras=[fig("lookUp", 300, scale=0.75, opacity=1), fig("stand", 450, scale=0.75, opacity=0.3, facing=-1),
                        fig("stand", 600, scale=0.75, opacity=0.3), fig("stand", 750, scale=0.75, opacity=0.3, facing=-1)],
                texts=[text("1 de cada 4", family="sans", size=90)], camera=cam(1.0, 1.05))),
        ]),
        scene("D", "demonstration", [
            shot("Sentimos que todos nos miran,", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("stand", 540),
                extras=crowd([200, 320, 760, 880], opacity=0.45, scale=0.72, facing=[1, 1, -1, -1]))),
            shot("pero cada persona está ocupada pensando en sí misma.", stage(
                figure=fig("stand", 540), extras=[fig("phone", 220, scale=0.72, opacity=0.5, facing=-1), fig("think", 360, scale=0.72, opacity=0.5, facing=-1),
                                                  fig("phone", 740, scale=0.72, opacity=0.5), fig("think", 880, scale=0.72, opacity=0.5)],
                texts=[text("Cada uno piensa en sí mismo", family="sans", size=48)])),
        ]),
        scene("E", "retention", [
            shot("Y después de una conversación pasa algo todavía más curioso.", stage(
                figure=fig("stand", 400), extras=[fig("stand", 680, facing=-1, opacity=0.9)],
                props=[prop("bubble", 540, 540, size=120, enter="pop"), prop("question", 540, 380, size=80, enter="pop", delay=0.8)])),
        ]),
        scene("F", "reveal", [
            shot("Investigadores pusieron a conversar a desconocidos", stage(
                figure=fig("reach", 400), extras=[fig("point", 680, facing=-1, opacity=0.9)],
                props=[prop("bubble", 470, 520, size=100, enter="pop"), prop("bubble", 620, 480, size=100, enter="pop", delay=0.5)])),
            shot("y luego les preguntaron cuánto les había gustado el otro y cuánto creían haberle gustado.", stage(
                props=[prop("balance", 540, 760, size=260, enter="pop")],
                texts=[text("Lo que creíste", x=380, y=560, family="sans", size=38), text("Lo que sintió", x=700, y=560, family="sans", size=38)])),
            shot("La gente subestimaba sistemáticamente cuánto había agradado.", stage(
                props=[prop("balance", 540, 760, size=260, enter="none", to={"state": "up", "at": 0.25})],
                texts=[text("Le agradaste más", family="sans", size=54, emphasis=["más"])], camera=cam(1.0, 1.08))),
            shot("Lo llamaron la brecha de agrado.", {"type": "kineticTitle", "kicker": "Lo llamaron", "lines": ["La brecha", "de agrado"], "emphasis": ["agrado"]}, "impact"),
        ]),
        scene("G", "action", [
            shot("Antes de no escribir ese mensaje o no hacer esa pregunta,", stage(
                figure=fig("phone", 480, holding="phone"), props=[prop("phone", 760, 600, size=150, state="typing", enter="pop", delay=0.3)])),
            shot("recuerda: el juicio que imaginas es más duro que el real.", stage(
                props=[prop("balance", 540, 760, size=220, enter="none", state="normal", to={"state": "down", "at": 0.3})],
                texts=[text("Imaginado", x=400, y=580, family="sans", size=38, accent="red"), text("Real", x=680, y=580, family="sans", size=38),
                       text("Más duro en tu cabeza", family="sans", size=50)])),
            shot("Empieza por algo pequeño.", stage(
                figure=fig("walk", 380, toX=520, path="rise"), texts=[text("Algo pequeño", family="sans", size=56)])),
        ]),
        scene("H", "closer", [
            shot("El rechazo que temes vive sobre todo en tu cabeza.", stage(
                figure=fig("think", 540), props=[prop("bubble", 640, 420, size=120, enter="pop", state="dim")],
                texts=[text("Vive en tu cabeza", emphasis=["cabeza"])])),
            shot("La conexión que te pierdes es real.", stage(
                figure=fig("walk", 300, toX=470, path="flat", pathTo=760), extras=[fig("walk", 800, toX=620, facing=-1, opacity=0.9)],
                texts=[text("La conexión es real", emphasis=["real"], accent="reward", delay=0.6)], camera=cam(1.0, 1.08))),
        ]),
        scene("I", "cta", [
            shot("¿Qué harías hoy si supieras que nadie te va a juzgar?", stage(
                figure=fig("lookUp", 540, path="rise"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.4)])),
            shot("Comenta.", stage(texts=[text("Comenta", family="sans", size=62)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
        ]),
    ],
    "Le caes mejor a la gente de lo que crees 💬 La ciencia lo llama «brecha de agrado». Mira hasta el final antes de dejar de escribir ese mensaje.",
    ["#psicologia", "#confianza", "#relaciones", "#autoestima", "#aprendeentiktok"],
)

for v in (v004, v019, v012):
    (OUT / f"{v['id']}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("wrote", v["id"])
