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
- Uso puntual de colores como verde, rojo y dorado para destacar información.
- Animaciones fluidas, movimientos de cámara y transiciones profesionales.

**Prohibido:** diapositivas, imágenes estáticas con subtítulos y recopilaciones de vídeos de stock.
**Obligatorio:** motion graphics reales que expliquen visualmente la narración. Cada escena debe mostrar el concepto que se está narrando.

### Identidad cinematográfica obligatoria (regla absoluta, desde 2026-11-25)

Se mantiene en todos los vídeos salvo que el propietario pida explícitamente un cambio.

- **Fondo SIEMPRE negro profundo `#000000`** (`COLORS.bg`). Nunca gris, azul ni entornos de color; nada de degradados tintados.
- En el fondo solo se permiten detalles discretos y secundarios: pequeños puntos o partículas blancas, una textura fina (grano ≤ 0,03). Nunca deben cargar la imagen.
- El blanco es el color principal de gráficos y contrastes; verde, rojo y dorado solo como acento puntual.
- Estética premium, minimalista, cinematográfica y psicológica. Contraste fuerte entre personaje, gráficos y negro.

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

### Sistema de storytelling y retención (obligatorio en cada vídeo)

Inspirado en las técnicas de retención de los grandes creadores de YouTube; sin copiar su contenido ni su marca.

1. **Hook** extremadamente atractivo en los primeros segundos (beat `hook`, legible en el fotograma 0).
2. **Pregunta psicológica** que abre un vacío de curiosidad (beat `question` en la escena 2 o 3).
3. **Progresión narrativa**: cada escena aporta información nueva (`mechanism`, `demonstration`, `retention` con giros y bucles abiertos).
4. **Metáforas visuales y animaciones** que hacen visibles las ideas (puertas, caminos, balanzas, relojes…).
5. **Revelación psicológica inesperada** (beat `reveal`, obligatoria, en la segunda mitad del vídeo y siempre respaldada por una fuente).
6. **Conclusión memorable** (beat `closer`), luego CTA natural (beat `cta`).

Nada de vídeos genéricos: cada escena tiene una función narrativa declarada en su `beat`. `pipeline/validate.ts` bloquea el render si falta el hook, la pregunta, la revelación, el cierre o el CTA.

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
- **Música:** «intimo» (pad cálido, piano agudo espaciado, cuerdas graves; Mi menor, 66 bpm), generada por `pipeline/music.py`. Campo `"music": "intimo"` en cada storyboard.
- El propietario no descarga ni instala archivos: Claude entrega siempre el vídeo final ya montado con voz, música y efectos.
- No descargar ni republicar vídeos de otros creadores. Los vídeos virales solo se usan como referencia de estructura.

## REGLAS EDITORIALES (acordadas en la Etapa A)

- Rigor: cada afirmación central se apoya en una revisión, metaanálisis o estudio replicado, con la cita completa (DOI o URL) en `sources` del storyboard.
- No inventar estadísticas, estudios ni citas. Si no hay cifra verificada, no hay cifra.
- Lo especulativo o debatido se presenta como tal; los temas no replicados solo en formato «mito vs. evidencia».
- Sin autodiagnóstico, autolesiones ni trastornos usados como gancho.
- Voz del narrador: español latinoamericano neutro, natural, cercano y profesional, sin acento regional marcado.
- Todo vídeo se publica con la etiqueta de contenido generado por IA.
- Nunca publicar automáticamente: todo vídeo queda para aprobación humana.

## REGLAS TÉCNICAS

- Motor: Remotion (React) + @remotion/three. Render en GitHub Actions (repo privado).
- Un vídeo = un archivo `storyboards/<id>.json` validado por `src/schema.ts`. Ejecutar `npx tsx pipeline/validate.ts` antes de producir.
- Pipeline: `bash pipeline/produce.sh storyboards/<id>.json <engine>` (validate → voice → captions → timeline → render → finish/QC).
- Diseño: colores, tipografía, zonas seguras y curvas de movimiento solo desde `src/design/tokens.ts`. Zonas seguras de TikTok/Reels: arriba 170 px, abajo 360 px, izquierda 72 px, derecha 150 px.
- Las animaciones se controlan solo con `useCurrentFrame()` (nada de animaciones CSS ni `useFrame` de three.js); todo aleatorio con semilla fija.
- El primer fotograma del hook debe ser legible (sin fundido de entrada en la primera escena).
- Sonido 100 % procedural (`pipeline/sfx.py`); sin música ni efectos con licencia de terceros.
- Credenciales solo como GitHub Secrets o variables de entorno. Nunca en código, logs ni commits.
- No activar servicios ni suscripciones de pago sin aprobación del propietario.
- QC bloqueante en `pipeline/finish.py`: 1080×1920, 30 fps, H.264 yuv420p, audio a −14 LUFS, sin negros ni congelados, todas las palabras subtituladas.
