"""
EJERCICIO 4 — Juego de Adivinanza de Palabras con Módulo
#########################################################

Definí una función llamada `jugar_adivinanza(palabra_secreta)` que implemente
un juego tipo ahorcado, **sin dibujo**.

Reglas:

- El usuario ingresa **una sola letra por turno**.
- Llevá un registro de las letras ya intentadas.
- Después de cada intento, mostrá el **progreso de la palabra** con guiones
  bajos para las letras todavía no adivinadas.
- El juego termina cuando:
  - El usuario adivina la palabra completa → mostrar mensaje de victoria.
  - El usuario acumula **5 errores** → mostrar mensaje de derrota y la
    palabra secreta.

Requisitos:
- Las funciones auxiliares del juego deben estar en un módulo separado llamado
  `juego.py`, e importarse en este archivo. Como mínimo el módulo debe tener:
  - `mostrar_progreso(palabra_secreta, letras_intentadas)`: devuelve el string
    con las letras adivinadas y guiones bajos (por ejemplo `"p _ _ _ _ _"`).
  - `palabra_completa(palabra_secreta, letras_intentadas)`: devuelve `True` si
    ya se adivinaron todas las letras de la palabra, o `False` si no.
- Cada función del módulo debe tener un docstring de una línea que explique
  qué hace. Ver formato: https://peps.python.org/pep-0257/#one-line-docstrings
- La función `jugar_adivinanza` y la lógica principal deben estar en este
  archivo (ejercicio_04.py).
- Si el usuario ingresa más de un carácter, algo que no es una letra, o una
  letra que ya había intentado, mostrar un mensaje de aviso y volver a pedir
  la letra **sin sumar un error**.

Ejemplo de ejecución (palabra secreta = `"python"`):

    Palabra: _ _ _ _ _ _
    Ingresá una letra: p
    ¡Bien! Letra encontrada.
    Palabra: p _ _ _ _ _
    Ingresá una letra: a
    Letra incorrecta. Errores: 1/5
    Ingresá una letra: p
    Ya intentaste esa letra.
    ...

"""


# Importamos las dos funciones que estan en el archivo juego.py.
from juego import mostrar_progreso, palabra_completa


def jugar_adivinanza(palabra_secreta):
    """Pide letras hasta completar la palabra o acumular cinco errores."""
    # lower convierte a minusculas para comparar las letras de la misma forma.
    palabra_secreta = palabra_secreta.lower()
    letras_intentadas = []
    errores = 0

    # Seguimos jugando mientras queden intentos y falten letras.
    while errores < 5 and not palabra_completa(palabra_secreta, letras_intentadas):
      print("Palabra:", mostrar_progreso(palabra_secreta, letras_intentadas))
      letra = input("Ingresa una letra: ").lower()

      # len cuenta caracteres e isalpha comprueba que sean letras.
      if len(letra) != 1 or not letra.isalpha():
        print("Ingresa una sola letra.")
        # continue vuelve al inicio del bucle sin sumar errores.
        continue

      if letra in letras_intentadas:
        print("Ya intentaste esa letra.")
        continue

      # Guardamos la letra para recordar que ya se intento.
      letras_intentadas.append(letra)
      if letra in palabra_secreta:
        print("Bien! Letra encontrada.")
      else:
        errores = errores + 1
        print("Letra incorrecta. Errores:", errores, "/5")

    # Mostramos el progreso final y el motivo por el que termino el juego.
    print("Palabra:", mostrar_progreso(palabra_secreta, letras_intentadas))
    if palabra_completa(palabra_secreta, letras_intentadas):
      print("Ganaste! Adivinaste la palabra.")
    else:
      print("Perdiste. La palabra secreta era:", palabra_secreta)


# Este bloque inicia el juego al ejecutar este archivo.
if __name__ == "__main__":
    jugar_adivinanza("python")
