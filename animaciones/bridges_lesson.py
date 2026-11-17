import json
import sys
from pathlib import Path

import numpy as np
from manim import *
import manimpango

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "implementacion del codigo")
)
from bridges import EDGES_EJEMPLO, N_EJEMPLO, find_bridges, find_bridges_bruteforce

for fuente in (Path(__file__).resolve().parent.parent / "assets" / "fonts").glob("*.ttf"):
    if not manimpango.register_font(str(fuente)):
        raise RuntimeError(f"No se pudo cargar la fuente incluida: {fuente.name}")
Text.font_list.cache_clear()

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


def ajustar(objeto, ancho):
    if objeto.width > ancho:
        objeto.scale_to_fit_width(ancho)
    return objeto


FPS = 30
TIEMPOS = {"e0": 300, "e1": 750, "e2": 900, "e3": 1350,
           "e4": 900, "e5": 600, "e6": 600}
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
    "e4_inicio": 3.0,
    "e4_back31": 7.0,
    "e4_enter4": 11.0,
    "e4_back64": 15.0,
    "e4_enter7": 18.0,
    "e4_puente67": 23.0,
    "e4_puente34": 28.0,
    "e4_fin": 29.5,
    "e5_ciclo": 6.0,
    "e5_paralelas": 10.0,
    "e5_id": 15.0,
    "e6_comparacion": 6.0,
    "e6_cierre": 14.0,
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
            self.play(FadeOut(self.titulo_actual), run_time=0.2)
        self.titulo_actual = VGroup(
            texto(f"{num:02} / 06", 20, VERDE), texto(titulo, 34))
        self.titulo_actual.arrange(
            DOWN, aligned_edge=LEFT, buff=0.16).to_corner(UL, buff=0.5)
        self.play(FadeIn(self.titulo_actual, shift=RIGHT * 0.1), run_time=0.4)

    def abrir_seccion(self, nombre, fotogramas):
        self.next_section(nombre)
        self._inicio = self.time
        self._fotogramas = fotogramas

    def esperar_hasta(self, segundo):
        fotogramas = round((segundo - (self.time - self._inicio)) * FPS)
        if fotogramas > 0:
            self.wait(fotogramas / FPS)

    def mostrar_parte(self, fotogramas, *animaciones, run_time=1.0):
        inicio = self.time
        if animaciones:
            self.play(*animaciones, run_time=run_time)
        restante = fotogramas / FPS - (self.time - inicio)
        if restante > 0:
            self.wait(restante)

    def cerrar_seccion(self):
        usados = round((self.time - self._inicio) * FPS)
        if usados > self._fotogramas:
            raise RuntimeError(f"Sección excedida: {usados} > {self._fotogramas}")
        if usados < self._fotogramas:
            self.wait((self._fotogramas - usados) / FPS)

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
        self.escena_4()
        self.escena_5()
        self.escena_6()

    def escena_0(self):
        self.abrir_seccion("e0_portada", TIEMPOS["e0"])
        titulo = VGroup(
            texto("PUENTES EN GRAFOS", 58, VERDE),
            texto("Algoritmos y Estructuras de Datos", 28),
            texto("Búsqueda de puentes con DFS (Tarjan)", 22, GRIS),
        ).arrange(DOWN, buff=0.4)
        integrantes = VGroup(
            texto("Integrantes", 20, VERDE),
            texto("Juan Diego Mejía Armas", 24),
            texto("Marcelo Rosillo Rodríguez", 24),
        ).arrange(DOWN, buff=0.16)
        portada = VGroup(titulo, integrantes).arrange(DOWN, buff=0.55)

        self.mostrar_parte(75, Write(portada), run_time=1.3)
        self.mostrar_parte(150)
        self.mostrar_parte(40, FadeOut(portada), run_time=0.4)
        self.cerrar_seccion()

    def escena_1(self):
        self.abrir_seccion("e1_motivacion", TIEMPOS["e1"])
        self.cambiar_titulo(1, "Por qué importan los puentes")

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
            texto("¿Cómo saber qué aristas son críticas?", 26, AMARILLO)
            .move_to([0, -1.7, 0])), run_time=0.7)

        self.esperar_hasta(MARCAS["e1_puentes"])
        self.play(Transform(nota, texto("PUENTES", 54, AMARILLO)
                            .move_to([0, -0.9, 0])), run_time=0.8)
        self.cerrar_seccion()

    def escena_2(self):
        self.abrir_seccion("e2_concepto", TIEMPOS["e2"])
        self.limpiar_escena()
        self.cambiar_titulo(2, "Qué es un puente")

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
        self.play(Transform(nota, texto(f"Sin (3,4): {len(comps)} componentes",
                                        22, AMARILLO).move_to(nota)),
                  run_time=0.6)

        self.esperar_hasta(MARCAS["e2_quita12"])
        self.play(FadeIn(aristas[(3, 4)]),
                  *[nodos[v][0].animate.set_stroke(VERDE).set_fill(
                      "#1E3448", opacity=1) for v in range(1, N_EJEMPLO + 1)],
                  run_time=0.5)
        self.play(FadeOut(aristas[(1, 2)]), run_time=0.5)
        comps12 = componentes(N_EJEMPLO, EDGES_EJEMPLO, sin_arista=(1, 2))
        mensaje12 = (f"Sin (1,2): sigue conexo ({len(comps12)} componente)"
                     if len(comps12) == 1 else f"Sin (1,2): {len(comps12)} componentes")
        self.play(Transform(nota, texto(mensaje12,
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
        ajustar(codigo, 6.0).move_to([3.3, 0.9, 0])
        nota = texto("DFS: tin y low", 22, GRIS).move_to([3.3, -1.7, 0])
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
                  Transform(nota, ajustar(texto(
                      "tin: orden en que el DFS descubre cada nodo",
                      20, AMARILLO), 6.2).move_to([3.3, -1.7, 0])),
                  run_time=0.8)

        self.esperar_hasta(MARCAS["e3_low"])
        low_labels = {v: texto(f"low={low[v]}", 13, VERDE).next_to(
            nodos[v], UP, buff=0.04) for v in range(1, N_EJEMPLO + 1)}
        self.play(*[FadeIn(l) for l in low_labels.values()],
                  Transform(cursor, cursor_en(2)),
                  Transform(nota, ajustar(texto(
                      "low: menor tin alcanzable desde el subárbol",
                      20, VERDE), 6.2).move_to([3.3, -1.7, 0])),
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
                  Transform(nota, ajustar(texto(
                      f"arista de retroceso: low[3] vuelve a {low[3]}",
                      20, AMARILLO), 6.2).move_to([3.3, -1.7, 0])),
                  run_time=0.8)

        self.esperar_hasta(MARCAS["e3_condicion"])
        condicion = ajustar(texto(
            f"low[4]={low[4]} > tin[3]={tin[3]} -> puente (3,4)",
            22, ROJO), 6.2).move_to([3.3, -1.7, 0])
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

    def escena_4(self):
        self.abrir_seccion("e4_ejecucion", TIEMPOS["e4"])
        self.limpiar_escena()
        self.cambiar_titulo(4, "El DFS, paso a paso")
        nodos, aristas = self.crear_grafo_demo(escala=0.8, centro=[-3.2, 0.4, 0])
        puentes_final, traza, tin_final, low_final = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)

        encabezado = texto("Estado del recorrido", 24, VERDE).move_to([3.4, 2.1, 0])
        columnas = VGroup(*[
            texto(s, 20, GRIS).move_to([x, 1.6, 0])
            for s, x in (("Nodo", 2.0), ("tin", 3.4), ("low", 4.8))
        ])
        tin_v, low_v, tin_lbl, low_lbl, filas = {}, {}, {}, {}, VGroup()
        for v in range(1, N_EJEMPLO + 1):
            y = 1.13 - (v - 1) * 0.34
            tin_lbl[v] = texto("—", 19, AMARILLO).move_to([3.4, y, 0])
            low_lbl[v] = texto("—", 19, VERDE).move_to([4.8, y, 0])
            filas.add(texto(str(v), 19).move_to([2.0, y, 0]), tin_lbl[v], low_lbl[v])
        pila, encontrados = [], []
        pila_lbl = texto("Pila DFS: vacía", 18, GRIS).move_to([-3.2, -1.35, 0])
        puentes_lbl = texto("Puentes: ninguno", 18, GRIS).move_to([3.4, -1.55, 0])
        nota = texto("Comenzamos en el nodo 1", 24, AMARILLO).move_to([0, -2.05, 0])
        self.play(*[Create(e) for e in aristas.values()],
                  *[FadeIn(n) for n in nodos.values()],
                  FadeIn(encabezado), FadeIn(columnas), FadeIn(filas),
                  FadeIn(pila_lbl), FadeIn(puentes_lbl), FadeIn(nota), run_time=1.2)

        anclas = {
            ("enter", 1): MARCAS["e4_inicio"],
            ("back_edge", 3, 1): MARCAS["e4_back31"],
            ("enter", 4): MARCAS["e4_enter4"],
            ("back_edge", 6, 4): MARCAS["e4_back64"],
            ("enter", 7): MARCAS["e4_enter7"],
            ("bridge", 6, 7): MARCAS["e4_puente67"],
            ("bridge", 3, 4): MARCAS["e4_puente34"],
            ("exit", 1): MARCAS["e4_fin"],
        }
        puntos = []
        for i, ev in enumerate(traza):
            clave = ev[:2] if ev[0] in ("enter", "exit") else ev[:3]
            if clave in anclas:
                puntos.append((i, round(anclas[clave] * FPS)))
        instantes = [0] * len(traza)
        for (i, inicio), (j, fin) in zip(puntos, puntos[1:]):
            for k in range(i, j + 1):
                instantes[k] = round(inicio + (fin - inicio) * (k - i) / (j - i))

        def valor(label, numero, color):
            return Transform(label, texto(str(numero), 19, color).move_to(label))

        for i, ev in enumerate(traza):
            self.esperar_hasta(instantes[i] / FPS)
            tipo, animaciones = ev[0], []
            if tipo == "enter":
                _, v, t = ev
                tin_v[v] = low_v[v] = t
                pila.append(v)
                animaciones += [valor(tin_lbl[v], t, AMARILLO), valor(low_lbl[v], t, VERDE),
                                nodos[v][0].animate.set_stroke(AMARILLO).set_fill(AMARILLO, opacity=0.22)]
                mensaje = f"Descubrimos {v}: tin[{v}] = low[{v}] = {t}"
            elif tipo == "tree_edge":
                _, u, v = ev
                animaciones.append(aristas[tuple(sorted((u, v)))].animate.set_color(AMARILLO))
                mensaje = f"{v} no fue visitado: bajamos desde {u}"
            elif tipo == "back_edge":
                _, u, v, bajo = ev
                low_v[u] = bajo
                animaciones += [valor(low_lbl[u], bajo, VERDE),
                                Indicate(aristas[tuple(sorted((u, v)))], color=AMARILLO)]
                mensaje = f"Retroceso {u} → {v}: low[{u}] = {bajo}"
            elif tipo == "check":
                _, u, v, bajo, t, es_puente = ev
                low_v[u] = min(low_v[u], bajo)
                animaciones.append(valor(low_lbl[u], low_v[u], VERDE))
                mensaje = (f"low[{v}] = {bajo} {'>' if es_puente else '≤'} tin[{u}] = {t}"
                           + ("   →   es puente" if es_puente else "   →   hay una ruta alternativa"))
                if not es_puente:
                    animaciones.append(aristas[tuple(sorted((u, v)))].animate.set_color(VERDE))
            elif tipo == "bridge":
                _, u, v = ev
                encontrados.append(tuple(sorted((u, v))))
                animaciones.append(aristas[tuple(sorted((u, v)))].animate.set_color(ROJO).set_stroke_width(9))
                mensaje = f"Puente encontrado: ({u}, {v})"
            elif tipo == "exit":
                _, v, bajo = ev
                low_v[v] = bajo
                assert pila.pop() == v
                animaciones += [valor(low_lbl[v], bajo, VERDE),
                                nodos[v][0].animate.set_stroke(VERDE).set_fill("#1E3448", opacity=1)]
                mensaje = f"Terminamos {v}: low[{v}] = {bajo}"
            else:
                raise ValueError(f"Evento desconocido: {ev}")
            color = ROJO if tipo == "bridge" else AMARILLO
            if set(encontrados) == puentes_final:
                mensaje = "Resultado: puentes " + " y ".join(
                    f"({a},{b})" for a, b in sorted(encontrados))
                color = ROJO
            animaciones += [
                Transform(nota, ajustar(texto(mensaje, 24, color), 12.8).move_to(nota)),
                Transform(pila_lbl, ajustar(texto("Pila DFS: " + (" → ".join(map(str, pila)) or "vacía"),
                                                       18, GRIS), 6.3).move_to(pila_lbl)),
                Transform(puentes_lbl, ajustar(texto("Puentes: " + (", ".join(f"{a}-{b}" for a, b in encontrados)
                                                                       or "ninguno"), 18, ROJO if encontrados else GRIS),
                                                    5.0).move_to(puentes_lbl)),
            ]
            siguiente = instantes[i + 1] if i + 1 < len(traza) else 900
            duracion = max(1, min(9, siguiente - instantes[i])) / FPS
            self.play(*animaciones, run_time=duracion)
        assert tin_v == tin_final and low_v == low_final
        self.cerrar_seccion()

    def crear_caso(self, n, edges, posiciones, paralelas=False):
        nodos = {v: self.crear_nodo(v, posiciones[v]) for v in range(1, n + 1)}
        aristas = []
        for i, (u, v) in enumerate(edges):
            if paralelas:
                inicio = nodos[u].get_center() + RIGHT * 0.34
                fin = nodos[v].get_center() + LEFT * 0.34
                arista = ArcBetweenPoints(inicio, fin, angle=(1 if i == 0 else -1) * PI / 2,
                                         color=VERDE, stroke_width=5)
            else:
                arista = self.crear_arista(posiciones[u], posiciones[v])
            aristas.append(arista)
        puentes, _, _, _ = find_bridges(n, edges)
        return nodos, aristas, puentes

    def escena_5(self):
        self.abrir_seccion("e5_casos_especiales", TIEMPOS["e5"])
        self.limpiar_escena()
        self.cambiar_titulo(5, "Tres casos que conviene probar")
        casos = [
            (0, "Árbol", 4, [(1, 2), (2, 3), (3, 4)],
             {v: (-4.2 + (v - 1) * 2.8, 0.5, 0) for v in range(1, 5)},
             "Sin ciclos, todas las aristas son puentes", False),
            (MARCAS["e5_ciclo"], "Ciclo", 3, [(1, 2), (2, 3), (3, 1)],
             {1: (-2, -0.3, 0), 2: (0, 1.25, 0), 3: (2, -0.3, 0)},
             "Hay una ruta alternativa: ningún puente", False),
            (MARCAS["e5_paralelas"], "Aristas paralelas", 2, [(1, 2), (1, 2)],
             {1: (-1.8, 0.5, 0), 2: (1.8, 0.5, 0)},
             "Quitar una deja la otra: ningún puente", True),
        ]
        objetos = None
        for marca, nombre, n, edges, posiciones, conclusion, paralelas in casos:
            self.esperar_hasta(marca)
            if objetos is not None:
                self.play(FadeOut(objetos), run_time=0.3)
            nodos, aristas, puentes = self.crear_caso(n, edges, posiciones, paralelas)
            rotulo = texto(nombre, 30, VERDE).move_to([0, 2.0, 0])
            nota = texto(conclusion, 25, AMARILLO).move_to([0, -1.4, 0])
            resultado = texto(f"Puentes calculados: {len(puentes)}", 21, GRIS).move_to([0, -1.95, 0])
            objetos = VGroup(*aristas, *nodos.values(), rotulo, nota, resultado)
            if paralelas:
                objetos.add(texto("id 0", 18, GRIS).move_to([0, 1.5, 0]),
                            texto("id 1", 18, GRIS).move_to([0, -0.5, 0]))
            self.play(FadeIn(objetos), run_time=0.7)
            cambios = [e.animate.set_color(ROJO).set_stroke_width(8)
                       for e, (u, v) in zip(aristas, edges) if tuple(sorted((u, v))) in puentes]
            if cambios:
                self.play(*cambios, run_time=0.5)
        self.esperar_hasta(MARCAS["e5_id"])
        regla = ajustar(texto("En el DFS se ignora la arista de llegada por su id", 24, AMARILLO), 12)
        regla.move_to([0, -1.4, 0])
        self.play(Transform(nota, regla), run_time=0.5)
        self.cerrar_seccion()

    def escena_6(self):
        self.abrir_seccion("e6_complejidad_cierre", TIEMPOS["e6"])
        self.limpiar_escena()
        self.cambiar_titulo(6, "Complejidad y conclusión")
        formula = texto("O(|V| + |E|)", 48, VERDE).move_to([0, 1.75, 0])
        explicacion = texto("Cada nodo se visita una vez; cada arista se revisa dos veces", 24)
        explicacion.move_to([0, 0.55, 0])
        memoria = texto("Espacio: O(|V| + |E|) para adyacencias y DFS", 22, GRIS)
        memoria.move_to([0, -0.35, 0])
        self.play(Write(formula), FadeIn(explicacion), FadeIn(memoria), run_time=1.0)

        self.esperar_hasta(MARCAS["e6_comparacion"])
        self.play(FadeOut(explicacion), FadeOut(memoria), run_time=0.3)
        edges = [(v, v + 1) for v in range(1, 25)]
        dfs_stats, brute_stats = {}, {}
        puentes = find_bridges(25, edges, stats=dfs_stats)[0]
        assert puentes == find_bridges_bruteforce(25, edges, stats=brute_stats)
        subtitulo = texto("Medición real: cadena de 25 nodos y 24 aristas", 22, GRIS)
        subtitulo.move_to([0, 0.95, 0])
        comparacion = VGroup(subtitulo)
        maximo = brute_stats["revisiones"]
        barras = []
        for nombre, cantidad, y, color in (("DFS", dfs_stats["revisiones"], 0.05, VERDE),
                                           ("Fuerza bruta", maximo, -0.8, AMARILLO)):
            barra = Rectangle(width=7.0 * cantidad / maximo, height=0.32,
                              fill_color=color, fill_opacity=1, stroke_width=0)
            barra.move_to([-3.6 + barra.width / 2, y, 0])
            etiqueta = texto(nombre, 20, color).move_to([-5.1, y, 0])
            valor = texto(f"{cantidad} revisiones", 19, color).next_to(barra, RIGHT, buff=0.2)
            comparacion.add(barra, etiqueta, valor)
            barras.append(barra)
        costo_bruto = texto("Fuerza bruta: O(|E| · (|V| + |E|))", 23, AMARILLO)
        costo_bruto.move_to([0, -1.75, 0])
        comparacion.add(costo_bruto)
        self.play(FadeIn(comparacion), run_time=0.8)

        self.esperar_hasta(MARCAS["e6_cierre"])
        self.play(FadeOut(comparacion), FadeOut(formula), run_time=0.4)
        cierre = self.crear_cierre()
        self.play(FadeIn(cierre, shift=UP * 0.1), run_time=0.8)
        self.cerrar_seccion()

    def crear_cierre(self):
        return VGroup(
            texto("Una ruta alternativa marca la diferencia", 34, VERDE),
            texto("low[v] > tin[u]  →  la arista (u,v) es un puente", 26, AMARILLO),
            texto("CS2023 · Algoritmos y Estructuras de Datos", 20, GRIS),
        ).arrange(DOWN, buff=0.4).move_to([0, 0.3, 0])


if __name__ == "__main__":
    BridgesLesson().render()
