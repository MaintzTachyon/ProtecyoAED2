# Hola, este es el codigo de la animacion demo.
# Esto es solo un avance para ver como va el video, no es el final.
# La idea fue copiar el estilo del video de listas enlazadas que nos pasaron:
# fondo oscurito, verde para dibujar, amarillo para resaltar y rojo solo
# para el puente. Todo con DejaVu Sans porque en la compu no tenemos LaTeX.
#
# Por ahora la demo tiene 2 partes nada mas:
#   1) la portada con el titulo y los nombres
#   2) el grafo con el pseudocodigo y una sola operacion (la de 6-7)
# Despues agregamos las escenas del plan, por ahora no nos preocupamos
# por los tiempos de las voces.

import sys
from pathlib import Path

# bridges.py esta en la carpeta de al lado ("implementacion del codigo"),
# asi que le avisamos a python donde buscarlo
sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "implementacion del codigo")
)

from manim import (
    RED,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Text,
    Transform,
    VGroup,
    Write,
)

from bridges import EDGES_EJEMPLO, N_EJEMPLO, find_bridges

# los colores que vimos en el video referencia, los copiamos tal cual
FONDO = "#101827"
BLANCO = "#EDF3FC"
GRIS = "#A9B8CF"
VERDE = "#40D9C0"
AMARILLO = "#FFCC66"
ROJO = "#FF5555"

# donde va cada nodo en la demo, lo dejamos a la izquierda para que
# el codigo entre a la derecha
POSICIONES = {
    1: (-6.0, 1.5, 0),
    2: (-4.8, 2.4, 0),
    3: (-3.6, 1.5, 0),
    4: (-2.0, 1.5, 0),
    5: (-0.8, 2.4, 0),
    6: (-0.8, 0.5, 0),
    7: (0.8, 0.5, 0),
}


def texto(s, size=28, color=BLANCO):
    # ayudita para escribir todo con la misma fuente sin LaTeX
    return Text(s, font="DejaVu Sans", font_size=size, color=color)


class BridgesLesson(Scene):
    """La demo basica que pedimos para el avance: portada + una operacion."""

    # --- los dibujitos basicos, copiados del estilo del video referencia ---
    def crear_nodo_grafo(self, v):
        c = Circle(radius=0.34, color=VERDE, stroke_width=4)
        c.move_to(POSICIONES[v])
        c.set_fill("#1E3448", opacity=1)
        n = texto(str(v), 26)
        n.move_to(c)
        return VGroup(c, n)

    def crear_arista(self, u, v, color=VERDE):
        return Line(POSICIONES[u], POSICIONES[v], color=color, stroke_width=5)

    def crear_grafo_demo(self):
        # arma los 7 nodos y las 8 aristas del ejemplo de la guia
        nodos = {v: self.crear_nodo_grafo(v) for v in range(1, N_EJEMPLO + 1)}
        aristas = {}
        for u, v in EDGES_EJEMPLO:
            aristas[(min(u, v), max(u, v))] = self.crear_arista(u, v)
        return nodos, aristas

    def cambiar_titulo(self, num, titulo):
        # igual que en el video de listas: arriba a la izquierda el numerito
        # en verde y el titulo en blanco
        if hasattr(self, "titulo_actual"):
            self.play(FadeOut(self.titulo_actual), run_time=0.3)
        self.titulo_actual = VGroup(
            texto(f"{num:02} / 02", 20, VERDE), texto(titulo, 36)
        )
        # juntamos las dos lineas una abajo de la otra alineadas a la izquierda
        self.titulo_actual.arrange(
            __import__("manim").DOWN,
            aligned_edge=__import__("manim").LEFT,
            buff=0.18,
        ).to_corner(__import__("manim").UL, buff=0.55)
        self.play(FadeIn(self.titulo_actual), run_time=0.4)

    def construct(self):
        self.camera.background_color = FONDO

        # ====== ESCENA 0: solo la portada con el titulo y los nombres ======
        self.next_section("portada")
        titulo = VGroup(
            texto("PUENTES EN GRAFOS", 60, VERDE),
            texto("Analisis y Diseno de Algoritmos", 30),
            texto("Busqueda de puentes con DFS (Tarjan)", 24, GRIS),
        ).arrange(
            __import__("manim").DOWN, buff=0.45
        )
        integrantes = VGroup(
            texto("Integrantes", 22, VERDE),
            texto("Juan Diego Mejia Armas", 26),
            texto("Marcelo Rosillo Rodriguez", 26),
        ).arrange(__import__("manim").DOWN, buff=0.2)
        portada = VGroup(titulo, integrantes).arrange(
            __import__("manim").DOWN, buff=0.65
        )
        self.play(Write(portada), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(portada), run_time=0.5)

        # ====== DEMO: mostramos el algoritmo y una sola operacion ======
        self.next_section("demo_algoritmo")
        self.cambiar_titulo(1, "Demo: find_bridges")

        # las tres lineas clave del pseudocodigo, para que se vea que
        # es lo que hace el codigo de verdad
        codigo = VGroup(
            texto("tin[v] = low[v] = t", 22, BLANCO),
            texto("low[v] = min(low[v], low[to])", 22, BLANCO),
            texto("si low[to] > tin[v] -> puente", 22, AMARILLO),
        ).arrange(__import__("manim").DOWN, aligned_edge=__import__("manim").LEFT, buff=0.25)
        codigo.move_to([4.8, 0.6, 0])

        # cartel de abajo que dice que operacion vamos a mostrar
        operacion = texto(
            "Operacion demo: comprobar (6,7)", 22, AMARILLO
        ).move_to([0, -1.2, 0])

        self.play(FadeIn(codigo), run_time=0.6)
        self.play(FadeIn(operacion), run_time=0.6)

        # dibujamos el grafo del ejemplo
        nodos, aristas = self.crear_grafo_demo()
        grafo = VGroup(*aristas.values(), *nodos.values())
        self.play(Create(grafo), run_time=1.2)

        # ahora si, llamamos al algoritmo de verdad.
        # los numeros que van a aparecer abajo salen de aca, no los escribimos a mano
        puentes, traza, tin, low = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)

        # mostramos el tin de cada nodo en el orden en que el DFS los descubre
        tin_labels = {}
        for v in range(1, N_EJEMPLO + 1):
            tin_labels[v] = texto(f"tin={tin[v]}", 18, AMARILLO)
            tin_labels[v].next_to(nodos[v], __import__("manim").DOWN, buff=0.15)
            self.play(
                nodos[v][0].animate.set_color(AMARILLO),
                FadeIn(tin_labels[v]),
                run_time=0.35,
            )

        # la unica operacion que mostramos en detalle: la arista 6-7
        # en este caso low[7]=6 y tin[6]=5, como 6 > 5 es puente
        cuenta = texto(
            f"low[7]={low[7]} > tin[6]={tin[6]} -> puente (6,7)",
            24, ROJO,
        ).move_to([0, -1.9, 0])
        self.play(
            aristas[(6, 7)].animate.set_color(ROJO).set_stroke_width(9),
            Transform(operacion, cuenta),
            run_time=0.6,
        )
        self.wait(1.2)

        # cierre chiquito: acordamos que tambien (3,4) es puente,
        # pero no lo animamos en detalle para que la demo sea corta
        resultado = texto(
            "Puentes: (3,4) y (6,7)  (salida de find_bridges)",
            22, ROJO,
        ).move_to([0, -2.4, 0])
        self.play(FadeIn(resultado), run_time=0.5)
        self.wait(1.5)


if __name__ == "__main__":
    BridgesLesson().render()
