"""Pruebas de find_bridges."""

import unittest
from itertools import combinations

from bridges import EDGES_EJEMPLO, N_EJEMPLO, find_bridges, find_bridges_bruteforce


class TestPuentes(unittest.TestCase):

    def test_ejemplo_guia(self):
        puentes, traza, tin, low = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)
        self.assertEqual(puentes, {(3, 4), (6, 7)})
        self.assertEqual(tin, {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6})
        self.assertEqual(low, {1: 0, 2: 0, 3: 0, 4: 3, 5: 3, 6: 3, 7: 6})
        self.assertEqual([ev[1] for ev in traza if ev[0] == "enter"],
                         [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual({(ev[1], ev[2]) for ev in traza if ev[0] == "bridge"},
                         {(3, 4), (6, 7)})

    def test_arbol_todo_es_puente(self):
        puentes, _, _, _ = find_bridges(4, [(1, 2), (2, 3), (3, 4)])
        self.assertEqual(puentes, {(1, 2), (2, 3), (3, 4)})

    def test_ciclo_sin_puentes(self):
        puentes, _, _, _ = find_bridges(3, [(1, 2), (2, 3), (3, 1)])
        self.assertEqual(puentes, set())

    def test_aristas_paralelas(self):
        puentes, _, _, _ = find_bridges(2, [(1, 2), (1, 2)])
        self.assertEqual(puentes, set())

    def test_grafo_sin_aristas(self):
        puentes, _, tin, low = find_bridges(3, [])
        self.assertEqual(puentes, set())
        self.assertEqual(tin, {1: 0, 2: 1, 3: 2})
        self.assertEqual(low, {1: 0, 2: 1, 3: 2})

    def test_un_solo_nodo(self):
        puentes, _, tin, low = find_bridges(1, [])
        self.assertEqual(puentes, set())
        self.assertEqual(tin, {1: 0})
        self.assertEqual(low, {1: 0})

    def test_grafo_no_conexo(self):
        puentes, _, _, _ = find_bridges(5, [(1, 2), (3, 4), (4, 5), (5, 3)])
        self.assertEqual(puentes, {(1, 2)})

    def test_todos_los_grafos_simples_hasta_cinco_nodos(self):
        for n in range(1, 6):
            posibles = list(combinations(range(1, n + 1), 2))
            for mascara in range(1 << len(posibles)):
                edges = [e for i, e in enumerate(posibles) if mascara & (1 << i)]
                self.assertEqual(find_bridges(n, edges)[0],
                                 find_bridges_bruteforce(n, edges), (n, edges))

    def test_bucles_y_paralelas_con_puente(self):
        edges = [(1, 1), (1, 2), (1, 2), (2, 3), (3, 3)]
        self.assertEqual(find_bridges(3, edges)[0], {(2, 3)})
        self.assertEqual(find_bridges_bruteforce(3, edges), {(2, 3)})

    def test_mediciones_de_la_comparacion(self):
        edges = [(v, v + 1) for v in range(1, 25)]
        dfs_stats, brute_stats = {}, {}
        self.assertEqual(find_bridges(25, edges, stats=dfs_stats)[0],
                         find_bridges_bruteforce(25, edges, stats=brute_stats))
        self.assertEqual(dfs_stats, {"vertices": 25, "revisiones": 48})
        self.assertEqual(brute_stats["revisiones"], 48 * 25)


if __name__ == "__main__":
    unittest.main()
