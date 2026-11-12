"""Escenas 0 a 3: portada, motivacion, concepto y tin/low."""

import json
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "implementacion del codigo")
)
from bridges import EDGES_EJEMPLO, N_EJEMPLO, find_bridges

FONDO = "#101827"
BLANCO = "#EDF3FC"
GRIS = "#A9B8CF"
VERDE = "#40D9C0"
AMARILLO = "#FFCC66"
ROJO = "#FF5555"

config.background_color = FONDO

RUTA_INDICE = Path(__file__).with_name("media") / "indice_textos.json"
INDICE_TEXTOS = json.loads(RUTA_INDICE.read_text()) if RUTA_INDICE.exists() else {}


class TextoGuardado(Text):
    def _text2svg(self, color):
        nombre = self._text2hash(color) + ".svg"
        registro = INDICE_TEXTOS.get(nombre)
        if registro is None:
            return super()._text2svg(color)
        destino = config.get_dir("text_dir") / registro["archivo"]
        if not destino.exists():
            Path(super()._text2svg(color)).rename(destino)
        return str(destino.resolve())


def texto(s, size=28, color=BLANCO):
    return TextoGuardado(s, font="DejaVu Sans", font_size=size, color=color)


def texto_mono(s, size=16, color=BLANCO):
    return TextoGuardado(s, font="DejaVu Sans Mono", font_size=size, color=color)


FPS = 30
TIEMPOS = {"e0": 300, "e1": 750, "e2": 900, "e3": 1350}
MARCAS = {
    "e1_islas": 0.0,
    "e1_ruptura": 9.0,
    "e1_pregunta": 15.0,
    "e1_puentes": 22.0,
    "e2_grafo": 0.0,
    "e2_rojas": 5.0,
    "e2_quita34": 13.0,
    "e2_quita12": 18.0,
    "e2_ciclo": 22.0,
    "e3_inicio": 0.0,
    "e3_tin": 8.0,
    "e3_low": 13.0,
    "e3_retroceso": 19.0,
    "e3_condicion": 31.0,
    "e3_puente": 40.0,
}

Y_MIN_ANIMACION = -2.4

POSICIONES = {
    1: (-4.4, 0.6, 0),
    2: (-3.2, 1.7, 0),
    3: (-2.0, 0.6, 0),
    4: (0.2, 0.6, 0),
    5: (1.4, 1.7, 0),
    6: (1.4, -0.5, 0),
    7: (3.0, -0.5, 0),
}


def componentes(n, edges, sin_arista=None):
    ady = {v: [] for v in range(1, n + 1)}
    for u, v in edges:
        if sin_arista and {u, v} == set(sin_arista):
            continue
        ady[u].append(v)
        ady[v].append(u)

    vistos, comps = set(), []
    for inicio in range(1, n + 1):
        if inicio in vistos:
            continue
        pila, comp = [inicio], []
        while pila:
            x = pila.pop()
            if x in vistos:
                continue
            vistos.add(x)
            comp.append(x)
            pila.extend(ady[x])
        comps.append(sorted(comp))
    return comps


class BridgesLesson(Scene):

    def crear_nodo(self, etiqueta, pos, radio=0.34, color=VERDE):
        circulo = Circle(radius=radio, color=color, stroke_width=4)
        circulo.move_to(pos)
        circulo.set_fill("#1E3448", opacity=1)
        return VGroup(circulo, texto(str(etiqueta), 24).move_to(circulo))

    def crear_nodo_grafo(self, v):
        return self.crear_nodo(v, POSICIONES[v])

    def crear_arista(self, p1, p2, color=VERDE, radio=0.34, punteada=False):
        a, b = np.array(p1, dtype=float), np.array(p2, dtype=float)
        d = (b - a) / np.linalg.norm(b - a)
        inicio, fin = a + d * radio, b - d * radio
        if punteada:
            return DashedLine(inicio, fin, color=color, dash_length=0.12,
                              stroke_width=3)
        return Line(inicio, fin, color=color, stroke_width=5)

    def crear_grafo_demo(self, escala=1.0, centro=ORIGIN):
        nodos = {v: self.crear_nodo_grafo(v) for v in range(1, N_EJEMPLO + 1)}
        aristas = {}
        for u, v in EDGES_EJEMPLO:
            aristas[(min(u, v), max(u, v))] = self.crear_arista(
                POSICIONES[u], POSICIONES[v])
        grafo = VGroup(*aristas.values(), *nodos.values())
        grafo.scale(escala).move_to(centro)
        return nodos, aristas

    def cambiar_titulo(self, num, titulo):
        if hasattr(self, "titulo_actual"):
            self.play(FadeOut(self.titulo_actual), run_time=0.25)
        self.titulo_actual = VGroup(
            texto(f"{num:02} / 06", 20, VERDE), texto(titulo, 34))
        self.titulo_actual.arrange(
            DOWN, aligned_edge=LEFT, buff=0.16).to_corner(UL, buff=0.5)
        self.play(FadeIn(self.titulo_actual, shift=RIGHT * 0.1), run_time=0.35)

    def abrir_seccion(self, nombre, fotogramas):
        self.next_section(nombre)
        self._inicio = self.time
        self._fotogramas = fotogramas

    def esperar_hasta(self, segundo):
        restante = segundo - (self.time - self._inicio)
        if restante > 0:
            self.wait(restante)

    def mostrar_parte(self, fotogramas, *animaciones, run_time=1.0):
        inicio = self.time
        if animaciones:
            self.play(*animaciones, run_time=run_time)
        restante = fotogramas / FPS - (self.time - inicio)
        if restante > 0:
            self.wait(restante)

    def cerrar_seccion(self):
        restante = self._fotogramas / FPS - (self.time - self._inicio)
        if restante > 0:
            self.wait(restante)

    def colorear_componentes(self, nodos, comps, colores=(VERDE, AMARILLO)):
        animaciones = []
        for i, comp in enumerate(comps):
            color = colores[i % len(colores)]
            for v in comp:
                animaciones.append(
                    nodos[v][0].animate.set_stroke(color).set_fill(
                        color, opacity=0.2))
        return animaciones

    def limpiar_escena(self):
        objetos = [o for o in self.mobjects
                   if o is not getattr(self, "titulo_actual", None)]
        if objetos:
            self.play(*[FadeOut(o) for o in objetos], run_time=0.4)

    def construct(self):
        self.escena_0()
        self.escena_1()
        self.escena_2()
        self.escena_3()

    def escena_0(self):
        self.abrir_seccion("e0_portada", TIEMPOS["e0"])
        titulo = VGroup(
            texto("PUENTES EN GRAFOS", 58, VERDE),
            texto("Analisis y Diseno de Algoritmos", 28),
            texto("Busqueda de puentes con DFS (Tarjan)", 22, GRIS),
        ).arrange(DOWN, buff=0.4)
        integrantes = VGroup(
            texto("Integrantes", 20, VERDE),
            texto("Juan Diego Mejia Armas", 24),
            texto("Marcelo Rosillo Rodriguez", 24),
        ).arrange(DOWN, buff=0.16)
        portada = VGroup(titulo, integrantes).arrange(DOWN, buff=0.55)

        self.mostrar_parte(75, Write(portada), run_time=1.3)
        self.mostrar_parte(150)
        self.mostrar_parte(40, FadeOut(portada), run_time=0.4)
        self.cerrar_seccion()

    def escena_1(self):
        self.abrir_seccion("e1_motivacion", TIEMPOS["e1"])
        self.cambiar_titulo(1, "Por que importan los puentes")

        pos_l = {1: (-5.7, 0.8, 0), 2: (-5.0, 1.8, 0), 3: (-4.3, 0.8, 0)}
        pos_r = {4: (2.2, 0.8, 0), 5: (2.9, 1.8, 0), 6: (3.6, 0.8, 0)}
        nodos_l = VGroup(*[self.crear_nodo(v, pos_l[v]) for v in (1, 2, 3)])
        nodos_r = VGroup(*[self.crear_nodo(v, pos_r[v]) for v in (4, 5, 6)])
        aristas_l = VGroup(*[self.crear_arista(pos_l[u], pos_l[v])
                             for u, v in ((1, 2), (2, 3), (3, 1))])
        aristas_r = VGroup(*[self.crear_arista(pos_r[u], pos_r[v])
                             for u, v in ((4, 5), (5, 6), (6, 4))])
        cable = self.crear_arista(pos_l[3], pos_r[4], color=AMARILLO)
        isla_l = VGroup(aristas_l, nodos_l)
        isla_r = VGroup(aristas_r, nodos_r)

        nota = texto("Dos grupos unidos por una sola arista", 24, GRIS)
        nota.move_to([0, -1.4, 0])
        self.play(Create(isla_l), Create(isla_r), Create(cable),
                  FadeIn(nota), run_time=1.4)
        self.play(Indicate(cable, color=AMARILLO), run_time=1.0)

        self.esperar_hasta(MARCAS["e1_ruptura"])
        self.play(
            FadeOut(cable),
            Transform(nota, texto("Se corta el cable: la red queda partida",
                                  24, ROJO).move_to(nota)),
            run_time=0.8,
        )
        self.play(isla_l.animate.shift(LEFT * 0.8),
                  isla_r.animate.shift(RIGHT * 0.8), run_time=1.6)

        self.esperar_hasta(MARCAS["e1_pregunta"])
        self.play(Transform(
            nota,
            texto("¿Como saber que aristas son criticas?", 26, AMARILLO)
            .move_to([0, -1.7, 0])), run_time=0.7)

        self.esperar_hasta(MARCAS["e1_puentes"])
        self.play(Transform(nota, texto("PUENTES", 54, AMARILLO)
                            .move_to([0, -0.9, 0])), run_time=0.8)
        self.cerrar_seccion()

    def escena_2(self):
        self.abrir_seccion("e2_concepto", TIEMPOS["e2"])
        self.limpiar_escena()
        self.cambiar_titulo(2, "Que es un puente")

        nodos, aristas = self.crear_grafo_demo(centro=[0, 0.2, 0])
        self.play(*[Create(e) for e in aristas.values()],
                  *[FadeIn(n) for n in nodos.values()], run_time=1.5)

        puentes, _, _, _ = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)
        nota = texto("Puente: al quitarlo aumentan las componentes conexas",
                     22, GRIS).move_to([0, -1.7, 0])
        self.play(FadeIn(nota), run_time=0.5)

        self.esperar_hasta(MARCAS["e2_rojas"])
        self.play(*[aristas[p].animate.set_color(ROJO).set_stroke_width(9)
                    for p in puentes], run_time=0.8)
        self.play(Transform(nota, texto("En rojo, las aristas puente",
                                        22, ROJO).move_to(nota)), run_time=0.5)

        self.esperar_hasta(MARCAS["e2_quita34"])
        self.play(FadeOut(aristas[(3, 4)]), run_time=0.6)
        comps = componentes(N_EJEMPLO, EDGES_EJEMPLO, sin_arista=(3, 4))
        self.play(*self.colorear_componentes(nodos, comps), run_time=0.6)
        self.play(Transform(nota, texto("Sin (3,4): 2 componentes",
                                        22, AMARILLO).move_to(nota)),
                  run_time=0.6)

        self.esperar_hasta(MARCAS["e2_quita12"])
        self.play(FadeIn(aristas[(3, 4)]),
                  *[nodos[v][0].animate.set_stroke(VERDE).set_fill(
                      "#1E3448", opacity=1) for v in range(1, N_EJEMPLO + 1)],
                  run_time=0.5)
        self.play(FadeOut(aristas[(1, 2)]), run_time=0.5)
        self.play(Transform(nota, texto("Sin (1,2): sigue conexo (1 componente)",
                                        22, VERDE).move_to(nota)), run_time=0.6)

        self.esperar_hasta(MARCAS["e2_ciclo"])
        self.play(FadeIn(aristas[(1, 2)]), run_time=0.4)
        ciclo_izq = SurroundingRectangle(
            VGroup(nodos[1], nodos[2], nodos[3]), color=AMARILLO,
            buff=0.16, stroke_width=3)
        ciclo_der = SurroundingRectangle(
            VGroup(nodos[4], nodos[5], nodos[6]), color=AMARILLO,
            buff=0.16, stroke_width=3)
        self.play(Create(ciclo_izq), Create(ciclo_der),
                  Transform(nota, texto(
                      "Dentro de un ciclo ninguna arista es puente",
                      22, AMARILLO).move_to(nota)), run_time=0.8)
        self.cerrar_seccion()

    def escena_3(self):
        self.abrir_seccion("e3_algoritmo", TIEMPOS["e3"])
        self.limpiar_escena()
        self.cambiar_titulo(3, "El algoritmo: tin y low")

        nodos, aristas = self.crear_grafo_demo(
            escala=0.72, centro=[-3.7, 0.3, 0])
        self.play(*[Create(e) for e in aristas.values()],
                  *[FadeIn(n) for n in nodos.values()], run_time=1.2)

        lineas_codigo = [
            "def find_bridges(n, edges):",
            "    tin[v] = low[v] = t",
            "    low[v] = min(low[v], low[to])",
            "    if low[to] > tin[v]:",
            "        puentes.add((v, to))",
            "    low[v] = min(low[v], tin[to])",
        ]
        codigo = VGroup(*[texto_mono(l, 16) for l in lineas_codigo])
        codigo.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        codigo.move_to([3.7, 0.9, 0])
        nota = texto("DFS: tin y low", 22, GRIS).move_to([3.7, -1.7, 0])
        self.play(FadeIn(codigo), FadeIn(nota), run_time=1.0)

        def cursor_en(i):
            return SurroundingRectangle(codigo[i], color=AMARILLO,
                                        buff=0.06, stroke_width=2)

        cursor = cursor_en(1)
        self.play(Create(cursor), run_time=0.3)

        puentes, _, tin, low = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)

        self.esperar_hasta(MARCAS["e3_tin"])
        tin_labels = {v: texto(f"tin={tin[v]}", 13, AMARILLO).next_to(
            nodos[v], DOWN, buff=0.04) for v in range(1, N_EJEMPLO + 1)}
        self.play(*[FadeIn(t) for t in tin_labels.values()],
                  Transform(cursor, cursor_en(1)),
                  Transform(nota, texto(
                      "tin: orden en que el DFS descubre cada nodo",
                      20, AMARILLO).move_to([3.7, -1.7, 0])),
                  run_time=0.8)

        self.esperar_hasta(MARCAS["e3_low"])
        low_labels = {v: texto(f"low={low[v]}", 13, VERDE).next_to(
            nodos[v], UP, buff=0.04) for v in range(1, N_EJEMPLO + 1)}
        self.play(*[FadeIn(l) for l in low_labels.values()],
                  Transform(cursor, cursor_en(2)),
                  Transform(nota, texto(
                      "low: hasta donde puedo volver sin repetir arista",
                      20, VERDE).move_to([3.7, -1.7, 0])),
                  run_time=0.8)

        self.esperar_hasta(MARCAS["e3_retroceso"])
        inicio = nodos[3].get_center()
        fin = nodos[1].get_center()
        medio = (inicio + fin) / 2 + DOWN * 0.5
        retroceso = DashedVMobject(
            CubicBezier(inicio, medio, medio, fin, color=AMARILLO,
                        stroke_width=3),
            num_dashes=18)
        self.play(Create(retroceso), Transform(cursor, cursor_en(5)),
                  Transform(nota, texto(
                      "arista de retroceso: low[3] vuelve a 0",
                      20, AMARILLO).move_to([3.7, -1.7, 0])),
                  run_time=0.8)

        self.esperar_hasta(MARCAS["e3_condicion"])
        condicion = texto(
            f"low[4]={low[4]} > tin[3]={tin[3]} -> puente (3,4)",
            22, ROJO).move_to([3.7, -1.7, 0])
        self.play(Transform(cursor, cursor_en(3)), Transform(nota, condicion),
                  Indicate(aristas[(3, 4)], color=AMARILLO), run_time=0.8)

        self.esperar_hasta(MARCAS["e3_puente"])
        self.play(
            aristas[(3, 4)].animate.set_color(ROJO).set_stroke_width(9),
            Flash(nodos[3].get_center(), color=ROJO, flash_radius=0.5),
            run_time=0.8,
        )
        self.play(FadeOut(retroceso), run_time=0.3)
        self.cerrar_seccion()


if __name__ == "__main__":
    BridgesLesson().render()
