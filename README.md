# Proyecto AED2: Puentes en grafos

Este proyecto es una animación explicativa sobre los puentes de un
grafo. Un puente es una arista cuya eliminación aumenta el número de
componentes conexas del grafo. La animación explica este concepto y muestra
cómo encontrarlos mediante un recorrido en profundidad (DFS) basado en el
algoritmo de Tarjan.

## Avances actuales

- Se implementó `find_bridges(n, edges)` para grafos no dirigidos.
- El algoritmo calcula los valores `tin` y `low`, registra una traza de
  eventos y funciona con grafos no conexos.
- Se contempló el caso de aristas paralelas usando un identificador por
  arista, en lugar de ignorar únicamente el vértice padre.
- Se agregaron siete pruebas unitarias: ejemplo de la guía, árbol, ciclo,
  aristas paralelas, grafo sin aristas, un solo nodo y grafo no conexo.
- Se desarrollaron y renderizaron las escenas 0 a 3 de la animación:
  portada, motivación, definición de puente y explicación de `tin`/`low`.
- La escena del algoritmo utiliza los valores reales producidos por
  `find_bridges`; los puentes y las componentes mostradas no están escritos
  manualmente en la animación.
- Se generó un video de avance en alta resolución, a 2560 × 1440 píxeles y
  30 fps, sin audio.

## Estructura del proyecto

| Carpeta | Contenido |
|---|---|
| `implementacion del codigo/` | Implementación del algoritmo y pruebas unitarias |
| `animaciones/` | Código de Manim, configuración y archivos generados durante el renderizado |
| `resultados/` | Videos renderizados del proyecto |

## Algoritmo

La función `find_bridges(n, edges)` devuelve:

```text
(puentes, traza, tin, low)
```

Realiza un DFS con listas de adyacencia de pares `(vecino, id_arista)`.
Cuando termina de recorrer un hijo `to` de un vértice `v`, la arista `(v, to)`
es un puente si:

```text
low[to] > tin[v]
```

El identificador de arista permite distinguir correctamente las aristas
paralelas. Además, se inicia un DFS desde cada vértice que todavía no haya
sido visitado para procesar grafos con varias componentes.

Para el ejemplo de la guía, con 7 vértices y 8 aristas, se obtienen:

```text
puentes = {(3, 4), (6, 7)}
tin = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}
low = {1: 0, 2: 0, 3: 0, 4: 3, 5: 3, 6: 3, 7: 6}
```

### Ejecutar las pruebas

Desde la raíz del proyecto:

```bash
cd "implementacion del codigo"
../.venv/bin/python -m unittest test_bridges -v
```

## Animación

El archivo `animaciones/bridges_lesson.py` contiene la escena
`BridgesLesson`, organizada en cuatro secciones:

| Sección | Duración | Contenido |
|---|---:|---|
| `e0_portada` | 10 s | Título, curso e integrantes |
| `e1_motivacion` | 25 s | Dos grupos unidos por una arista crítica |
| `e2_concepto` | 30 s | Definición de puente, componentes y ciclos |
| `e3_algoritmo` | 45 s | DFS, valores `tin` y `low`, retroceso y condición del puente |

La duración de cada sección está definida en `TIEMPOS` y las marcas de las
explicaciones en `MARCAS`. La franja inferior de la escena queda libre para
incorporar personajes durante la postproducción.

### Renderizar la animación

Para generar el video con Manim:

```bash
cd animaciones
../.venv/bin/python -m manim --save_sections bridges_lesson.py BridgesLesson
```

Para crear el video de avance en `resultados/`:

```bash
ffmpeg -y -i media/videos/bridges_lesson/1440p30/BridgesLesson.mp4 \
  -c copy -movflags +faststart ../resultados/BridgesLesson_avance_mitad.mp4
```

Para una revisión rápida se puede añadir `-ql` al comando de Manim.

## Trabajo pendiente

- Implementar las escenas 4, 5 y 6: demostración completa con la traza,
  casos límite, complejidad y cierre.
- Incorporar y sincronizar las voces.
- Ajustar `TIEMPOS` y `MARCAS` después de integrar el audio.
- Completar la postproducción y generar la versión final del video.
