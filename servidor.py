"""Sirve el laboratorio visual y ejecuta los ejercicios originales."""

import argparse
import builtins
import contextlib
import inspect
import io
import json
from pathlib import Path
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import ejercicio_01
import ejercicio_02
import ejercicio_03
import ejercicio_04
import juego
from curso import LESSONS


ROOT = Path(__file__).resolve().parent
MODULES = [ejercicio_01, ejercicio_02, ejercicio_03, ejercicio_04, juego]
FILES = {str(Path(module.__file__).resolve()) for module in MODULES}


class EsperandoLetra(Exception):
    """Interrumpe una partida cuando necesita otra entrada del navegador."""


def codigo_original():
    """Devuelve las funciones originales con sus numeros de linea."""
    sources = {}
    for module in MODULES:
        lines = []
        for function in vars(module).values():
            if inspect.isfunction(function) and function.__module__ == module.__name__:
                source, first = inspect.getsourcelines(function)
                lines.extend({"number": first + offset, "text": text.rstrip("\n")}
                             for offset, text in enumerate(source))
        sources[Path(module.__file__).name] = lines
    return sources


def texto(data, name, limit=2000):
    """Valida un campo de texto recibido desde el navegador."""
    value = data.get(name)
    if not isinstance(value, str) or len(value) > limit:
        raise ValueError(f"{name}: ingresa texto de hasta {limit} caracteres.")
    return value


def ejecutar(data):
    """Ejecuta una actividad y registra sus lineas y variables reales."""
    if not isinstance(data, dict):
        raise ValueError("Se esperaba un objeto con los datos del ejercicio.")
    exercise = data.get("exercise")
    steps = []
    output = io.StringIO()
    game_state = {}
    previous_trace = sys.gettrace()
    previous_input = builtins.input

    def trace(frame, event, value):
        if frame.f_code.co_filename in FILES and event == "exception" and isinstance(value[1], EsperandoLetra):
            event = "input"
        if event == "return" and steps and steps[-1]["event"] == "input":
            return trace
        if frame.f_code.co_filename in FILES and event in ("line", "return", "input"):
            variables = {name: repr(item) for name, item in frame.f_locals.items()}
            if len(steps) < 12000:
                steps.append({"file": Path(frame.f_code.co_filename).name,
                              "line": frame.f_lineno, "function": frame.f_code.co_name,
                              "event": event, "variables": variables,
                              "returnValue": repr(value) if event == "return" else None})
            if frame.f_code.co_name == "jugar_adivinanza":
                game_state.update(frame.f_locals)
        return trace

    try:
        with contextlib.redirect_stdout(output):
            sys.settrace(trace)
            if exercise == 1:
                phrases = texto(data, "phrases").splitlines()
                word = texto(data, "word", 100)
                replacement = texto(data, "replacement", 100)
                result = {"original": phrases,
                          "new": ejercicio_01.buscar_reemplazar(phrases, word, replacement)}
            elif exercise == 2:
                result = ejercicio_02.validar_email(texto(data, "email", 254))
            elif exercise == 3:
                raw = texto(data, "numbers", 500).replace(",", " ").split()
                if not 1 <= len(raw) <= 25:
                    raise ValueError("Ingresa entre 1 y 25 numeros enteros.")
                try:
                    numbers = [int(number) for number in raw]
                except ValueError:
                    raise ValueError("Usa numeros enteros separados por comas o espacios.") from None
                if any(abs(number) > 10**12 for number in numbers):
                    raise ValueError("Usa enteros entre -1000000000000 y 1000000000000.")
                largest, smallest = ejercicio_03.calcular_extremos(numbers)
                result = {"original": numbers, "largest": largest, "smallest": smallest,
                          "sorted": ejercicio_03.ordenar_lista(numbers),
                          "filtered": ejercicio_03.filtrar_mayores_a_cinco(numbers)}
            elif exercise == 4:
                secret = texto(data, "secret", 20)
                if secret not in ("python", "lista", "bucle", "variable"):
                    raise ValueError("Selecciona una de las palabras disponibles.")
                guesses = data.get("guesses", [])
                if not isinstance(guesses, list) or len(guesses) > 100 or any(
                        not isinstance(guess, str) or len(guess) > 50 for guess in guesses):
                    raise ValueError("La partida admite hasta 100 entradas de 50 caracteres.")
                pending = iter(guesses)

                def read_guess(prompt):
                    try:
                        return next(pending)
                    except StopIteration:
                        raise EsperandoLetra() from None

                builtins.input = read_guess
                finished = False
                try:
                    ejercicio_04.jugar_adivinanza(secret)
                    finished = True
                except EsperandoLetra:
                    pass
                letters = game_state.get("letras_intentadas", [])
                sys.settrace(previous_trace)
                result = {"progress": juego.mostrar_progreso(secret, letters),
                          "letters": letters, "errors": game_state.get("errores", 0),
                          "finished": finished, "won": juego.palabra_completa(secret, letters)}
            else:
                raise ValueError("Ejercicio desconocido.")
    finally:
        sys.settrace(previous_trace)
        builtins.input = previous_input
    return {"result": result, "steps": steps, "output": output.getvalue()}


class Handler(BaseHTTPRequestHandler):
    """Expone solamente los recursos y operaciones del laboratorio."""

    def respond(self, status, content, content_type):
        """Envia una respuesta con longitud y tipo explicitos."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, status, payload):
        """Serializa una respuesta JSON para el navegador."""
        self.respond(status, json.dumps(payload).encode(), "application/json; charset=utf-8")

    def do_GET(self):
        """Entrega la interfaz y el codigo de los ejercicios."""
        if self.path == "/api/curso":
            self.send_json(200, LESSONS)
            return
        if self.path == "/api/code":
            self.send_json(200, codigo_original())
            return
        paths = {"/": ("laboratorio.html", "text/html"),
                 "/aprender": ("aprender.html", "text/html"),
                 "/aprender.css": ("aprender.css", "text/css"),
                 "/aprender.js": ("aprender.js", "text/javascript"),
                 "/python-worker.js": ("python-worker.js", "text/javascript"),
                 "/practica_motor.py": ("practica_motor.py", "text/plain"),
                 "/favicon.ico": ("python.ico", "image/x-icon"),
                 "/laboratorio.css": ("laboratorio.css", "text/css"),
                 "/laboratorio.js": ("laboratorio.js", "text/javascript")}
        if self.path not in paths:
            self.send_json(404, {"error": "Recurso no encontrado."})
            return
        filename, content_type = paths[self.path]
        self.respond(200, (ROOT / filename).read_bytes(), content_type + "; charset=utf-8")

    def do_POST(self):
        """Valida una peticion y ejecuta el ejercicio solicitado."""
        if self.path != "/api/run":
            self.send_json(404, {"error": "Recurso no encontrado."})
            return
        if self.headers.get("Origin") not in (None, "http://" + self.headers.get("Host", "")):
            self.send_json(403, {"error": "Origen no permitido."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16000:
                raise ValueError("La peticion esta vacia o es demasiado grande.")
            data = json.loads(self.rfile.read(length))
            self.send_json(200, ejecutar(data))
        except (ValueError, UnicodeDecodeError) as error:
            self.send_json(400, {"error": str(error)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true", help="Abre el navegador al iniciar.")
    args = parser.parse_args()
    try:
        server = HTTPServer(("127.0.0.1", args.port), Handler)
    except OSError:
        server = HTTPServer(("127.0.0.1", 0), Handler)
    address = f"http://127.0.0.1:{server.server_port}"
    print(f"Laboratorio listo en {address}", flush=True)
    if args.open:
        webbrowser.open(address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()