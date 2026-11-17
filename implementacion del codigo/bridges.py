"""Puentes en un grafo no dirigido (DFS de Tarjan)."""

import sys

sys.setrecursionlimit(10000)

N_EJEMPLO = 7
EDGES_EJEMPLO = [(1, 2), (2, 3), (3, 1), (3, 4),
                 (4, 5), (5, 6), (6, 4), (6, 7)]


def find_bridges(n, edges, *, stats=None):
    """Devuelve (puentes, traza, tin, low)."""
    if stats is not None:
        stats.clear()
        stats.update(vertices=0, revisiones=0)
    # (vecino, id_arista): el id distingue aristas paralelas.
    adyacencia = [[] for _ in range(n + 1)]
    for id_arista, (u, v) in enumerate(edges):
        adyacencia[u].append((v, id_arista))
        adyacencia[v].append((u, id_arista))

    tin = {}
    low = {}
    puentes = set()
    traza = []
    reloj = [0]

    def dfs(v, arista_padre):
        if stats is not None:
            stats["vertices"] += 1
        tin[v] = low[v] = reloj[0]
        reloj[0] += 1
        traza.append(("enter", v, tin[v]))

        for vecino, id_arista in adyacencia[v]:
            if stats is not None:
                stats["revisiones"] += 1
            if id_arista == arista_padre:
                continue
            if vecino in tin:
                low[v] = min(low[v], tin[vecino])
                if tin[vecino] < tin[v]:
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


def find_bridges_bruteforce(n, edges, *, stats=None):
    if stats is not None:
        stats.clear()
        stats.update(vertices=0, revisiones=0)
    ady = [[] for _ in range(n + 1)]
    for eid, (u, v) in enumerate(edges):
        ady[u].append((v, eid))
        ady[v].append((u, eid))

    def contar_componentes(excluir=-1):
        vistos = set()
        cantidad = 0
        for inicio in range(1, n + 1):
            if inicio in vistos:
                continue
            cantidad += 1
            vistos.add(inicio)
            pila = [inicio]
            while pila:
                v = pila.pop()
                if stats is not None:
                    stats["vertices"] += 1
                for vecino, eid in ady[v]:
                    if stats is not None:
                        stats["revisiones"] += 1
                    if eid != excluir and vecino not in vistos:
                        vistos.add(vecino)
                        pila.append(vecino)
        return cantidad

    inicial = contar_componentes()
    return {
        (min(u, v), max(u, v))
        for eid, (u, v) in enumerate(edges)
        if contar_componentes(eid) > inicial
    }


if __name__ == "__main__":
    puentes, traza, tin, low = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)
    print("puentes:", sorted(puentes))
    print("tin:", tin)
    print("low:", low)
    print("eventos:", len(traza))
