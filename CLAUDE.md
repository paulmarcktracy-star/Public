# CLAUDE.md — mente-studio

Reglas permanentes del proyecto. Consultar este archivo **antes de crear cada vídeo**.
Si el propietario modifica una regla, actualizar este archivo en el mismo cambio.

---

## IDENTIDAD VISUAL Y ESTILO DE PRODUCCIÓN

### Referencia visual principal

La primera referencia de vídeo del propietario define el estilo gráfico:

- Fondo negro profundo `#000000` (ver «Identidad cinematográfica obligatoria»).
- Personajes minimalistas blancos, tipo figuras humanas sencillas.
- Ilustraciones de líneas blancas y elementos geométricos.
- Focos de luz y efectos de iluminación cinematográficos.
- Objetos animados que representan conceptos: dinero, puertas, relojes, gráficos, pantallas, cerebros, etc.
- Textos y cifras que aparecen animados.
- Paleta exclusivamente blanco y negro (ver «Identidad blanco y negro»).
- Animaciones fluidas, movimientos de cámara y transiciones profesionales.

**Prohibido:** diapositivas, imágenes estáticas con subtítulos y recopilaciones de vídeos de stock.
**Obligatorio:** motion graphics reales que expliquen visualmente la narración. Cada escena debe mostrar el concepto que se está narrando.

### Identidad blanco y negro (regla absoluta, desde 2026-11-25; reemplaza la paleta con dorado/verde/rojo)

Se mantiene en todos los vídeos salvo que el propietario pida explícitamente un cambio.

- **Solo dos colores:** negro profundo `#000000` y blanco puro `#FFFFFF`. Personajes, motion graphics, gráficos, tipografía y transiciones respetan esta paleta (los grises son blanco con opacidad).
- Prohibido: azul, violeta, rojo, degradados de color y cualquier color añadido solo para decorar.
- **Excepción:** un único color extra (`accent: "reward"`, `COLORS.reward`) solo cuando tiene una función narrativa real (recompensa, victoria, momento emocional clave). Raro e intencional: `validate.ts` bloquea más de 2 planos con `reward`.
- Los antiguos acentos `gold`/`green` se dibujan en blanco y `red` en gris atenuado (pérdida, error).
- Estética premium, minimalista, cinematográfica y psicológica. Contraste fuerte entre personaje, gráficos y negro.

#### Fondo: cuadrícula de puntos estática

- Fondo casi negro `#050505` (`COLORS.bgGrid`) con una cuadrícula regular de puntos grises diminutos (~1,3 px, opacidad 20 %, separación 36 px idéntica en horizontal y vertical).
- Generada solo con CSS `radial-gradient()` + `background-size` (`src/components/Background.tsx`). Sin elementos individuales ni JavaScript.
- **Totalmente estática:** nunca se mueve, anima, pulsa ni cambia de posición. Es una capa independiente debajo de todas las escenas; los movimientos de cámara y las transiciones ocurren encima y no la afectan.
- Sin partículas animadas ni grano animado en el fondo.

#### Firma gráfica: el camino discontinuo

- Cuando un personaje camina, camina **sobre** un camino hecho de muchos trazos blancos cortos, finos y separados a intervalos regulares (— — — —). Nunca flota en el vacío negro.
- El camino puede extenderse delante, prolongarse detrás, unir dos puntos y transformarse según el tema psicológico. La parte ya recorrida es más tenue y la que queda por delante es más brillante.
- Implementación: `figure.path` en el storyboard (`src/scenes/Stage.tsx`, componente `DashedPath`):
  - `auto`/`flat`: recto.
  - `rise`: sube (progreso, acercarse a una meta).
  - `fall`: baja (recaída, pérdida).
  - `fork`: se bifurca (decisión, elección).
  - `fade`: se desvanece por delante (futuro incierto, lo que no vemos).
  - `none`.
  - `pathFrom`/`pathTo` fijan los extremos. El personaje sigue la altura del camino.

#### Animación

- Personajes con movimiento natural, cámara cinematográfica fluida, motion graphics sincronizados con la narración, transiciones limpias, partículas blancas discretas.
- Objetivo: personajes 3D que caminan. El motor actual usa figuras blancas 2D con cinemática; la migración a un personaje 3D procedural es el siguiente paso técnico y debe respetar este mismo lenguaje (blanco, minimalista, camino discontinuo).

### Cámara cinematográfica inteligente (propietario, 2026-11-25; vídeos producidos desde entonces)

Implementada en `src/camera/Camera.tsx` (`planCamera` + `CameraRig`), aplicada a toda la capa de escenas; la cuadrícula de puntos y los subtítulos nunca se mueven.

- **Apertura:** el vídeo empieza en primer plano (110 %), mantiene el primer plano durante el hook y, al terminar el hook, retrocede suavemente al 100 % (curva cinematográfica, nunca lineal).
- **Zoom inteligente por jerarquía visual:** en cada plano la cámara elige el elemento más importante (cifra > elemento `reward` > objeto con marca o transformación > personaje que camina > texto con énfasis) y se acerca a él justo cuando aparece (103–112 %; la revelación llega a ~110–111 %).
- **Variedad:** push-in, pull-out, travelling que sigue al personaje, focus, paneos lentos; nunca el mismo movimiento dos veces seguidas. El título cinético hace un push-in lento; el cierre, un push-in deliberado; el CTA vuelve a 100 %.
- **Transiciones:** en cada cambio de plano la cámara vuelve suavemente a un encuadre tranquilo; cada movimiento empieza exactamente donde terminó el anterior (sin saltos).
- **Seguridad de encuadre:** zoom alrededor del centro de contenido (540, 760), recentrado parcial y limitado (±70 px / ±46 px) para que nada importante se corte ni entre en las zonas inseguras. Si el plano ya tiene un zoom interno fuerte, la cámara global se modera.
- Los vídeos hechos antes de esta regla (1, 2, 4, 12, 19) llevan `"cameraStyle": "classic"` y se publican tal cual.

### Sistema de storytelling y retención (obligatorio en cada vídeo)

Inspirado en las técnicas de retención de los grandes creadores de YouTube; sin copiar su contenido ni su marca.

1. **Hook** extremadamente atractivo en los primeros segundos (beat `hook`, legible en el fotograma 0).
2. **Pregunta psicológica** que abre un vacío de curiosidad (beat `question` en la escena 2 o 3).
3. **Progresión narrativa**: cada escena aporta información nueva (`mechanism`, `demonstration`, `retention` con giros y bucles abiertos).
4. **Metáforas visuales y animaciones** que hacen visibles las ideas (puertas, caminos, balanzas, relojes…).
5. **Revelación psicológica inesperada** (beat `reveal`, obligatoria, en la segunda mitad del vídeo y siempre respaldada por una fuente).
6. **Conclusión memorable** (beat `closer`), luego CTA natural (beat `cta`).

**Reglas de implementación del hook (propietario, 2026-11-25):**

- Cuando el propietario da un hook, se usa EXACTAMENTE como primera frase. No se cambia sin una razón editorial concreta, y en ese caso se le consulta antes. Hooks aprobados: `plan/hooks-mes-1.md`.
- El hook aparece desde el primer segundo, sin presentación, saludo ni introducción. La voz empieza de inmediato, en el fotograma 0.
- La primera escena visual representa exactamente lo que dice la frase del hook.
- No se divide el hook en varias frases antes de presentar la idea principal: es la primera escena (beat `hook`), en una sola toma de voz.
- Hook corto, natural y fácil de entender.

Nada de vídeos genéricos: cada escena tiene una función narrativa declarada en su `beat`. `pipeline/validate.ts` bloquea el render si falta el hook, la pregunta, la revelación, el cierre o el CTA.

### Sound design premium (prioridad absoluta)

Nunca un vídeo con solo música de fondo + narración. Cada detalle visual puede llevar su efecto sonoro, y cada sonido tiene una razón para existir:

- Personaje que camina: pasos reales, sincronizados con cada contacto del pie.
- Pequeño elemento gráfico que aparece: pop sutil o soft click.
- Línea blanca que se dibuja: sonido ligero de trazo.
- Objeto que se desplaza: SFX fluido y preciso.
- Texto que aparece: micro-sonido discreto.
- Transición: whoosh cinematográfico suave.
- Animación 3D: sonidos sutiles adaptados al movimiento.
- Revelación importante (`reveal`): diseño sonoro que acentúa el impacto.
- Recompensa final: sonido distintivo y satisfactorio.

SFX profesionales, suaves, sutiles y perfectamente sincronizados al fotograma. Nunca agresivos, repetitivos, artificiales ni excesivos.

**Implementación:** `pipeline/mix.py` deriva cada sonido de los mismos tiempos que las animaciones (`Stage.tsx`): pasos en cada contacto del pie (también de los personajes secundarios, más lejanos), pop/thud en apariciones, trazo de lápiz en caminos y líneas dibujadas, swish en desplazamientos, click en textos, ticks en contadores, whoosh suave solo en cambios de escena, golpe suave en el fotograma 0, subida + impacto en la revelación y campanilla cálida en cada elemento `reward`. Capa de textura (room tone a −54 dB). Semilla fija: mismo storyboard, mismo sonido.

### Mezcla de audio profesional

- La narración domina y es perfectamente inteligible: ducking por sidechain de la voz (música ≈ −6 dB y SFX ≈ −3,7 dB mientras habla; vuelven en las pausas). Implementado en `pipeline/mix.py`.
- La música sostiene la emoción sin competir con la voz.
- Los SFX son limpios, sincronizados, equilibrados en volumen y adaptados a cada escena, sin saturación (true peak ≤ −1 dBTP) ni ruidos inútiles.
- Capas cuando mejoran la inmersión: ambiente, textura, movimiento e impacto.

### Calidad de montaje y experiencia del espectador

- Montaje extremadamente cuidado: animaciones fluidas, timing preciso, transiciones elegantes, tipografía perfectamente colocada, cámara natural, ritmo dinámico pero nunca desordenado.
- Sincronización perfecta entre narración, imagen, animación y sonido.
- Nada de animaciones solo para llenar la pantalla.
- Cada escena crea una emoción, transmite información o refuerza la curiosidad. Debe sentirse como una producción profesional, no como un vídeo IA genérico.
- La recompensa narrativa final va acompañada de un momento audiovisual satisfactorio.
- Objetivo: minidocumentales psicológicos cinematográficos, con identidad blanco y negro reconocible, sound design premium y montaje de estudio.

### Control de calidad final (obligatorio antes de entregar)

1. Respeto de la identidad blanco y negro.
2. Coherencia de personajes y escenas.
3. Calidad y fluidez de las animaciones.
4. Sincronización de los micro-SFX.
5. Calidad de la mezcla de audio.
6. Ritmo y retención narrativa.
7. Calidad de transiciones y detalles.
8. Impacto de la revelación final.

Si algo parece amateur, se mejora antes de la entrega.

### Minimalismo y encuadre 9:16

- Imágenes y textos discretos: ningún elemento debe ocupar toda la pantalla. Mucho espacio negativo.
- Todo se dibuja dentro de la zona de contenido, escalado al 84 % (`SCALE.visual` en `src/design/tokens.ts`).
- Tamaños máximos: títulos ~62 px (`SCALE.text`), subtítulos 48 px, etiquetas de objetos 32 px.
- Respetar las zonas seguras de TikTok, Reels y Shorts: nada importante en los 170 px superiores, los 360 px inferiores ni los 150 px de la derecha.
- Ante la duda, más pequeño y más limpio.

### Referencia narrativa

La segunda referencia define la estructura para captar y mantener la atención:

1. **HOOK:** captar la atención desde los primeros segundos.
2. **RETENCIÓN:** mantener la curiosidad mediante cambios visuales, preguntas, información progresiva y elementos que hagan querer descubrir lo siguiente.
3. **CTA:** terminar con una llamada a la acción natural que invite a comentar o interactuar.

### Identidad del contenido

- **Nicho:** psicología humana: cerebro, comportamiento, disciplina, emociones, relaciones, dinero y transformación personal.
- **Público:** jóvenes hispanohablantes de aproximadamente 18 a 35 años.
- **Idioma:** español latinoamericano neutro.
- **Formato principal:** vertical 9:16, resolución 1080 × 1920.

Estas referencias son la identidad visual y narrativa permanente del proyecto.

### Reglas obligatorias de producción

1. Cada parte de la narración debe tener una representación visual relacionada con lo que se está diciendo.
2. No mantener una escena estática durante demasiado tiempo. En la práctica: un plano (shot) por frase, de 2 a 5 s, siempre con movimiento (cámara, personaje, objeto o texto).
3. Usar animaciones de personajes, objetos, gráficos, textos, números y elementos visuales.
4. Mantener una identidad visual coherente con las referencias.
5. Construir una historia con principio, desarrollo y conclusión.
6. El hook debe despertar curiosidad inmediatamente, legible desde el primer fotograma.
7. La retención se construye durante todo el vídeo, no solo al principio (preguntas, giros, información progresiva, cambios visuales).
8. El CTA debe ser natural y relacionado con el tema.
9. Evitar información inventada, afirmaciones psicológicas sin fundamento y estadísticas falsas.
10. Priorizar calidad visual y narrativa sobre producir vídeos rápidamente.

### Antes de renderizar (obligatorio)

Preparar y dejar por escrito:

- El título y el concepto.
- El hook.
- El guion completo.
- La estructura narrativa.
- La descripción de las escenas y animaciones.
- La estrategia de retención.
- El CTA.

Después verificar que todo respeta estas reglas y que la infraestructura existente puede producirlo. Solo entonces renderizar.

### Restricciones permanentes

- No activar servicios de pago, no comprar suscripciones y no publicar nada sin autorización del propietario.
- Si hace falta una cuenta, una clave o un permiso, explicar exactamente qué debe hacer el propietario.

---

## VOZ Y MÚSICA (elegidas por el propietario, usar en todos los vídeos)

- **Voz:** n.º 10 del catálogo, mujer, mezcla Kokoro `ef_dora+af_heart`, velocidad 0.9. Variable `KOKORO_VOICE=ef_dora+af_heart`. Ver `VOICES.md`.
- **Música (decisión del propietario, 2026-11-25):** «Meaningful Love – instrumental» (Silo, Steven Cranberry), tramo tranquilo y lento, en todos los vídeos. Campo `"music": "meaningful"`. El propietario asume el uso de esta canción comercial (riesgo informado: TikTok puede silenciar o limitar audio incrustado; primero se publica un vídeo de prueba). Se guarda cifrada en `assets/music/meaningful.flac.enc` (nunca en claro en el repo público); el workflow la descifra con el secreto `MUSIC_KEY`. Bucle con fundidos cruzados de 3 s, ducking bajo la voz como siempre. Excepción explícita a la regla de música 100 % procedural.
- El propietario no descarga ni instala archivos: Claude entrega siempre el vídeo final ya montado con voz, música y efectos.
- No descargar ni republicar vídeos de otros creadores. Los vídeos virales solo se usan como referencia de estructura.

## REGLAS EDITORIALES (acordadas en la Etapa A)

- Rigor: cada afirmación central se apoya en una revisión, metaanálisis o estudio replicado, con la cita completa (DOI o URL) en `sources` del storyboard.
- No inventar estadísticas, estudios ni citas. Si no hay cifra verificada, no hay cifra.
- Lo especulativo o debatido se presenta como tal; los temas no replicados solo en formato «mito vs. evidencia».
- Sin autodiagnóstico, autolesiones ni trastornos usados como gancho.
- Voz del narrador: español latinoamericano neutro, natural, cercano y profesional, sin acento regional marcado.
- **Español fluido y natural (propietario, 2026-11-25):** escribir como se habla, no como un paper. Frases cortas, conectores naturales («así que», «ojo», «una y otra vez»), «tú» cercano, nada de giros traducidos («subestimaban sistemáticamente», «evaluamos todo como»). Leer cada guion en voz alta antes de producir.
- Todo vídeo se publica con la etiqueta de contenido generado por IA.
- Nunca publicar automáticamente: todo vídeo queda para aprobación humana.

## REGLAS TÉCNICAS

- Motor: Remotion (React) + @remotion/three. Render en GitHub Actions (repo privado).
- Un vídeo = un archivo `storyboards/<id>.json` validado por `src/schema.ts`. Ejecutar `npx tsx pipeline/validate.ts` antes de producir.
- Pipeline: `bash pipeline/produce.sh storyboards/<id>.json <engine>` (validate → voice → captions → timeline → render → finish/QC).
- Diseño: colores, tipografía, zonas seguras y curvas de movimiento solo desde `src/design/tokens.ts`. Zonas seguras de TikTok/Reels: arriba 170 px, abajo 360 px, izquierda 72 px, derecha 150 px.
- Las animaciones se controlan solo con `useCurrentFrame()` (nada de animaciones CSS ni `useFrame` de three.js); todo aleatorio con semilla fija.
- El primer fotograma del hook debe ser legible (sin fundido de entrada en la primera escena).
- SFX 100 % procedurales (`pipeline/sfx.py`, `pipeline/mix.py`). Música: la elegida por el propietario (ver VOZ Y MÚSICA); ningún otro audio de terceros.
- Credenciales solo como GitHub Secrets o variables de entorno. Nunca en código, logs ni commits.
- No activar servicios ni suscripciones de pago sin aprobación del propietario.
- Calendario: los vídeos del mes se producen con TODAS estas reglas; no se producen vídeos fuera del plan sin pedido del propietario.
- QC bloqueante en `pipeline/finish.py`: 1080×1920, 30 fps, H.264 yuv420p, audio a −14 LUFS, sin negros ni congelados, todas las palabras subtituladas.
