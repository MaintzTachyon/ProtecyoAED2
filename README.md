# Proyecto AED2: Puentes en grafos

En este README.md se mostrara los avances realizados de nuestro poryecto

## Estructura del proyecto

```text
ProyectoAED2/
├── implementacion del codigo/   implementación del algoritmo en Python
├── animaciones/                 archivos fuente de la demostración con Manim
├── media/                   archivos generados durante el renderizado
└── resultados/                  video renderizado de la demostración
```

- `implementacion del codigo/`: `bridges.py` (el algoritmo) y `test_bridges.py` (las pruebas).
- `animaciones/`: `bridges_lesson.py` (la demo), `manim.cfg` y la carpeta `media/`.
  Dentro de `media/` se guardan los archivos que Manim genera durante el
  renderizado, como SVG, archivos temporales y otros recursos de la animación.
- `resultados/`: el video renderizado (`avance_demo.mp4`), para verlo sin volver a renderizar.

## Algoritmo implementado

La función principal es `find_bridges(n, edges)`. Recibe un grafo no dirigido,
cuyos vértices están numerados de 1 a `n`, y devuelve
`(puentes, traza, tin, low)`:

- `puentes` contiene las aristas identificadas como puentes.
- `tin` registra el momento en que cada vértice es descubierto durante el
  recorrido DFS.
- `low` indica el vértice más antiguo al que se puede llegar desde un vértice
  dado mediante las aristas del subárbol correspondiente, sin utilizar dos
  veces la misma arista.
- `traza` es una secuencia de eventos que utilizamos para que la animación
  represente el comportamiento real del algoritmo.

La implementación se basa en el algoritmo de Tarjan. Se realiza un recorrido
DFS y, al regresar desde un hijo `to` hacia su padre `v`, se verifica la
condición `low[to] > tin[v]`. Si se cumple, la arista `v-to` es un puente.

Una parte que nos costó fue manejar los grafos con aristas paralelas. Ignorar al vértice padre no alcanza: hay que ignorar la arista exacta por la que llegamos, porque si no, dos aristas entre 1 y 2 se clasificarían mal. Por eso la lista de adyacencia guarda pares `(vecino, id_arista)`.

Para comprobar el funcionamiento, utilizamos el grafo de ejemplo de la guía,
con 7 vértices y 8 aristas:
`(1,2),(2,3),(3,1),(3,4),(4,5),(5,6),(6,4),(6,7)`.
El programa obtiene:

```text
tin = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6}
low = {1:0, 2:0, 3:0, 4:3, 5:3, 6:3, 7:6}
puentes = {(3,4), (6,7)}
```

Estos valores son los mismos que da la guía del proyecto.

### Pruebas

Para ejecutar las pruebas:

```bash
cd "implementacion del codigo"
../.venv/bin/python -m unittest test_bridges -v
```

Por ahora hay siete pruebas, todas pasan: el ejemplo de la guía, un árbol (todas sus aristas son puentes), un ciclo (ningún puente), un grafo con aristas paralelas, un grafo sin aristas, un grafo de un solo vértice y un grafo no conexo.

## Demostración animada

Usamos como base el estilo visual del video de listas enlazadas: fondo oscuro (`#101827`), verde (`#40D9C0`) para el grafo, amarillo (`#FFCC66`) para resaltar y rojo solo para los puentes. La fuente es DejaVu Sans.

Como parte de la preparación del entorno para este proyecto, instalamos
LaTeX, incluyendo los comandos `latex` y `pdflatex`, ya que Manim los
necesita cuando se utilizan objetos como `Tex` o `MathTex`. La demostración
actual utiliza principalmente `Text` con la fuente DejaVu Sans, por lo que
esas escenas no dependen directamente de LaTeX; sin embargo, la instalación
queda disponible para las escenas y fórmulas que se incorporen en la versión
final.

La demostración actual incluye dos partes:

1. **Portada:** presenta el título *Puentes en grafos*, el curso y los
   nombres de los integrantes.
2. **Demostración del algoritmo:** muestra el pseudocódigo con sus tres líneas
   principales a la derecha, el grafo a la izquierda y una operación del
   recorrido en la parte inferior:
   `low[7]=6 > tin[6]=5 -> puente (6,7)`.

Los valores de esa operación salen directo de `find_bridges`, no los escribimos a mano en la animación.

### Renderizado de la demostración

```bash
cd animaciones
../.venv/bin/python -m manim -ql bridges_lesson.py BridgesLesson
cp media/videos/BridgesLesson.mp4 ../resultados/avance_demo.mp4
```

El video queda en `resultados/avance_demo.mp4`: 854x480, unos 12 segundos y sin audio. Por ahora renderizamos en calidad baja (`-ql`) para revisar rápido; la versión final será en 2560x1440, como pide la guía.

## Trabajo pendiente

- Completar las escenas 1 a 6 descritas en el plan: motivación, concepto,
  explicación de `tin` y `low`, demostración completa, casos límite y
  complejidad, junto con el cierre.
- Ajustar los tiempos de `TIEMPOS` y `MARCAS` después de incorporar las
  voces.
- Generar el renderizado final en alta resolución y completar la
  documentación para la entrega.

---