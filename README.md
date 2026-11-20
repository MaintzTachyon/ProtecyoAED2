# Proyecto AED2: Puentes en grafos

Un **puente** de un grafo no dirigido es una arista cuya eliminación desconecta el grafo (o, en general, aumenta su número de componentes conexas). Este proyecto implementa el cálculo de puentes y presenta el tema en una animación hecha con Python y Manim. También incluye una explicación de los valores `tin` y `low`, una ejecución animada del recorrido DFS y una comparación con el método de fuerza bruta.

## Integrantes

- Juan Diego Mejía Armas
- Marcelo Rosillo Rodríguez

Curso: Algoritmos y Estructuras de Datos.

## Video final

El video terminado se encuentra en `resultados/VideoFinal/videoAEDv4.mp4`. Tiene una duración aproximada de 2 minutos y 23 segundos, resolución 1920 × 1080, 24 fps y pista de audio AAC, para la edicion se utilizo DaVinci Resolve 21.

Para trabajar con la animación original se guardaron también estos archivos:

- `resultados/BridgesLesson_fondo.mp4`: versión generada en Manim a 2560 × 1440 y 30 fps, sin audio.
- `resultados/BridgesLesson_preview.mp4`: vista previa a 960 × 540.
- `resultados/escenas/`: siete partes independientes del video base y su archivo `BridgesLesson.json`.
- `resultados/escenas_preview/`: las mismas siete partes en resolución de vista previa.

> **Nota sobre la reproducibilidad:** las imágenes de personajes y las voces no forman parte de la animación generada con Manim, estas fueron agregadas en postproducción con el fin de hacer el video más entretenido para la audiencia.Estos materiales no están incluidos en el repositorio, por lo que `renderizar.py` solo regenera la animación base `BridgesLesson_fondo.mp4` y sus clips, no `videoAEDv4.mp4`.

La animación base se renderiza a 30 fps y 2560 × 1440; el video final se exportó a 24 fps y 1920 × 1080 al unir el material con el audio.

## Contenido del video

| Parte | Tiempo aproximado | Contenido |
|---|---|---|
| 0 | 0:00-0:04 | Portada, curso e integrantes |
| 1 | 0:04-0:23 | Ejemplo inicial con una conexión crítica |
| 2 | 0:23-0:43 | Definición de puente y relación con componentes y ciclos |
| 3 | 0:43-0:51 | Recorrido DFS y valores `tin` y `low` |
| 4 | 0:51-1:11 | Ejecución del algoritmo sobre el ejemplo principal |
| 5 | 1:11-1:45 | Árboles, ciclos y aristas paralelas |
| 6 | 1:45-2:23 | Complejidad, comparación y cierre |

Los tiempos de las escenas están definidos por `TIEMPOS` y los momentos destacados por `MARCAS`, ambos ubicados en `animaciones/bridges_lesson.py`. La animación base suma 4282 fotogramas a 30 fps.

## Organización del proyecto

```text
ProyectoAED2/
├── animaciones/
│   ├── bridges_lesson.py
│   └── manim.cfg
├── implementacion del codigo/
│   ├── bridges.py
│   └── test_bridges.py
├── assets/fonts/
├── resultados/
│   ├── VideoFinal/videoAEDv4.mp4
│   ├── BridgesLesson_fondo.mp4
│   ├── BridgesLesson_preview.mp4
│   ├── escenas/
│   └── escenas_preview/
├── renderizar.py
├── requirements.txt
└── README.md
```


## Implementación del algoritmo

La función principal está en `implementacion del codigo/bridges.py`. `find_bridges(n, edges)` recibe la cantidad de nodos y una lista de aristas, y devuelve los puentes encontrados, la traza del recorrido, el arreglo `tin` y el arreglo `low`.

Los nodos se representan con números del 1 a `n`. En la lista de adyacencia cada entrada guarda el nodo vecino y el identificador de su arista. Ese identificador permite distinguir aristas paralelas y evita confundir la arista padre con otra arista que conecte los mismos vértices.

- `tin[v]`: momento en el que el DFS descubre el nodo `v`.
- `low[v]`: menor tiempo de descubrimiento al que `v` puede llegar usando aristas del árbol y a lo sumo una arista de retroceso.
- Si `v` es hijo de `u` en el árbol DFS, la arista `(u, v)` es puente cuando `low[v] > tin[u]`.

La animación registra los eventos `enter`, `tree_edge`, `back_edge`, `check`, `bridge` y `exit`. Con ellos construye la tabla de valores y actualiza el recorrido paso a paso. Al terminar, se verifica que los datos mostrados coincidan con el resultado que entrega la implementación.

### Ejemplo de uso

Un grafo de cuatro nodos con un triángulo (1, 2, 3) y una arista colgante (3, 4):

```python
from bridges import find_bridges

n = 4
edges = [(1, 2), (2, 3), (3, 1), (3, 4)]

bridges, trace, tin, low = find_bridges(n, edges)

print(bridges)  # [(3, 4)]
print(tin)      # {1: 0, 2: 1, 3: 2, 4: 3}
print(low)      # {1: 0, 2: 0, 3: 0, 4: 3}
```

La arista `(3, 4)` es puente porque `low[4] = 3 > tin[3] = 2`. Las aristas del triángulo no lo son porque pertenecen a un ciclo.

### Ejemplo principal del video

El ejemplo del video tiene siete nodos y produce los puentes `(3, 4)` y `(6, 7)`:

```text
tin = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}
low = {1: 0, 2: 0, 3: 0, 4: 3, 5: 3, 6: 3, 7: 6}
```

## Complejidad

El algoritmo recorre el grafo mediante un DFS y tarda **O(|V| + |E|)**. También usa **O(|V| + |E|)** de memoria para guardar la lista de adyacencia, los valores `tin` y `low`, y la pila del recorrido.

En el video se mide la cantidad de revisiones hechas en la lista de adyacencia para una cadena de 25 nodos y 24 aristas:

| Método | Revisiones | Cómo se obtiene |
|---|---|---|
| DFS con `tin` y `low` | 48 | 2 · \|E\| = 2 · 24 (cada arista aparece dos veces en la adyacencia) |
| Fuerza bruta | 1200 | 25 recorridos × 48 revisiones: uno de referencia más uno por cada una de las 24 aristas eliminadas |

Esta comparación mide revisiones de la adyacencia, no el tiempo real de ejecución. Cada intento de fuerza bruta también cuenta las revisiones del recorrido inicial de referencia.

## Instalación y ejecución

El proyecto fue probado con Python 3.12 y Manim 0.21.0. La instalación desde la raíz del proyecto, en Windows, es:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para ejecutar las pruebas:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s "implementacion del codigo" -v
```

Para generar nuevamente la animación base completa y sus siete clips:

```powershell
.\.venv\Scripts\python.exe renderizar.py
```

Para generar una vista previa de 960 × 540 a 30 fps:

```powershell
.\.venv\Scripts\python.exe renderizar.py --preview
```

En Linux o macOS se usa `.venv/bin/python` en lugar de `.venv\Scripts\python.exe`. El lanzador ejecuta Manim desde `animaciones/`, guarda el resultado en `resultados/` y conserva los clips separados gracias a `--save_sections`.

También se puede ejecutar Manim directamente desde la carpeta `animaciones/`:

```powershell
..\.venv\Scripts\python.exe -m manim --save_sections bridges_lesson.py BridgesLesson
```

Las fuentes DejaVu están incluidas en `assets/fonts/`. El texto de la animación usa objetos `Text`, por lo que no es necesario instalar LaTeX.

## Pruebas realizadas

La batería tiene diez pruebas y cubre el ejemplo principal, árboles, ciclos, aristas paralelas, bucles, grafos con varias componentes conexas, grafos sin aristas y grafos de un solo nodo. También compara los resultados del DFS con la fuerza bruta en los **1099 grafos simples etiquetados de 1 a 5 nodos** (1 + 2 + 8 + 64 + 1024) y verifica las mediciones utilizadas en la comparación del video.

## Referencias

- [Documentación oficial de Manim](https://docs.manim.community/en/stable/).
- Licencia de las fuentes DejaVu incluida en `assets/fonts/LICENSE_DEJAVU`.