"""Ejecuta practicas en Pyodide y explica resultados observables."""

import ast
import builtins
import contextlib
import copy
import io
import json
import traceback
import types


class SalidaLimitada(io.StringIO):
    """Limita la salida para evitar saturar la interfaz."""

    def write(self, text):
        if self.tell() + len(text) > 8000:
            raise RuntimeError("La salida supera 8000 caracteres. Revisa cuantas veces imprimes.")
        return super().write(text)


def explicar_error(error):
    """Traduce errores comunes conservando su mensaje y ubicacion."""
    explanations = {
        "SyntaxError": "Python no pudo leer la instruccion. Revisa comillas, parentesis y los dos puntos al iniciar un bloque.",
        "IndentationError": "La sangria indica que instrucciones pertenecen a un bloque. Usa cuatro espacios dentro de if, for, while o def.",
        "TabError": "Se mezclaron tabulaciones y espacios. Usa cuatro espacios para la sangria.",
        "NameError": "Se uso un nombre que aun no existe. Revisa su escritura y que se haya definido antes de usarlo.",
        "TypeError": "Una operacion recibio un tipo de dato que no admite. input() devuelve texto; int() lo convierte a entero.",
        "ValueError": "El tipo es aceptable, pero el contenido no sirve para esta operacion. Por ejemplo, int('hola') no es un numero.",
        "IndexError": "La posicion no existe en la lista o el texto. La primera posicion es 0 y la ultima es len(datos) - 1.",
        "ZeroDivisionError": "No se puede dividir por cero. Comprueba el divisor antes de dividir.",
        "AttributeError": "Ese dato no tiene el metodo o atributo pedido. Revisa su tipo: append() es de listas, no de strings.",
        "EOFError": "Tu programa pidio mas datos con input() de los disponibles. Agrega una respuesta por linea en Entradas.",
        "ModuleNotFoundError": "No se encontro el modulo importado. En la practica final, completa tambien el archivo juego.py.",
        "AssertionError": "Una comprobacion de tu programa no se cumplio.",
    }
    name = type(error).__name__
    filename = getattr(error, "filename", None)
    line = getattr(error, "lineno", None)
    for frame in traceback.extract_tb(error.__traceback__):
        if frame.filename in ("solucion.py", "juego.py"):
            filename, line = frame.filename, frame.lineno
    return {"type": name, "message": str(error), "file": filename, "line": line,
            "explanation": explanations.get(name, "La ejecucion se detuvo. El mensaje original indica la causa; revisa la instruccion marcada.")}


def ejecutar_codigo(files, inputs, call=None):
    """Ejecuta archivos virtuales y devuelve salida, variables y retorno."""
    output = SalidaLimitada()
    pending = iter(inputs)
    modules = {}

    def read_input(prompt=""):
        output.write(str(prompt))
        try:
            return str(next(pending))
        except StopIteration:
            raise EOFError("No quedan entradas disponibles para input().") from None

    def import_module(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "juego" and "juego.py" in files:
            if name not in modules:
                module = types.ModuleType(name)
                module.__dict__["__builtins__"] = environment
                modules[name] = module
                exec(compile(files["juego.py"], "juego.py", "exec"), module.__dict__)
            return modules[name]
        return builtins.__import__(name, globals, locals, fromlist, level)

    environment = dict(vars(builtins), input=read_input, __import__=import_module)
    namespace = {"__name__": "__main__" if call is None else "practica", "__builtins__": environment}
    result = None
    arguments = copy.deepcopy(call.get("args", [])) if call else []
    error = None
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        try:
            exec(compile(files.get("solucion.py", ""), "solucion.py", "exec"), namespace)
            if call:
                function = namespace.get(call["function"])
                if not callable(function):
                    raise NameError(f"Falta definir la funcion {call['function']}.")
                result = function(*arguments)
        except BaseException as caught:
            error = explicar_error(caught)
    return {"output": output.getvalue(), "namespace": namespace, "result": result,
            "arguments": arguments, "error": error}


def revisar_estructura(files, rules):
    """Comprueba solamente las restricciones expresas de la consigna."""
    tree = ast.parse(files.get("solucion.py", ""))
    checks = []
    for rule in rules:
        if rule["kind"] == "node":
            passed = any(type(node).__name__ == rule["name"] for node in ast.walk(tree))
        elif rule["kind"] == "forbid":
            names = set(rule["names"])
            passed = not any((isinstance(node, ast.Name) and node.id in names) or
                             (isinstance(node, ast.Attribute) and node.attr in names) for node in ast.walk(tree))
        elif rule["kind"] == "module":
            module_tree = ast.parse(files.get("juego.py", ""))
            functions = [node for node in module_tree.body if isinstance(node, ast.FunctionDef)]
            imported = any(isinstance(node, ast.ImportFrom) and node.module == "juego" for node in ast.walk(tree))
            passed = imported and all(any(node.name == name and ast.get_docstring(node) and
                                         len(ast.get_docstring(node).splitlines()) == 1 for node in functions)
                                      for name in rule["names"])
        else:
            raise ValueError("Regla desconocida.")
        checks.append({"title": rule["title"], "passed": passed,
                       "explanation": rule["why"], "expected": rule["title"],
                       "actual": "Se cumple" if passed else "Todavia no se cumple"})
    return checks


def evaluar(request):
    """Ejecuta o valida una solucion con casos independientes y explicados."""
    files = request["files"]
    if request.get("mode") == "run":
        execution = ejecutar_codigo(files, request.get("inputs", []))
        variables = {name: repr(value)[:500] for name, value in execution["namespace"].items()
                     if not name.startswith("__") and isinstance(value, (str, int, float, bool, list, tuple, dict, type(None)))}
        return {"output": execution["output"], "variables": variables, "error": execution["error"], "checks": []}
    lesson = request["lesson"]
    checks = []
    try:
        checks.extend(revisar_estructura(files, lesson.get("rules", [])))
    except (SyntaxError, IndentationError) as error:
        return {"output": "", "error": explicar_error(error), "checks": [], "passed": False}
    last_output = ""
    for case in lesson["cases"]:
        execution = ejecutar_codigo(files, case.get("inputs", []), case.get("call"))
        last_output = execution["output"]
        if execution["error"]:
            checks.append({"title": case["title"], "passed": False, "expected": repr(case.get("expected")),
                           "actual": execution["error"]["message"], "explanation": case["why"], "error": execution["error"]})
            continue
        kind = case["kind"]
        if kind == "output":
            actual = last_output.strip()
        elif kind == "variable":
            actual = execution["namespace"].get(case["name"])
        elif kind == "function":
            actual = execution["result"]
        elif kind == "game":
            normalized = last_output.lower()
            actual = {"won": "ganaste" in normalized, "lost": "perdiste" in normalized}
        else:
            raise ValueError("Caso desconocido.")
        expected = case["expected"]
        if case.get("expectedType") == "tuple":
            expected = tuple(expected)
        passed = actual == expected and type(actual) is type(expected)
        if case.get("unchanged"):
            passed = passed and execution["arguments"] == case["call"]["args"]
        checks.append({"title": case["title"], "passed": passed, "expected": repr(expected), "actual": repr(actual),
                       "explanation": case["why"] + (" Los argumentos originales deben quedar intactos." if case.get("unchanged") else "")})
        if kind == "game":
            secret = case["call"]["args"][0].lower()
            attempted = []
            progresses = [" ".join("_" for letter in secret)]
            errors = 0
            for entry in case["inputs"]:
                letter = entry.lower()
                if len(letter) != 1 or not letter.isalpha() or letter in attempted:
                    continue
                attempted.append(letter)
                errors += int(letter not in secret)
                progresses.append(" ".join(letter if letter in attempted else "_" for letter in secret))
                if errors == 5 or all(letter in attempted for letter in secret):
                    break
            missing = [progress for progress in progresses if progress not in last_output]
            checks.append({"title": case["title"] + ": progreso visible", "passed": not missing,
                           "expected": repr(progresses), "actual": last_output,
                           "explanation": "El progreso inicial y los estados de la palabra deben mostrarse, incluyendo el estado final."})
            if not expected["won"]:
                checks.append({"title": "Revelar la palabra al perder", "passed": secret in last_output.lower(),
                               "expected": secret, "actual": last_output,
                               "explanation": "La derrota debe informar cual era la palabra secreta."})
    return {"output": last_output, "error": None, "checks": checks,
            "passed": bool(checks) and all(check["passed"] for check in checks)}