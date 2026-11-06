# Esto es lo que hicimos para el algoritmo de puentes.
# La idea es del apunte de clase: hacemos un DFS y vamos guardando
# tin (cuando alguien te descubre) y low (hasta donde puedes volver).
# Al final, si low[hijo] > tin[padre], esa arista es un puente.
# No usamos networkx ni nada externo, solo Python pelado, como pide el enunciado.

import sys

# por las dudas subimos el limite de recursion, con la demo alcanza
sys.setrecursionlimit(10000)

# el grafo que viene en la guia, lo usamos para probar y para la animacion
N_EJEMPLO = 7
EDGES_EJEMPLO = [(1, 2), (2, 3), (3, 1), (3, 4),
                 (4, 5), (5, 6), (6, 4), (6, 7)]


def find_bridges(n, edges):
    # n es la cantidad de nodos (los numeramos desde 1)
    # edges es una lista de pares, puede tener aristas repetidas
    # devuelve (puentes, traza, tin, low) y eso mismo usamos despues para animar
    #
    # guardamos la adyacencia con el id de la arista porque ahi estaba
    # el truco de las aristas paralelas: si entre 1 y 2 hay dos aristas,
    # no podes ignorar "al padre 1" a secas, tenes que ignorar solo la
    # arista por la que llegaste (por su id)
    adyacencia = [[] for _ in range(n + 1)]
    for id_arista, (u, v) in enumerate(edges):
        adyacencia[u].append((v, id_arista))
        adyacencia[v].append((u, id_arista))

    # ordenamos para que el ejemplo de la guia de los tin/low exactos que dice
    for lista in adyacencia:
        lista.sort(key=lambda par: (par[0], par[1]))

    tin = {}
    low = {}
    puentes = set()
    traza = []  # aca vamos anotando todo para despues mostrarlo en Manim
    reloj = [0]  # lo puse en una lista porque si no python se quejaba adentro de dfs

    def dfs(v, arista_padre):
        # cuando entramos a un nodo nuevo, tin y low arrancan iguales
        tin[v] = low[v] = reloj[0]
        reloj[0] += 1
        traza.append(("enter", v, tin[v]))

        for vecino, id_arista in adyacencia[v]:
            # esta es la arista por la que llegamos, la salteamos
            if id_arista == arista_padre:
                continue

            if vecino in tin:
                # si ya lo vimos, es una arista de retroceso, achicamos low
                low[v] = min(low[v], tin[vecino])
                traza.append(("back_edge", v, vecino, low[v]))
            else:
                # si no lo vimos, bajamos por aca (arista del arbol DFS)
                traza.append(("tree_edge", v, vecino))
                dfs(vecino, id_arista)
                # ya volvimos de vecino, actualizamos low y vemos si es puente
                low[v] = min(low[v], low[vecino])
                es_puente = low[vecino] > tin[v]
                traza.append(("check", v, vecino, low[vecino], tin[v], es_puente))
                if es_puente:
                    puentes.add((min(v, vecino), max(v, vecino)))
                    traza.append(("bridge", v, vecino))

        traza.append(("exit", v, low[v]))

    # si el grafo tiene varias partes sueltas, arrancamos un DFS por cada una
    for v in range(1, n + 1):
        if v not in tin:
            dfs(v, -1)

    return puentes, traza, tin, low


if __name__ == "__main__":
    # para probar rapido con: python bridges.py
    p, t, tin, low = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)
    print("puentes:", sorted(p))
    print("tin:", tin)
    print("low:", low)
    print("eventos en la traza:", len(t))
