"""Puentes en un grafo no dirigido (DFS de Tarjan)."""

import sys

sys.setrecursionlimit(10000)

N_EJEMPLO = 7
EDGES_EJEMPLO = [(1, 2), (2, 3), (3, 1), (3, 4),
                 (4, 5), (5, 6), (6, 4), (6, 7)]


def find_bridges(n, edges):
    """Devuelve (puentes, traza, tin, low)."""
    # (vecino, id_arista): el id distingue aristas paralelas.
    adyacencia = [[] for _ in range(n + 1)]
    for id_arista, (u, v) in enumerate(edges):
        adyacencia[u].append((v, id_arista))
        adyacencia[v].append((u, id_arista))
    for lista in adyacencia:
        lista.sort()

    tin = {}
    low = {}
    puentes = set()
    traza = []
    reloj = [0]

    def dfs(v, arista_padre):
        tin[v] = low[v] = reloj[0]
        reloj[0] += 1
        traza.append(("enter", v, tin[v]))

        for vecino, id_arista in adyacencia[v]:
            if id_arista == arista_padre:
                continue
            if vecino in tin:
                low[v] = min(low[v], tin[vecino])
                traza.append(("back_edge", v, vecino, low[v]))
            else:
                traza.append(("tree_edge", v, vecino))
                dfs(vecino, id_arista)
                low[v] = min(low[v], low[vecino])
                es_puente = low[vecino] > tin[v]
                traza.append(("check", v, vecino, low[vecino], tin[v], es_puente))
                if es_puente:
                    puentes.add((min(v, vecino), max(v, vecino)))
                    traza.append(("bridge", v, vecino))

        traza.append(("exit", v, low[v]))

    # Arranca un DFS por cada componente.
    for v in range(1, n + 1):
        if v not in tin:
            dfs(v, -1)

    return puentes, traza, tin, low


if __name__ == "__main__":
    puentes, traza, tin, low = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)
    print("puentes:", sorted(puentes))
    print("tin:", tin)
    print("low:", low)
    print("eventos:", len(traza))
