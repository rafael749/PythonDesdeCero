"""
EJERCICIO 3 — Análisis de una Lista de Números
###############################################

Dada la siguiente lista de números:

    numeros = [4, 7, 2, 9, 1, 5, 8, 3, 6]

Tu programa debe:

1. Imprimir la lista original.
2. Imprimir el número **más alto** y el **más bajo** de la lista.
3. Imprimir la lista **ordenada de menor a mayor**.
4. Imprimir solamente los números **mayores a 5**.

Restricciones:

- **No** se permite usar las funciones `sorted()`, `max()` ni `min()`.
- Recorré la lista con un bucle para calcular cada resultado.

Ejemplo de salida esperada:

    Lista original: [4, 7, 2, 9, 1, 5, 8, 3, 6]
    Número más alto: 9
    Número más bajo: 1
    Lista ordenada: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    Números mayores a 5: [7, 9, 8, 6]

"""


def calcular_extremos(numeros):
    """Devuelve el mayor y el menor de una lista no vacia."""
    # La posicion 0 es el primer elemento. Lo usamos como referencia inicial.
    mayor = numeros[0]
    menor = numeros[0]

    # Comparamos cada numero con el mayor y el menor encontrados hasta ahora.
    for numero in numeros:
        if numero > mayor:
            # Si encontramos uno mas alto, actualizamos el mayor.
            mayor = numero
        if numero < menor:
            # Si encontramos uno mas bajo, actualizamos el menor.
            menor = numero

    # Devolvemos los dos resultados, primero el mayor y despues el menor.
    return mayor, menor


def ordenar_lista(numeros):
    """Devuelve una copia ordenada de menor a mayor mediante burbuja."""
    # Ordenamos una copia para conservar la lista original.
    ordenados = numeros.copy()

    # len cuenta los elementos y range indica cuantas pasadas hacemos.
    for pasada in range(len(ordenados) - 1):
        # En cada pasada queda un numero en su lugar al final: revisamos uno menos.
        for posicion in range(len(ordenados) - 1 - pasada):
            # Comparamos un numero con su vecino de la derecha.
            if ordenados[posicion] > ordenados[posicion + 1]:
                # Guardamos el primero para no perderlo al intercambiar los dos.
                temporal = ordenados[posicion]
                ordenados[posicion] = ordenados[posicion + 1]
                ordenados[posicion + 1] = temporal

    # Devolvemos la copia ya ordenada.
    return ordenados


def filtrar_mayores_a_cinco(numeros):
    """Devuelve los numeros mayores a 5 en su orden original."""
    # Empezamos con una lista vacia para guardar los numeros que cumplan la condicion.
    mayores = []
    for numero in numeros:
        # El 5 no se incluye: pedimos numeros estrictamente mayores.
        if numero > 5:
            # append agrega el numero al final, conservando el orden de llegada.
            mayores.append(numero)
    return mayores


# Este bloque se ejecuta al iniciar este archivo como programa.
if __name__ == "__main__":
    numeros = [4, 7, 2, 9, 1, 5, 8, 3, 6]
    print("Lista original:", numeros)

    # Llamamos a la funcion y guardamos sus dos resultados en variables separadas.
    mayor, menor = calcular_extremos(numeros)
    print("Número más alto:", mayor)
    print("Número más bajo:", menor)
    # Ejecutamos las otras funciones y mostramos las listas que devuelven.
    print("Lista ordenada:", ordenar_lista(numeros))
    print("Números mayores a 5:", filtrar_mayores_a_cinco(numeros))
