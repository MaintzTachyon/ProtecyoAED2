# Proyecto AED2: Puentes en grafos

Video educativo de **2:23 minutos**, **2560 × 1440 píxeles**, **30 fps** y
**sin audio**. Explica los puentes de un grafo no dirigido y cómo encontrarlos
con un DFS y los valores `tin` y `low`. La animación se genera con Python y
Manim 0.21.0 a partir de la implementación del grupo. Los tiempos están
ajustados al audio final `references/Demo1.mp3`.

Integrantes: Juan Diego Mejía Armas y Marcelo Rosillo Rodríguez.
Curso: CS2023 - Algoritmos y Estructuras de Datos.

## Ver el resultado

- `resultados/BridgesLesson_fondo.mp4`: video completo, sin pista de audio.
- `resultados/escenas/`: los siete clips por separado y su índice JSON.

Esta versión continúa el avance recibido (escenas 0 a 3) y completa las
escenas 4 a 6. Se mantiene la franja inferior libre para una posible edición
posterior. Las voces y las imágenes de personajes no forman parte de esta
versión, conforme al alcance elegido.

## Contenido y tiempos

| Escena | Intervalo | Contenido |
|---|---|---|
| 0 | 0:00-0:04 | Título, curso e integrantes |
| 1 | 0:04-0:23 | Motivación: una conexión crítica entre dos grupos |
| 2 | 0:23-0:43 | Definición de puente, componentes conexas y ciclos |
| 3 | 0:43-0:51 | DFS, descubrimiento `tin`, `low` y condición del puente |
| 4 | 0:51-1:11 | Ejecución completa guiada por la traza real |
| 5 | 1:11-1:45 | Árbol, ciclo y aristas paralelas |
| 6 | 1:45-2:23 | Complejidad, medición de revisiones y cierre |

`TIEMPOS` contiene los fotogramas de cada sección y `MARCAS` sus momentos
de énfasis. Las siete secciones suman 4282 fotogramas a 30 fps.

## Organización

```text
ProyectoAED2/
├── animaciones/bridges_lesson.py, manim.cfg
├── implementacion del codigo/bridges.py, test_bridges.py
├── assets/fonts/                # Fuentes y licencia
├── resultados/BridgesLesson_fondo.mp4
├── resultados/escenas/          # Siete clips e índice JSON
├── renderizar.py
├── requirements.txt
├── CAMBIOS.md
└── README.md
```

## Algoritmo y vínculo con la animación

`find_bridges(n, edges)` devuelve `(puentes, traza, tin, low)`. Los nodos
se numeran de 1 a `n`. La lista de adyacencia guarda `(vecino, id_arista)`;
el DFS ignora solo la arista por la que llegó, lo que permite tratar las
aristas paralelas correctamente. También recorre todas las componentes.

- `tin[v]`: instante de descubrimiento de `v`.
- `low[v]`: menor tiempo de descubrimiento alcanzable bajando por el árbol
  DFS desde `v` y usando, como máximo, una arista de retroceso.
- Para una arista del árbol DFS de `u` a su hijo `v`, es puente si
  `low[v] > tin[u]`.

La escena 4 reproduce los eventos `enter`, `tree_edge`, `back_edge`,
`check`, `bridge` y `exit`. Actualiza la tabla y la pila desde esos eventos;
comprueba al terminar que sus valores coinciden con el resultado real.
La escena 5 llama al algoritmo para cada caso y colorea sus resultados.
No se usa una implementación de puentes de una librería externa.

El ejemplo de siete nodos produce los puentes `{(3, 4), (6, 7)}`:

```text
tin = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}
low = {1: 0, 2: 0, 3: 0, 4: 3, 5: 3, 6: 3, 7: 6}
```

## Complejidad y medición

El DFS tarda **O(|V| + |E|)** y usa **O(|V| + |E|)** de espacio, incluyendo
la adyacencia y la pila recursiva. Conserva el orden de entrada de las
aristas; no ordena las listas de adyacencia.

La escena 6 compara el número real de revisiones de adyacencia en una
cadena de 25 nodos y 24 aristas: **48 con DFS** y **1200 con fuerza bruta**.
Las barras tienen longitudes proporcionales a esos contadores. Cada intento
de fuerza bruta cuenta las componentes al excluir una arista por su id;
también se incluye el recorrido inicial de referencia. La unidad medida
es una revisión de una entrada de adyacencia, no tiempo de ejecución.

## Instalación y ejecución en Windows

Probado con Python 3.12 y Manim 0.21.0. Desde la raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s "implementacion del codigo" -v
```

Generar el video completo y los siete clips:

```powershell
.\.venv\Scripts\python.exe renderizar.py
```

Generar una vista previa a 960 × 540, manteniendo 30 fps:

```powershell
.\.venv\Scripts\python.exe renderizar.py --preview
```

En Linux/macOS, los comandos equivalentes usan `.venv/bin/python`.
El lanzador ejecuta Manim desde `animaciones/`, copia el resultado a
`resultados/` y conserva clips separados mediante `--save_sections`.
También se puede ejecutar Manim directamente desde `animaciones/`:

```powershell
..\.venv\Scripts\python.exe -m manim --save_sections bridges_lesson.py BridgesLesson
```

Las fuentes están incluidas y se cargan solo para el proceso. Todos los
textos usan `Text`; no se requiere LaTeX. Manim utiliza Cairo y Pango.

## Verificación

Hay diez pruebas, que incluyen el ejemplo, árboles, ciclos, aristas
paralelas, bucles, componentes desconectadas, grafos sin aristas y un solo
nodo. Una prueba dentro de esa batería compara con fuerza bruta los
**1099 grafos simples etiquetados de hasta cinco nodos**. Otra comprueba
los contadores usados en las barras.

## Referencias y entrega

- Enunciado del curso: Proyecto 2, CS2023, periodo 2026-2.
- Guía de programación y planificación de puentes proporcionadas por el grupo.
- Estilo y estructura del proyecto AED1 del grupo como referencia de continuidad.
- [Documentación oficial de Manim](https://docs.manim.community/en/stable/).
- Fuentes DejaVu: licencia incluida en `assets/fonts/LICENSE_DEJAVU`.

Para incorporar esta versión, suban los cambios al repositorio original
conservando su historial. La descarga ZIP no contiene los commits de Git.
El enlace del repositorio, el enlace accesible del video y el informe
académico se gestionan por separado según las indicaciones del curso.
