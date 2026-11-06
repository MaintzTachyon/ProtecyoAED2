# Hola, estas son nuestras pruebas del algoritmo de puentes.
# Las hicimos para estar tranquilos de que el find_bridges funciona
# antes de meternos con la animacion.
#
# Se corren con:
#   cd "implementacion del codigo"
#   ../.venv/bin/python -m unittest test_bridges -v

import unittest

from bridges import EDGES_EJEMPLO, N_EJEMPLO, find_bridges


class TestPuentes(unittest.TestCase):

    def test_ejemplo_guia(self):
        # el ejemplo de la guia, el de 7 nodos y 8 aristas
        puentes, traza, tin, low = find_bridges(N_EJEMPLO, EDGES_EJEMPLO)
        # los unicos puentes que tiene que ser son (3,4) y (6,7)
        self.assertEqual(puentes, {(3, 4), (6, 7)})
        # estos tin/low son los que dice la guia, si cambian es porque rompimos algo
        self.assertEqual(tin, {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6})
        self.assertEqual(low, {1: 0, 2: 0, 3: 0, 4: 3, 5: 3, 6: 3, 7: 6})
        # tambien chequeamos que la traza anote los nodos en orden y los puentes
        self.assertEqual([ev[1] for ev in traza if ev[0] == "enter"],
                         [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual({(ev[1], ev[2]) for ev in traza
                          if ev[0] == "bridge"}, {(3, 4), (6, 7)})

    def test_arbol_todo_es_puente(self):
        # si es un arbol (tipo una cadenita 1-2-3-4) todas las aristas cortan
        puentes, _, _, _ = find_bridges(4, [(1, 2), (2, 3), (3, 4)])
        self.assertEqual(puentes, {(1, 2), (2, 3), (3, 4)})

    def test_ciclo_sin_puentes(self):
        # un triangulo, si sacas una arista igual queda todo conectado
        puentes, _, _, _ = find_bridges(3, [(1, 2), (2, 3), (3, 1)])
        self.assertEqual(puentes, set())

    def test_aristas_paralelas(self):
        # aca estaba el error que comentamos en bridges.py:
        # entre 1 y 2 hay dos aristas, ninguna es puente
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
        # un pedacito 1-2 (que si es puente) y un triangulo aparte 3-4-5
        puentes, _, _, _ = find_bridges(5, [(1, 2), (3, 4), (4, 5), (5, 3)])
        self.assertEqual(puentes, {(1, 2)})


if __name__ == "__main__":
    unittest.main()
