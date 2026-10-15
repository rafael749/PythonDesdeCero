"""Prueba el corrector con codigo controlado, no con entradas externas."""

import unittest
import inspect
import json

import ejercicio_01
import ejercicio_02
import ejercicio_03
import ejercicio_04
import juego
from curso import LESSONS

from practica_motor import evaluar


class MotorTests(unittest.TestCase):
    """Comprueba correcciones, errores y archivos virtuales."""

    def test_run_input_and_error(self):
        response = evaluar({"mode": "run", "files": {"solucion.py": "edad = int(input())\nprint(edad + 1)"}, "inputs": ["20"]})
        self.assertEqual(response["output"], "21\n")
        self.assertEqual(response["variables"]["edad"], "20")
        response = evaluar({"mode": "run", "files": {"solucion.py": "print(nombre)"}})
        self.assertEqual(response["error"]["type"], "NameError")
        self.assertEqual(response["error"]["line"], 1)

    def test_cases_are_independent(self):
        lesson = {"cases": [{"kind": "function", "title": "Duplicar", "call": {"function": "doble", "args": [number]},
                              "expected": number * 2, "why": "El resultado debe ser el doble."} for number in [2, -3, 0]]}
        response = evaluar({"lesson": lesson, "files": {"solucion.py": "def doble(numero):\n    return numero * 2"}})
        self.assertTrue(response["passed"])
        response = evaluar({"lesson": lesson, "files": {"solucion.py": "def doble(numero):\n    print(numero * 2)"}})
        self.assertFalse(response["passed"])
        self.assertEqual(response["checks"][0]["actual"], "None")

    def test_virtual_module(self):
        response = evaluar({"mode": "run", "files": {"solucion.py": "from juego import saludo\nprint(saludo())", "juego.py": "def saludo():\n    return 'hola'"}})
        self.assertEqual(response["output"], "hola\n")

    def test_limits_and_syntax(self):
        response = evaluar({"mode": "run", "files": {"solucion.py": "print('a' * 9000)"}})
        self.assertEqual(response["error"]["type"], "RuntimeError")
        response = evaluar({"lesson": {"cases": []}, "files": {"solucion.py": "if True\n print(1)"}})
        self.assertEqual(response["error"]["type"], "SyntaxError")

    def test_course_reference_solutions(self):
        solutions = [
            'print("Hola Python")',
            'nombre = "Ana"\nprint("Hola", nombre)',
            'edad = 20\nprint(edad)',
            'precio = 150\ncantidad = 3\ntotal = precio * cantidad\nprint(total)',
            'numero = 7\nresto = numero % 2\nprint(resto)',
            'nombre = input()\nprint("Hola", nombre)',
            'edad = int(input())\nprint(edad + 5)',
            'print(int(input()) >= 18)',
            'nota = int(input())\nif nota >= 6:\n    print("Aprobado")\nelse:\n    print("A recuperar")',
            'numero = int(input())\nif numero > 0:\n    print("positivo")\nelif numero < 0:\n    print("negativo")\nelse:\n    print("cero")',
            'numero = int(input())\nprint(1 <= numero <= 10)',
            'print(len(input()))',
            'print(input().lower())',
            'print(input().count("@"))',
            'frase = "gato y gato"\nnueva = frase.replace("gato", "perro")\nprint(nueva)',
            'usuario, dominio = input().split("@")\nprint(usuario)\nprint(dominio)',
            'numeros = [4, 7, 2]\nprimero = numeros[0]\nultimo = numeros[-1]\nprint(primero)\nprint(ultimo)',
            'letras = ["a", "b"]\nletras.append("c")\nprint(letras)',
            'for numero in [3, 1, 4]:\n    print(numero)',
            'total = 0\nfor numero in [4, 7, 2]:\n    total += numero\nprint(total)',
            'mayores = []\nfor numero in [4, 7, 2, 9, 5, 8]:\n    if numero > 5:\n        mayores.append(numero)\nprint(mayores)',
            'numeros = [-4, -7, -2]\nmayor = menor = numeros[0]\nfor numero in numeros:\n    if numero > mayor:\n        mayor = numero\n    if numero < menor:\n        menor = numero\nprint(mayor)\nprint(menor)',
            'numeros = [8, 2]\nnumeros[0], numeros[1] = numeros[1], numeros[0]\nprint(numeros)',
            inspect.getsource(ejercicio_03.ordenar_lista) + '\nnumeros = [4, 1, 3, 2]\nordenados = ordenar_lista(numeros)\nprint(ordenados)',
            'contador = 1\nwhile contador <= 3:\n    print(contador)\n    contador += 1',
            'respuesta = input()\nwhile respuesta != "si":\n    respuesta = input()\nprint("Listo")',
            'for numero in [2, 0, 3, 0, 1]:\n    if numero == 0:\n        continue\n    print(numero)',
            'def doble(numero):\n    return numero * 2',
            'def es_letra(texto):\n    return len(texto) == 1 and texto.isalpha()',
            'def duplicar_lista(numeros):\n    return [numero * 2 for numero in numeros]',
            inspect.getsource(juego.mostrar_progreso),
            'from juego import mostrar_progreso, palabra_completa',
            inspect.getsource(ejercicio_01.buscar_reemplazar),
            inspect.getsource(ejercicio_02.validar_email),
            '\n'.join(inspect.getsource(function) for function in [ejercicio_03.calcular_extremos, ejercicio_03.ordenar_lista, ejercicio_03.filtrar_mayores_a_cinco]),
            'from juego import mostrar_progreso, palabra_completa\n' + inspect.getsource(ejercicio_04.jugar_adivinanza),
        ]
        self.assertEqual(len(solutions), len(LESSONS))
        for lesson, solution in zip(LESSONS, solutions):
            with self.subTest(lesson=lesson["title"]):
                files = {"solucion.py": solution}
                if "juego.py" in lesson["files"]:
                    files["juego.py"] = inspect.getsource(juego)
                request = json.loads(json.dumps({"lesson": lesson, "files": files}))
                response = evaluar(request)
                self.assertTrue(response["passed"], response)

    def test_incorrect_results_and_original_list(self):
        lesson = json.loads(json.dumps(LESSONS[32]))
        files = {"solucion.py": "def buscar_reemplazar(lista, palabra, reemplazo):\n    for posicion in range(len(lista)):\n        lista[posicion] = lista[posicion].replace(palabra, reemplazo)\n    return lista"}
        self.assertFalse(evaluar({"lesson": lesson, "files": files})["passed"])
        for lesson in LESSONS:
            with self.subTest(lesson=lesson["id"]):
                response = evaluar(json.loads(json.dumps({"lesson": lesson, "files": lesson["files"]})))
                self.assertFalse(response["passed"])


if __name__ == "__main__":
    unittest.main()