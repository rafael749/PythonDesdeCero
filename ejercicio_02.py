"""
EJERCICIO 2 — Validar Email
############################

Definí una función llamada `validar_email(email)` que reciba un string y
devuelva `True` si el email es válido, o `False` en caso contrario.

Validaciones requeridas:

1. Debe contener **exactamente un símbolo `@`** (ni más, ni menos).
2. Debe tener **al menos un carácter antes** del `@` (nombre de usuario).
3. Debe tener **al menos un carácter después** del `@` y antes del punto
   (dominio).
4. Debe contener **al menos un punto `.`** después del `@`.
5. Debe tener **al menos 2 caracteres después del último punto** (extensión
   del tipo `.com`, `.ar`, `.edu`).
6. **No debe contener espacios en blanco** en ninguna parte.
7. El email **no puede empezar ni terminar** con `@` o `.`.

Ejemplos:

    validar_email("juan@gmail.com")          # True
    validar_email("maria.lopez@utn.edu.ar")  # True
    validar_email("correo@dominio.com.ar")   # True
    validar_email("usuario@@gmail.com")      # False  (dos @)
    validar_email("gmail.com")               # False  (sin @)
    validar_email("juan @gmail.com")         # False  (tiene espacio)
    validar_email("@gmail.com")              # False  (sin usuario)
    validar_email("juan@gmail")              # False  (sin punto después del @)
    validar_email("juan@.com")               # False  (sin dominio)
    validar_email("juan@gmail.c")            # False  (extensión muy corta)

Ayuda: podés usar `.count()` para contar caracteres, `.find()` o `.index()`
para localizar posiciones, y validar cada condición paso a paso.

"""


def validar_email(email):
   """Devuelve True si el email cumple las siete reglas de la consigna."""
   # count cuenta las arrobas. Si no hay exactamente una, no es valido.
   # Cada return False termina la funcion al encontrar un problema.
   if email.count("@") != 1:
      return False

   # Revisamos cada caracter: no aceptamos espacios, tabulaciones ni saltos de linea.
   for caracter in email:
      if caracter.isspace():
         return False

   # startswith revisa el inicio y endswith revisa el final del texto.
   if email.startswith(("@", ".")) or email.endswith(("@", ".")):
      return False

   # split separa el texto en dos partes usando la arroba.
   # Por ejemplo, "juan@gmail.com" queda como "juan" y "gmail.com".
   usuario, dominio = email.split("@")
   # len cuenta caracteres: cero significa que el usuario esta vacio.
   if len(usuario) == 0:
      return False

   # find devuelve -1 si no hay punto, o 0 si el dominio empieza con punto.
   # Ambos casos fallan: necesitamos texto antes del primer punto.
   primer_punto = dominio.find(".")
   if primer_punto <= 0:
      return False

   # Separamos una vez desde la derecha y tomamos lo que sigue al ultimo punto.
   # Por ejemplo, de "gmail.com" obtenemos "com".
   extension = dominio.rsplit(".", 1)[1]
   # La extension debe tener al menos dos caracteres.
   if len(extension) < 2:
      return False

   # Si llegamos hasta aqui, el correo paso todas las validaciones.
   return True


# Este bloque se ejecuta al iniciar este archivo como programa.
if __name__ == "__main__":
   # input espera que escribamos un correo y presionemos Enter.
   correo = input("Ingresa un email: ")
   # Mostramos True si cumple las reglas o False si alguna falla.
   print("Email valido:", validar_email(correo))
