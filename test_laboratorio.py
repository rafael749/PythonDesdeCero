"""Comprueba que el laboratorio usa los resultados de los ejercicios."""

import builtins
import sys
import unittest

from servidor import codigo_original, ejecutar


class LaboratorioTests(unittest.TestCase):
    """Verifica resultados, trazas y reglas de las cuatro actividades."""

    def test_reemplazo_y_traza(self):
        response = ejecutar({"exercise": 1, "phrases": "Mate mate\nMate", "word": "Mate", "replacement": "cafe"})
        self.assertEqual(response["result"], {"original": ["Mate mate", "Mate"], "new": ["cafe mate", "cafe"]})
        snapshots = [step["variables"]["nueva_lista"] for step in response["steps"] if "nueva_lista" in step["variables"]]
        self.assertIn("[]", snapshots)
        self.assertEqual(snapshots[-1], "['cafe mate', 'cafe']")

    def test_email(self):
        for email, expected in [("juan@gmail.com", True), ("maria.lopez@utn.edu.ar", True),
                                ("usuario@@gmail.com", False), ("@gmail.com", False),
                                ("juan@.com", False), ("juan@gmail.c", False),
                                ("juan\t@gmail.com", False), ("", False)]:
            with self.subTest(email=email):
                self.assertIs(ejecutar({"exercise": 2, "email": email})["result"], expected)

    def test_numeros(self):
        result = ejecutar({"exercise": 3, "numbers": "4, 7, 2, 9, 1, 5, 8, 3, 6"})["result"]
        self.assertEqual(result["largest"], 9)
        self.assertEqual(result["smallest"], 1)
        self.assertEqual(result["sorted"], list(range(1, 10)))
        self.assertEqual(result["filtered"], [7, 9, 8, 6])
        result = ejecutar({"exercise": 3, "numbers": "-2 -2 0"})["result"]
        self.assertEqual(result["sorted"], [-2, -2, 0])
        for invalid in ("", "1, hola", "1.5", "1 " * 26, "1000000000001"):
            with self.assertRaises(ValueError):
                ejecutar({"exercise": 3, "numbers": invalid})

    def test_juego(self):
        initial_input = builtins.input
        initial_trace = sys.gettrace()
        waiting = ejecutar({"exercise": 4, "secret": "python", "guesses": []})
        self.assertEqual(waiting["steps"][-1]["event"], "input")
        result = ejecutar({"exercise": 4, "secret": "python", "guesses": ["P", "p", "12", "", "a"]})["result"]
        self.assertEqual(result["progress"], "p _ _ _ _ _")
        self.assertEqual(result["errors"], 1)
        self.assertEqual(result["letters"], ["p", "a"])
        self.assertFalse(result["finished"])
        self.assertIs(builtins.input, initial_input)
        self.assertIs(sys.gettrace(), initial_trace)
        victory = ejecutar({"exercise": 4, "secret": "python", "guesses": list("python")})["result"]
        self.assertTrue(victory["won"])
        self.assertTrue(victory["finished"])
        defeat = ejecutar({"exercise": 4, "secret": "python", "guesses": list("abcde")})
        self.assertTrue(defeat["result"]["finished"])
        self.assertEqual(defeat["result"]["errors"], 5)
        self.assertIn("Perdiste", defeat["output"])

    def test_codigo(self):
        sources = codigo_original()
        self.assertEqual(len(sources), 5)
        self.assertTrue(any("def buscar_reemplazar" in line["text"] for line in sources["ejercicio_01.py"]))


if __name__ == "__main__":
    unittest.main()