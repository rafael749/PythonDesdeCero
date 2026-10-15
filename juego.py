def mostrar_progreso(palabra_secreta, letras_intentadas):
    """Devuelve la palabra con guiones bajos en las letras no adivinadas."""
    progreso = []
    for letra in palabra_secreta:
        if letra in letras_intentadas:
            progreso.append(letra)
        else:
            progreso.append("_")
    # join une los elementos con un espacio entre ellos.
    return " ".join(progreso)


def palabra_completa(palabra_secreta, letras_intentadas):
    """Devuelve True si se adivinaron todas las letras de la palabra."""
    for letra in palabra_secreta:
        # Con una sola letra que falte, la palabra todavia no esta completa.
        if letra not in letras_intentadas:
            return False
    return True