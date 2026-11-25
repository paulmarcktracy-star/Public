"""Videos 13, 15, 17, 18, 20, 21. Hooks verbatim. Natural spoken Spanish. Cinematic camera."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbkit import cam, crowd, fig, prop, sb, scene, shot, stage, text, write  # noqa: E402


def CTA(q, last="Te leo en los comentarios.", word="Te leo"):
    return scene("I", "cta", [
        shot(q, stage(figure=fig("lookUp", 540, path="flat"), props=[prop("bubble", 720, 500, size=130, enter="pop", delay=0.3)])),
        shot(last, stage(texts=[text(word, family="sans", size=60)], props=[prop("bubble", 540, 640, size=150, enter="pop")])),
    ])


def closer(line, emph, source, spoken):
    return shot(spoken, {"type": "closer", "line": line, "emphasis": emph, "source": source}, "shimmer")


# ------------------------------------------------------------------ 013 social proof (Asch)
v13 = sb(
    "013-prueba-social", "La prueba social: por qué seguimos a la mayoría", 3,
    [
        {"citation": "Asch, S. E. (1956). Studies of independence and conformity: I. A minority of one against a unanimous majority. Psychological Monographs, 70(9), 1–70.",
         "doi": "10.1037/h0093718", "supports": "La mayoría cedió al menos una vez; cerca de uno de cada cuatro nunca cedió; un solo aliado reducía mucho la conformidad."},
        {"citation": "Bond, R., & Smith, P. B. (1996). Culture and conformity: A meta-analysis of studies using Asch's line judgment task. Psychological Bulletin, 119(1), 111–137.",
         "doi": "10.1037/0033-2909.119.1.111", "supports": "Metaanálisis: la conformidad varía según la cultura y la época."},
    ],
    [
        scene("A", "hook", [
            shot("Puedes ver la respuesta correcta con tus propios ojos…", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("lookUp", 540, path="flat"),
                props=[prop("chart", 540, 460, size=150, state="normal", enter="none")], camera=cam(1.0, 1.06)), "impact"),
            shot("y aun así decir la incorrecta.", stage(
                figure=fig("stand", 540), extras=crowd([200, 320, 760, 880], opacity=0.55, scale=0.8, pose="point", facing=[1, 1, -1, -1]),
                props=[prop("question", 540, 440, size=80, enter="pop", mark="cross", markAt=0.5)])),
        ]),
        scene("B", "question", [
            shot("¿Por qué seguimos a la mayoría, incluso cuando se equivoca?", stage(
                figure=fig("walk", 300, toX=500, path="flat"), extras=crowd([620, 740, 860], opacity=0.6, scale=0.8, pose="walk"),
                texts=[text("¿Por qué la seguimos?", family="sans", size=54)])),
        ]),
        scene("C", "mechanism", [
            shot("En los años cincuenta, Solomon Asch mostró a unos grupos tres líneas.", stage(
                props=[prop("chart", 540, 600, size=200, enter="draw")], texts=[text("Solomon Asch · años 50", family="sans", size=46)])),
            shot("Había que decir cuál medía lo mismo que otra. Era obvio.", stage(
                props=[prop("chart", 540, 600, size=200, enter="none", mark="check", markAt=0.5)], texts=[text("Era obvio", emphasis=["obvio"])])),
            shot("Pero los demás del grupo eran actores, y a veces daban la respuesta equivocada a propósito.", stage(
                figure=fig("think", 540), extras=crowd([200, 320, 760, 880], opacity=0.6, scale=0.8, pose="point", facing=[1, 1, -1, -1]))),
        ]),
        scene("D", "demonstration", [
            shot("La mayoría de los participantes cedió al menos una vez.", stage(
                figure=fig("slump", 540), extras=crowd([200, 320, 760, 880], opacity=0.6, scale=0.8, facing=[1, 1, -1, -1]),
                texts=[text("Cedieron", emphasis=["Cedieron"])])),
        ]),
        scene("E", "retention", [
            shot("Pero hay un detalle que casi nadie cuenta.", stage(
                figure=fig("stand", 540, path="fade"), props=[prop("lightbulb", 540, 440, size=100, state="glow", enter="pop", delay=0.3)], camera=cam(1.0, 1.08))),
        ]),
        scene("F", "reveal", [
            shot("Más o menos una de cada cuatro personas nunca cedió.", stage(
                extras=[fig("stand", 300, scale=0.8, opacity=1), fig("slump", 450, scale=0.8, opacity=0.35), fig("slump", 600, scale=0.8, opacity=0.35), fig("slump", 750, scale=0.8, opacity=0.35)],
                texts=[text("1 de cada 4", family="sans", size=80)])),
            shot("Y cuando había un solo aliado que decía la verdad,", stage(
                figure=fig("stand", 460), extras=[fig("stand", 640, facing=-1, opacity=1)] + crowd([200, 860], opacity=0.4, scale=0.8),
                props=[prop("bubble", 640, 460, size=100, enter="pop", delay=0.3, accent="reward")])),
            shot("la presión del grupo caía muchísimo.", stage(
                props=[prop("gauge", 540, 600, size=200, state="normal", enter="pop", to={"state": "down", "at": 0.25})],
                texts=[text("Un aliado lo cambia todo", family="sans", size=50, emphasis=["aliado"])])),
        ]),
        scene("G", "action", [
            shot("No necesitas ser valiente contra todos. Solo necesitas una voz.", stage(
                figure=fig("stand", 540, path="fork"), texts=[text("Solo una voz", emphasis=["una voz"])])),
            shot("Sé esa voz para alguien.", stage(
                figure=fig("walk", 300, toX=500, path="flat"), extras=[fig("slump", 720, facing=-1, opacity=0.9)])),
        ]),
        scene("H", "closer", [closer("La mayoría no siempre tiene razón. A veces solo tiene volumen.", ["volumen"], "Asch, 1956 · Bond y Smith, 1996",
                                      "La mayoría no siempre tiene razón. A veces solo tiene volumen.")]),
        CTA("¿Alguna vez dijiste que sí solo porque todos decían que sí?", "Cuéntamelo en los comentarios.", "Cuéntamelo"),
    ],
    "Puedes ver la respuesta correcta y aun así decir la incorrecta 👥 El experimento de Asch tiene un detalle que casi nadie cuenta.",
    ["#psicologia", "#presionsocial", "#comportamiento", "#ciencia", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 015 scarcity
v15 = sb(
    "015-escasez", "La escasez psicológica: por qué queremos más lo que se acaba", 4,
    [
        {"citation": "Worchel, S., Lee, J., & Adewole, A. (1975). Effects of supply and demand on ratings of object value. Journal of Personality and Social Psychology, 32(5), 906–914.",
         "doi": "10.1037/0022-3514.32.5.906", "supports": "Galletas de un frasco con 2 valoradas como más deseables que las de un frasco con 10; las que pasaron de 10 a 2, las mejor valoradas."},
        {"citation": "Lynn, M. (1991). Scarcity effects on value: A quantitative review of the commodity theory literature. Psychology & Marketing, 8(1), 43–57.",
         "doi": "10.1002/mar.4220080105", "supports": "Metaanálisis: la escasez aumenta el valor percibido."},
    ],
    [
        scene("A", "hook", [
            shot("¿Por qué queremos más algo justo cuando está a punto de agotarse?", stage(
                spotlight={"x": 640, "snap": True}, figure=fig("reach", 400, path="flat"),
                props=[prop("jar", 680, 640, size=170, enter="none")], counters=[{"from": 10, "to": 2, "x": 680, "y": 420, "size": 100, "seconds": 2.0, "delay": 0.6}],
                texts=[text("Quedan pocas", emphasis=["pocas"])], camera=cam(1.0, 1.06)), "impact"),
        ]),
        scene("B", "question", [
            shot("Unas simples galletas tienen la respuesta.", stage(
                props=[prop("jar", 540, 640, size=190, enter="pop"), prop("question", 540, 420, size=80, enter="pop", delay=0.5)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1975, Stephen Worchel le dio a unas personas un frasco con galletas.", stage(
                figure=fig("reach", 400), props=[prop("jar", 680, 640, size=150, enter="draw")], texts=[text("Worchel · 1975", family="sans", size=46)])),
            shot("Unos frascos tenían diez. Otros, solo dos.", stage(
                props=[prop("jar", 380, 640, size=150, enter="pop"), prop("jar", 700, 640, size=150, enter="pop", delay=0.4)],
                counters=[{"from": 0, "to": 10, "x": 380, "y": 830, "size": 90, "seconds": 0.5}, {"from": 0, "to": 2, "x": 700, "y": 830, "size": 90, "seconds": 0.4, "delay": 0.4}])),
            shot("Las del frasco casi vacío parecieron más deseables. Y eran las mismas galletas.", stage(
                props=[prop("jar", 540, 640, size=170, enter="pop", state="glow")], texts=[text("Las mismas galletas", emphasis=["mismas"])])),
        ]),
        scene("D", "demonstration", [
            shot("Un metaanálisis lo confirmó: lo escaso nos parece más valioso.", stage(
                props=[prop("chart", 540, 620, size=200, state="up", enter="draw", mark="check", markAt=0.6)])),
        ]),
        scene("E", "retention", [
            shot("Pero el resultado más potente vino de otro grupo.", stage(
                extras=crowd([300, 420, 660, 780], opacity=0.6, scale=0.75), props=[prop("question", 540, 440, size=80, enter="pop", delay=0.4)], camera=cam(1.0, 1.08))),
        ]),
        scene("F", "reveal", [
            shot("A algunos les cambiaban el frasco delante de sus ojos: de diez galletas, pasaba a dos.", stage(
                figure=fig("stand", 380), props=[prop("jar", 680, 640, size=160, enter="pop")],
                counters=[{"from": 10, "to": 2, "x": 680, "y": 420, "size": 110, "seconds": 1.6, "delay": 0.8}])),
            shot("Esas fueron las mejor valoradas de todas.", stage(
                props=[prop("jar", 540, 640, size=190, state="glow", enter="pop", accent="reward")], texts=[text("Las mejor valoradas", emphasis=["mejor"])], camera=cam(1.0, 1.1))),
            shot("Perder algo que tenías pesa más que no haberlo tenido nunca.", stage(
                figure=fig("slump", 540, path="fall"), texts=[text("Perder pesa más", family="sans", size=54)])),
        ]),
        scene("G", "action", [
            shot("Así que, cuando veas «últimas unidades» o «solo por hoy»,", stage(
                props=[prop("tag", 540, 600, size=200, label="ÚLTIMAS", enter="drop")])),
            shot("pregúntate: ¿lo querría igual si hubiera cien?", stage(
                figure=fig("think", 400, path="fork"), counters=[{"from": 2, "to": 100, "x": 720, "y": 520, "size": 110, "seconds": 1.2}])),
        ]),
        scene("H", "closer", [closer("La escasez no cambia lo que algo vale. Cambia lo que sientes que vale.", ["sientes"], "Worchel et al., 1975 · Lynn, 1991",
                                      "La escasez no cambia lo que algo vale. Cambia lo que sientes que vale.")]),
        CTA("¿Qué compraste alguna vez solo porque se estaba acabando?", "Cuéntame en los comentarios.", "Cuéntame"),
    ],
    "¿Por qué queremos más lo que está por acabarse? 🍪 Un experimento con galletas lo explica… y te ayuda a no caer en el próximo «últimas unidades».",
    ["#psicologia", "#compras", "#marketing", "#dinero", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 017 false memories
v17 = sb(
    "017-falsos-recuerdos", "Los falsos recuerdos: tu memoria puede engañarte", 1,
    [
        {"citation": "Loftus, E. F., & Palmer, J. C. (1974). Reconstruction of automobile destruction: An example of the interaction between language and memory. Journal of Verbal Learning and Verbal Behavior, 13(5), 585–589.",
         "doi": "10.1016/S0022-5371(74)80011-3", "supports": "«Estrellaron» frente a «golpearon»: más velocidad estimada y más recuerdos de vidrios rotos inexistentes."},
        {"citation": "Scoboria, A., Wade, K. A., Lindsay, D. S., et al. (2017). A mega-analysis of memory reports from eight peer-reviewed false memory implantation studies. Memory, 25(2), 146–163.",
         "doi": "10.1080/09658211.2016.1260747", "supports": "Ocho estudios, más de 400 participantes: alrededor del 30 % formó un recuerdo falso."},
    ],
    [
        scene("A", "hook", [
            shot("Puedes recordar con detalle algo que nunca te pasó.", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("think", 420, path="flat"),
                props=[prop("bubble", 640, 440, size=150, enter="none", state="glow")], texts=[text("Algo que nunca pasó", emphasis=["nunca"])], camera=cam(1.0, 1.06)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Cómo puede engañarte tu memoria, si la sientes tan real?", stage(
                props=[prop("brain", 540, 600, size=200, state="glow", enter="pop"), prop("question", 540, 400, size=80, enter="pop", delay=0.5)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1974, Elizabeth Loftus le mostró a unas personas el video de un choque.", stage(
                props=[prop("phone", 540, 620, size=180, enter="draw")], texts=[text("Elizabeth Loftus · 1974", family="sans", size=46)])),
            shot("Después preguntó a qué velocidad iban los autos cuando se «estrellaron»… o cuando se «golpearon».", stage(
                texts=[text("«Se estrellaron»", x=540, y=560, family="sans", size=52), text("«Se golpearon»", x=540, y=700, family="sans", size=44, delay=1.2)],
                props=[prop("clock", 540, 860, size=90, state="spin", enter="pop")])),
            shot("Con la palabra más fuerte, calcularon más velocidad.", stage(
                props=[prop("gauge", 540, 620, size=200, state="normal", enter="pop", to={"state": "up", "at": 0.3})])),
        ]),
        scene("D", "demonstration", [
            shot("Y una semana después, más personas recordaban vidrios rotos que nunca aparecieron.", stage(
                props=[prop("phone", 540, 620, size=160, enter="pop", mark="question", markAt=0.6)], texts=[text("Vidrios que no existían", family="sans", size=48)])),
            shot("Recordar no es reproducir un video. Es reconstruir la escena cada vez.", stage(
                props=[prop("book", 540, 620, size=180, state="open", enter="draw")], texts=[text("Reconstruimos", emphasis=["Reconstruimos"])])),
        ]),
        scene("E", "retention", [
            shot("Pero, ¿se puede crear un recuerdo completo desde cero?", stage(
                figure=fig("stand", 540, path="fade"), props=[prop("question", 540, 420, size=90, enter="pop", delay=0.3)], camera=cam(1.0, 1.08))),
        ]),
        scene("F", "reveal", [
            shot("Una revisión de ocho estudios juntó a más de cuatrocientas personas.", stage(
                extras=crowd([200, 330, 460, 620, 750, 880], opacity=0.6, scale=0.6), counters=[{"from": 0, "to": 400, "prefix": "+", "x": 540, "y": 460, "size": 110, "seconds": 1.2}])),
            shot("A todas les sugirieron un recuerdo falso de su infancia.", stage(
                figure=fig("think", 420, scale=0.8), props=[prop("bubble", 640, 460, size=130, enter="pop", delay=0.3)])),
            shot("Y alrededor del 30 % terminó formando un recuerdo falso.", stage(
                counters=[{"from": 0, "to": 30, "suffix": "%", "x": 540, "y": 580, "size": 160, "seconds": 1.0, "accent": "reward"}],
                texts=[text("formó un recuerdo falso", y=740, family="sans", size=44)])),
        ]),
        scene("G", "action", [
            shot("Así que, cuando discutas sobre cómo pasó algo, recuerda: estar seguro no prueba que tengas razón.", stage(
                figure=fig("point", 400), extras=[fig("point", 680, facing=-1, opacity=0.9)], props=[prop("bubble", 540, 440, size=100, enter="pop")])),
            shot("Si importa, busca registros: mensajes, fotos, notas.", stage(
                props=[prop("phone", 380, 620, size=120, enter="pop"), prop("book", 700, 620, size=120, enter="pop", delay=0.4, mark="check", markAt=0.6)])),
        ]),
        scene("H", "closer", [
            closer("Tu memoria no es un archivo. Es una historia que vuelves a contar.", ["historia"], "Loftus y Palmer, 1974 · Scoboria et al., 2017",
                   "Tu memoria no es un archivo. Es una historia que vuelves a contar…"),
            shot("y a veces, a escribir.", stage(props=[prop("book", 540, 620, size=180, state="open", enter="draw", accent="reward")])),
        ]),
        CTA("¿Alguna vez descubriste que un recuerdo tuyo no era como creías?", "Cuéntamelo en los comentarios.", "Cuéntamelo"),
    ],
    "Puedes recordar con detalle algo que nunca te pasó 🧠 Casi un tercio de las personas lo hizo en estos estudios.",
    ["#psicologia", "#memoria", "#cerebro", "#ciencia", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 018 frequency illusion
v18 = sb(
    "018-ilusion-frecuencia", "La ilusión de frecuencia: por qué ahora lo ves en todas partes", 1,
    [
        {"citation": "Zwicky, A. (2006). Why are we so illuded? Language Log (origen del término «frequency illusion»); resumen.",
         "url": "https://en.wikipedia.org/wiki/Frequency_illusion", "supports": "El término ilusión de frecuencia, popularizado por Arnold Zwicky."},
        {"citation": "Simons, D. J., & Chabris, C. F. (1999). Gorillas in our midst: Sustained inattentional blindness for dynamic events. Perception, 28(9), 1059–1074.",
         "doi": "10.1068/p281059", "supports": "Cerca de la mitad no vio a la persona disfrazada de gorila mientras contaba pases."},
    ],
    [
        scene("A", "hook", [
            shot("Aprendes una palabra nueva y, de pronto, está en todas partes.", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("lookUp", 540, path="flat"),
                props=[prop("bubble", 340, 460, size=90, enter="pop", delay=0.4), prop("bubble", 740, 420, size=90, enter="pop", delay=0.8), prop("bubble", 560, 340, size=80, enter="pop", delay=1.2)],
                camera=cam(1.0, 1.06)), "impact"),
            shot("No es una señal.", stage(
                figure=fig("stand", 540), texts=[text("No es una señal", emphasis=["No"])])),
        ]),
        scene("B", "question", [
            shot("¿Por qué algo que nunca veías, de repente aparece en todos lados?", stage(
                figure=fig("think", 540, path="flat"), props=[prop("question", 720, 460, size=80, enter="pop", delay=0.4)])),
        ]),
        scene("C", "mechanism", [
            shot("Se llama ilusión de frecuencia. El lingüista Arnold Zwicky le puso nombre.", {"type": "kineticTitle", "kicker": "Se llama", "lines": ["Ilusión de", "frecuencia"], "emphasis": ["frecuencia"]}, "impact"),
            shot("No es que aparezca más. Es que ahora lo notas.", stage(
                figure=fig("lookUp", 540), props=[prop("lightbulb", 540, 420, size=100, state="glow", enter="pop")])),
        ]),
        scene("D", "demonstration", [
            shot("Tu atención funciona como un foco:", stage(
                spotlight={"x": 400}, figure=fig("stand", 400), extras=[fig("stand", 760, facing=-1, opacity=0.25)])),
            shot("ilumina lo que le parece importante y deja todo lo demás a oscuras.", stage(
                spotlight={"x": 760}, figure=fig("stand", 400, opacity=0.25), extras=[fig("stand", 760, facing=-1, opacity=1)])),
        ]),
        scene("E", "retention", [
            shot("¿Y qué tan oscuro es ese «todo lo demás»?", stage(
                props=[prop("question", 540, 560, size=110, enter="pop")], camera=cam(1.0, 1.1))),
        ]),
        scene("F", "reveal", [
            shot("En un experimento famoso, unas personas contaban pases de pelota en un video.", stage(
                extras=crowd([300, 420, 660, 780], pose="reach", opacity=0.7, scale=0.8), props=[prop("donut", 540, 520, size=50, enter="pop")])),
            shot("A mitad de la escena, cruzaba alguien disfrazado de gorila.", stage(
                extras=crowd([300, 780], pose="reach", opacity=0.5, scale=0.8) + [fig("walk", 200, toX=880, scale=0.95, opacity=0.9)])),
            shot("Cerca de la mitad no lo vio.", stage(
                counters=[{"from": 0, "to": 50, "suffix": "%", "x": 540, "y": 580, "size": 160, "seconds": 0.9, "accent": "reward"}],
                texts=[text("no lo vio", y=740, family="sans", size=48)])),
        ]),
        scene("G", "action", [
            shot("Y cuando por fin lo notas, cada nueva aparición se siente como una prueba.", stage(
                props=[prop("bubble", 380, 560, size=100, enter="pop", mark="check", markAt=0.3), prop("bubble", 700, 560, size=100, enter="pop", delay=0.6, mark="check", markAt=0.7)])),
            shot("Así que elige con cuidado qué quieres notar.", stage(
                spotlight={"x": 540}, figure=fig("walk", 340, toX=540, path="rise"))),
        ]),
        scene("H", "closer", [closer("El mundo no cambió. Cambió lo que decides ver.", ["ver"], "Simons y Chabris, 1999",
                                      "El mundo no cambió. Cambió lo que decides ver.")]),
        CTA("¿Qué empezaste a ver en todos lados después de descubrirlo?", "Cuéntame en los comentarios.", "Cuéntame"),
    ],
    "Aprendes algo nuevo y de pronto lo ves en todas partes 👀 No es una señal: es tu atención. Y el experimento del gorila lo demuestra.",
    ["#psicologia", "#atencion", "#cerebro", "#curiosidades", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 020 self-fulfilling prophecy
v20 = sb(
    "020-profecia-autocumplida", "La profecía autocumplida: lo que esperas de alguien puede cambiarlo", 5,
    [
        {"citation": "Rosenthal, R., & Jacobson, L. (1968). Pygmalion in the classroom. The Urban Review, 3(1), 16–20.",
         "doi": "10.1007/BF02322211", "supports": "Profesores informados de que ciertos alumnos (elegidos al azar) «florecerían»: algunos mejoraron más."},
        {"citation": "Jussim, L., & Harber, K. D. (2005). Teacher expectations and self-fulfilling prophecies: Knowns and unknowns, resolved and unresolved controversies. Personality and Social Psychology Review, 9(2), 131–155.",
         "doi": "10.1207/s15327957pspr0902_3", "supports": "Revisión: las expectativas influyen, pero el efecto suele ser pequeño; muchas expectativas son acertadas."},
    ],
    [
        scene("A", "hook", [
            shot("La forma en que tratas a alguien puede terminar cambiando en quién se convierte.", stage(
                spotlight={"x": 640, "snap": True}, figure=fig("point", 400, path="flat"), extras=[fig("walk", 640, toX=720, facing=1, scale=0.8, opacity=0.9)],
                camera=cam(1.0, 1.06)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿De verdad creer en alguien lo vuelve mejor?", stage(
                figure=fig("stand", 400), extras=[fig("stand", 680, facing=-1, scale=0.8, opacity=0.9)], props=[prop("question", 540, 440, size=80, enter="pop", delay=0.4)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1968, a unos profesores les dijeron que ciertos alumnos iban a florecer este año.", stage(
                figure=fig("point", 360), extras=crowd([580, 700, 820], opacity=0.7, scale=0.65), props=[prop("lightbulb", 700, 420, size=80, state="glow", enter="pop", delay=0.6)])),
            shot("En realidad, los habían elegido al azar.", stage(
                props=[prop("dice", 540, 620, size=150, state="spin", enter="pop", label="3")], texts=[text("Al azar", emphasis=["azar"])])),
            shot("Meses después, algunos de esos alumnos mejoraron más que el resto.", stage(
                extras=[fig("walk", 380, toX=560, scale=0.7, opacity=1, path="rise")] + crowd([760, 880], opacity=0.4, scale=0.65))),
            shot("Se hizo famoso como el efecto Pigmalión.", {"type": "kineticTitle", "kicker": "El efecto", "lines": ["Pigmalión"], "emphasis": ["Pigmalión"]}, "impact"),
        ]),
        scene("D", "retention", [
            shot("Y la historia se contó como si fuera magia: cree en alguien y lo transformarás.", stage(
                figure=fig("reach", 400), extras=[fig("stand", 680, facing=-1, scale=0.8)], props=[prop("lightbulb", 540, 420, size=120, state="glow", enter="pop")])),
        ]),
        scene("E", "reveal", [
            shot("Pero una revisión de décadas de estudios encontró que sí influye…", stage(
                props=[prop("chart", 540, 620, size=200, state="up", enter="draw", mark="check", markAt=0.5)])),
            shot("aunque el efecto suele ser pequeño.", stage(
                props=[prop("chart", 540, 620, size=200, state="up", enter="none", to={"state": "normal", "at": 0.3})], texts=[text("Pequeño", emphasis=["Pequeño"])], camera=cam(1.0, 1.1))),
            shot("Y muchas veces, lo que espera el profesor acierta porque se basa en información real.", stage(
                figure=fig("think", 400), props=[prop("book", 700, 600, size=130, enter="pop", mark="check", markAt=0.6)])),
        ]),
        scene("F", "demonstration", [
            shot("Cuando funciona, no es magia. Es el trato: más atención, más oportunidades, más respuestas.", stage(
                figure=fig("reach", 360), extras=[fig("walk", 560, toX=720, scale=0.8, opacity=1, path="rise")],
                props=[prop("bubble", 460, 460, size=90, enter="pop", delay=0.3), prop("checklist", 860, 520, size=100, state="open", enter="pop", delay=0.9, accent="reward")])),
        ]),
        scene("G", "action", [
            shot("Si esperas algo de alguien, dale las condiciones para lograrlo.", stage(
                figure=fig("point", 380), extras=[fig("walk", 600, toX=760, scale=0.85, path="flat")])),
            shot("Y contigo igual: no basta con creer. Diseña tu entorno.", stage(
                figure=fig("walk", 300, toX=520, path="rise"), props=[prop("door", 780, 600, size=150, state="open", enter="draw")])),
        ]),
        scene("H", "closer", [closer("Creer en alguien no es magia. Es darle oportunidades.", ["oportunidades"], "Rosenthal y Jacobson, 1968 · Jussim y Harber, 2005",
                                      "Creer en alguien no es magia. Es darle oportunidades.")]),
        CTA("¿Alguien creyó en ti cuando tú no lo hacías?", "Cuéntamelo en los comentarios.", "Cuéntamelo"),
    ],
    "Lo que esperas de alguien puede cambiar en quién se convierte 🌱 Pero no funciona como en el mito: funciona a través del trato.",
    ["#psicologia", "#educacion", "#crecimientopersonal", "#liderazgo", "#aprendeentiktok"],
)

# ------------------------------------------------------------------ 021 cognitive dissonance (myth vs evidence)
v21 = sb(
    "021-disonancia-cognitiva", "La disonancia cognitiva: ¿justificamos lo que hicimos?", 5,
    [
        {"citation": "Festinger, L., & Carlsmith, J. M. (1959). Cognitive consequences of forced compliance. Journal of Abnormal and Social Psychology, 58(2), 203–210.",
         "doi": "10.1037/h0041593", "supports": "Pagar 1 dólar vs 20 por decir que una tarea aburrida era divertida: los de 1 dólar la valoraron mejor."},
        {"citation": "Vaidis, D. C., et al. (2024). A multilab replication of the induced-compliance paradigm of cognitive dissonance. Advances in Methods and Practices in Psychological Science, 7(1).",
         "doi": "10.1177/25152459231213375", "supports": "Réplica multilaboratorio: no se encontró el cambio de actitud esperado en el paradigma de acatamiento inducido."},
    ],
    [
        scene("A", "hook", [
            shot("¿Alguna vez defendiste una decisión que sabías que estaba mal, solo porque ya la habías tomado?", stage(
                spotlight={"x": 540, "snap": True}, figure=fig("point", 540, path="fork"),
                props=[prop("bubble", 700, 440, size=100, enter="none", mark="cross", markAt=0.7)], camera=cam(1.0, 1.06)), "impact"),
        ]),
        scene("B", "question", [
            shot("¿Cambiamos lo que pensamos para justificar lo que hicimos?", stage(
                props=[prop("balance", 540, 700, size=230, state="normal", enter="pop"), prop("question", 540, 440, size=80, enter="pop", delay=0.4)])),
        ]),
        scene("C", "mechanism", [
            shot("En 1959, Festinger y Carlsmith pagaron a personas para decir que una tarea aburrida era divertida.", stage(
                figure=fig("stand", 380), props=[prop("checklist", 700, 600, size=140, state="closed", enter="pop")], texts=[text("Festinger · 1959", family="sans", size=46)])),
            shot("A unos les dieron un dólar. A otros, veinte.", stage(
                counters=[{"from": 0, "to": 1, "prefix": "$", "x": 360, "y": 600, "size": 130, "seconds": 0.4}, {"from": 0, "to": 20, "prefix": "$", "x": 720, "y": 600, "size": 130, "seconds": 0.6, "delay": 0.5}])),
            shot("Y los del dólar terminaron diciendo que la tarea les había gustado más.", stage(
                props=[prop("balance", 540, 720, size=220, enter="none", to={"state": "down", "at": 0.3})],
                texts=[text("$1", x=420, y=560, family="sans", size=44), text("$20", x=660, y=560, family="sans", size=44)])),
            shot("La idea: sin una buena excusa, cambias tu opinión para sentirte coherente.", {"type": "kineticTitle", "kicker": "Disonancia", "lines": ["Cambias de opinión", "para ser coherente"], "emphasis": ["coherente"]}, "impact"),
        ]),
        scene("D", "retention", [
            shot("Se volvió uno de los pilares de la psicología social.", stage(
                props=[prop("book", 540, 620, size=180, enter="draw", state="glow")], camera=cam(1.0, 1.06))),
        ]),
        scene("E", "reveal", [
            shot("Pero en 2024, decenas de laboratorios en varios países intentaron repetirlo…", stage(
                extras=crowd([200, 330, 460, 620, 750, 880], pose="think", opacity=0.55, scale=0.65))),
            shot("y no encontraron el cambio de opinión esperado.", stage(
                props=[prop("chart", 540, 620, size=200, state="normal", enter="draw", mark="cross", markAt=0.5)], texts=[text("No se repitió", emphasis=["No"])], camera=cam(1.0, 1.1))),
            shot("La teoría sigue en debate. Lo que se tambalea es su prueba más famosa.", stage(
                props=[prop("book", 540, 620, size=170, state="dim", enter="pop")], texts=[text("Sigue en debate", family="sans", size=52)])),
        ]),
        scene("F", "demonstration", [
            shot("Eso no significa que nunca te justifiques. Significa que la ciencia corrige sus propias historias.", stage(
                figure=fig("walk", 300, toX=520, path="rise"), props=[prop("checklist", 780, 580, size=130, state="open", enter="pop", delay=0.6, accent="reward")])),
        ]),
        scene("G", "action", [
            shot("Así que, cuando te descubras defendiendo algo solo porque ya lo hiciste,", stage(
                figure=fig("point", 540, path="fork"))),
            shot("pregúntate: ¿lo elegiría otra vez hoy, sabiendo lo que sé?", stage(
                figure=fig("think", 540, path="fork"), texts=[text("¿Lo elegiría otra vez?", family="sans", size=52)])),
        ]),
        scene("H", "closer", [closer("Ser coherente no es nunca cambiar. Es estar dispuesto a revisar.", ["revisar"], "Festinger y Carlsmith, 1959 · Vaidis et al., 2024",
                                      "Ser coherente no es nunca cambiar. Es estar dispuesto a revisar.")]),
        CTA("¿Qué «verdad» de la psicología te gustaría que pusiéramos a prueba?", "Cuéntamelo en los comentarios.", "Cuéntamelo"),
    ],
    "¿Justificas decisiones solo porque ya las tomaste? 🤔 El experimento más famoso sobre esto acaba de fallar en una gran réplica.",
    ["#psicologia", "#mitos", "#decisiones", "#ciencia", "#aprendeentiktok"],
)

write(v13, v15, v17, v18, v20, v21)
