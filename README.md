# mente-studio

Estudio automatizado de motion graphics de psicología en español (1080×1920, 9:16).

**Un storyboard JSON entra → un video terminado, verificado y empaquetado sale.**

```
storyboards/<id>.json ──► validate ──► voice ──► captions ──► timeline ──► Remotion render ──► master + QC ──► release
        (Claude)          (gate)     (TTS)    (Whisper)     (props)      (3D + 2D scenes)     (-14 LUFS)     (privado)
```

## Cómo se usa

| Quiero… | Hago… |
|---|---|
| Producir un video | Subir `storyboards/<id>.json` a `main`. El workflow **Produce videos** corre solo. |
| Re-renderizar con otra voz | Actions › Produce videos › Run workflow › elegir `engine`. |
| Comparar voces | Actions › Voice A/B test › Run workflow. Las muestras quedan en *Releases*. |
| Ver un video terminado | *Releases* → `[PASS] <id>`: mp4, miniatura, caption, fuentes, informe QC. |
| Probar localmente | `npm ci && pip install -r requirements.txt && bash pipeline/produce.sh storyboards/001-placer-inmediato.json kokoro` |
| Editar visualmente | `npm run studio` |

## Estructura

```
src/
  schema.ts            contrato Storyboard → Timeline (zod)
  design/tokens.ts     colores, tipografía, zonas seguras, curvas de movimiento
  scenes/              escenas reutilizables (Brain3D, DiscountCurve, BehaviorLoop, …)
  components/          fondo, captions, transiciones, texto cinético
pipeline/
  validate.ts          control editorial (estructura, duración, fuentes)
  voice.py             kokoro | piper | elevenlabs | estimate
  captions.py          marcas de tiempo por palabra (faster-whisper) alineadas al guion
  sfx.py               sonido y música 100 % procedurales (sin licencias)
  timeline.ts          storyboard + tiempos de voz → props de render
  finish.py            codificación final, loudness, QC, paquete de entrega
  produce.sh           orquesta todo
storyboards/           un JSON por video (lo escribe Claude)
.github/workflows/     produce.yml, voice-test.yml
```

## Escenas disponibles

`kineticTitle` · `brain3d` (cerebro 3D procedural, regiones: prefrontal, reward, amygdala, hippocampus) · `neuralNetwork` (firing / strengthening / organizing) · `twoForces` (task / reward / future / now) · `discountCurve` · `behaviorLoop` · `emotionWave` · `actionSteps` · `closer`

## Reglas de seguridad

- Ninguna clave en el código. `ELEVENLABS_API_KEY` vive solo como *GitHub Secret* y solo se expone al paso de voz.
- Nada se publica en redes automáticamente: los videos quedan como *pre-release* privados para aprobación.
- Todo video lleva la etiqueta de contenido generado por IA al publicarse (ver `qc.json › publishChecklist`).

## Control de calidad automático

Dimensiones, fps, códec y rango de color, pista de audio, duración, loudness (-14 LUFS), segmentos negros, imagen congelada, cobertura de subtítulos, tamaño de archivo y DOIs de las fuentes. Un fallo bloqueante marca el release como `[FAIL]`.
