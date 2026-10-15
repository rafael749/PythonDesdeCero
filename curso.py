"""Ruta de practica desde las primeras instrucciones hasta el parcial."""

LESSONS = []


def salida(expected, inputs=None, why="La salida debe coincidir con lo pedido, linea por linea."):
    """Describe una comprobacion de la salida visible."""
    return {"kind": "output", "title": "Salida con entradas " + repr(inputs or []),
            "expected": expected, "inputs": inputs or [], "why": why}


def variable(name, expected, why):
    """Describe el valor esperado de una variable."""
    return {"kind": "variable", "title": "Valor de " + name, "name": name,
            "expected": expected, "why": why}


def funcion(name, args, expected, why, unchanged=False, inputs=None):
    """Describe una llamada de prueba a una funcion."""
    return {"kind": "function", "title": name + "(" + ", ".join(map(repr, args)) + ")",
            "call": {"function": name, "args": args}, "expected": expected, "why": why,
            "expectedType": "tuple" if isinstance(expected, tuple) else None,
            "unchanged": unchanged, "inputs": inputs or []}


def estructura(name, why):
    """Pide una construccion explicitamente indicada en la consigna."""
    return {"kind": "node", "name": name, "title": "Usar " + name, "why": why}


SIN_ATAJOS = {"kind": "forbid", "names": ["max", "min", "sorted", "sort"],
              "title": "Resolver con bucles, sin max, min, sorted ni sort",
              "why": "El objetivo es construir las comparaciones y los intercambios, no delegarlos a una funcion de ordenamiento."}


def agregar(group, title, theory, example, task, cases, hints, starter="", inputs="", rules=None, module=None):
    """Agrega una practica con explicacion, consigna y pruebas."""
    identifier = len(LESSONS) + 1
    files = {"solucion.py": starter}
    if module is not None:
        files["juego.py"] = module
    LESSONS.append({"id": identifier, "group": group, "title": title, "theory": theory,
                    "example": example, "task": task, "cases": cases, "hints": hints,
                    "files": files, "inputs": inputs, "rules": rules or []})


agregar("01 / Primeras instrucciones", "Tu primer mensaje",
        ["Un programa es una secuencia de instrucciones. Python las ejecuta de arriba hacia abajo.",
         "print() muestra un dato. El texto va entre comillas; los parentesis contienen lo que recibe la funcion. Las comillas no aparecen en la salida."],
        'print("Buen dia")\nprint("Estoy practicando")',
        'Mostra exactamente Hola Python en una sola linea.',
        [salida("Hola Python", why="print muestra el texto, sin las comillas que lo delimitan. Las mayusculas y los espacios tambien son parte del texto.")],
        ["Escribi print seguido de parentesis.", 'Dentro de los parentesis va el texto entre comillas: "Hola Python".'])

agregar("01 / Primeras instrucciones", "Un nombre para un dato",
        ["Una variable es un nombre asociado a un valor. El signo = asigna el valor de la derecha al nombre de la izquierda; no pregunta si son iguales.",
         "Al usar nombre sin comillas, Python busca su valor. Con comillas, seria el texto literal nombre. print puede recibir varios datos separados por comas."],
        'ciudad = "Rosario"\nprint("Ciudad:", ciudad)',
        'Crea nombre con el texto Ana. Luego mostra Hola Ana usando esa variable.',
        [variable("nombre", "Ana", "La variable nombre debe guardar el string 'Ana'."), salida("Hola Ana")],
        ['Primero asigna el texto a nombre con =.', 'print("Hola", nombre) agrega un espacio entre los dos datos.'])

agregar("01 / Primeras instrucciones", "Texto o numero",
        ["Un string (str) representa texto y lleva comillas. Un entero (int) representa un numero sin decimales y se escribe sin comillas.",
         "20 y '20' se ven parecidos, pero tienen tipos distintos: el primero permite hacer cuentas directamente."],
        'cantidad = 3\nproducto = "cuaderno"\nprint(cantidad, producto)',
        'Crea edad con el numero entero 20 y mostra su valor.',
        [variable("edad", 20, "Se necesita el entero 20, no el string '20'. El tipo importa al operar."), salida("20")],
        ["Asigna un numero sin comillas.", "Mostra la variable con print(edad)."])

agregar("02 / Operaciones y entradas", "Calcular un total",
        ["+ suma, - resta, * multiplica y / divide. Una expresion calcula un valor que podes guardar en otra variable.",
         "Python primero evalua el lado derecho de una asignacion. Por eso total puede recibir el resultado de precio * cantidad."],
        'horas = 4\nminutos = horas * 60\nprint(minutos)',
        'Crea precio = 150 y cantidad = 3. Guarda su producto en total y mostralo.',
        [variable("precio", 150, "Cada unidad cuesta 150."), variable("cantidad", 3, "Se compran tres unidades."),
         variable("total", 450, "El total es precio por cantidad: 150 * 3."), salida("450")],
        ["Crea primero las dos variables de entrada.", "Usa * para calcular el producto, no el texto '150 * 3'."])

agregar("02 / Operaciones y entradas", "El resto de una division",
        ["El operador % devuelve el resto de una division entera. En 10 % 3, el resto es 1.",
         "Un entero es par si al dividirlo por 2 sobra 0. Esto sera util para construir condiciones."],
        'sobrantes = 14 % 4\nprint(sobrantes)',
        'Crea numero = 7. Guarda el resto de dividir numero por 2 en resto y mostralo.',
        [variable("resto", 1, "7 contiene tres grupos de 2 y sobra 1."), salida("1")],
        ["No necesitas usar /; el operador para el resto es %.", "Calcula numero % 2."])

agregar("02 / Operaciones y entradas", "Leer una respuesta",
        ["input() recibe una respuesta y devuelve texto. Una asignacion permite guardar esa respuesta.",
         "En esta practica, cada linea del campo Entradas responde a una llamada de input(). En las pruebas usa input() sin mensaje para que la salida solo contenga el resultado pedido."],
        'animal = input()\nprint("Elegiste", animal)',
        'Lee un nombre con input() y mostra Hola seguido de ese nombre. Debe funcionar con cualquier nombre.',
        [salida("Hola Lucia", ["Lucia"], "El saludo debe usar la respuesta recibida, no un nombre fijo."), salida("Hola Leo", ["Leo"])],
        ["Guarda input() en una variable.", 'Mostra "Hola" y la variable separados por una coma.'], inputs="Lucia")

agregar("03 / Decidir con condiciones", "Convertir una entrada",
        ["input() siempre devuelve str, incluso cuando escribis digitos. int(texto) convierte un texto numerico a entero.",
         "Primero se evalua lo mas interno: en int(input()), se recibe la respuesta y despues se convierte."],
        'unidades = int(input())\nprint(unidades * 2)',
        'Lee una edad entera y mostra la edad que tendra la persona dentro de 5 a\u00f1os.',
        [salida("25", ["20"], "Converti la edad antes de sumar 5. Concatenar textos no realiza una suma."), salida("12", ["7"])],
        ["Usa int() sobre el resultado de input().", "Despues de convertir, suma 5 y mostra el resultado."], inputs="20")

agregar("03 / Decidir con condiciones", "Verdadero o falso",
        ["Una comparacion devuelve un booleano: True o False. >= significa mayor o igual; == compara igualdad, mientras = asigna.",
         "Los booleanos no llevan comillas. print(8 > 3) muestra True."],
        'temperatura = 12\nprint(temperatura < 10)',
        'Lee una edad entera. Mostra True si tiene al menos 18 a\u00f1os, o False si tiene menos.',
        [salida("True", ["18"], "El limite 18 tambien debe incluirse: se necesita >=, no >."), salida("False", ["17"]), salida("True", ["40"])],
        ["Converti la entrada a entero.", "Podes mostrar directamente el resultado de una comparacion."], inputs="18")

agregar("03 / Decidir con condiciones", "Elegir entre dos caminos",
        ["if ejecuta un bloque cuando una condicion es verdadera. else ejecuta el camino alternativo.",
         "Cada encabezado termina con : y sus instrucciones llevan sangria (cuatro espacios). La sangria es parte de la sintaxis de Python."],
        'stock = 2\nif stock > 0:\n    print("Disponible")\nelse:\n    print("Agotado")',
        'Lee una nota entera. Con if y else, mostra Aprobado si es 6 o mas; si no, mostra A recuperar.',
        [salida("Aprobado", ["6"], "6 es el primer valor aprobado."), salida("A recuperar", ["5"]), salida("Aprobado", ["10"])],
        ["Compara la nota con 6.", "Cada print pertenece a un bloque diferente; deja la misma sangria dentro de cada bloque."],
        inputs="6", rules=[estructura("If", "Esta practica pide una decision con if.")])

agregar("04 / Condiciones y textos", "Tres posibilidades",
        ["elif permite preguntar otra condicion si la anterior fue falsa. Solo se ejecuta el primer camino que se cumple.",
         "else no lleva condicion: cubre los casos restantes."],
        'hora = 15\nif hora < 12:\n    print("Ma\u00f1ana")\nelif hora < 20:\n    print("Tarde")\nelse:\n    print("Noche")',
        'Lee un entero y mostra positivo, negativo o cero segun su valor.',
        [salida("positivo", ["3"]), salida("negativo", ["-2"]), salida("cero", ["0"], "Cero no es positivo ni negativo.")],
        ["Pregunta primero si es mayor que 0.", "Usa otra condicion para los negativos y deja cero para el caso restante."], inputs="-2")

agregar("04 / Condiciones y textos", "Dos condiciones juntas",
        ["and exige que ambas condiciones se cumplan. or permite que se cumpla al menos una. not invierte un booleano.",
         "Para pertenecer a un intervalo, un numero debe superar el limite inferior Y no pasar el superior."],
        'edad = 15\nprint(edad >= 13 and edad <= 19)',
        'Lee un entero y mostra True si esta entre 1 y 10 inclusive; False en caso contrario.',
        [salida("True", ["1"]), salida("True", ["10"]), salida("False", ["0"]), salida("False", ["11"])],
        ["Necesitas comprobar dos limites.", "Una ambas condiciones con and; con or aceptarias numeros fuera del intervalo."], inputs="5")

agregar("04 / Condiciones y textos", "La longitud de un texto",
        ["len(texto) devuelve cuantos caracteres contiene. Los espacios tambien cuentan.",
         "El string vacio se escribe '' y tiene longitud 0. No es lo mismo que ' ', que contiene un espacio."],
        'palabra = "mesa"\nprint(len(palabra))',
        'Lee un texto con input() y mostra su cantidad de caracteres, incluyendo espacios.',
        [salida("6", ["python"]), salida("8", ["hola sol"]), salida("0", [""], "El texto vacio no contiene caracteres.")],
        ["Guarda la entrada sin modificarla.", "Aplica len a la variable y mostra el numero obtenido."], inputs="python")

agregar("05 / Herramientas para strings", "Comparar sin mayusculas",
        ["Un metodo es una operacion asociada a un dato. Se escribe dato.metodo(). lower() devuelve una copia del texto en minusculas.",
         "Los strings no cambian en el lugar: para conservar el cambio, guarda o utiliza lo que devuelve el metodo."],
        'saludo = "BUEN Dia"\nnormalizado = saludo.lower()\nprint(normalizado)',
        'Lee un texto y mostra su version en minusculas. No elimines sus espacios.',
        [salida("python", ["PyThOn"]), salida("hola mundo", ["HOLA MUNDO"])],
        ["Los parentesis de lower() son necesarios para ejecutar el metodo.", "Mostra el valor que devuelve texto.lower()."], inputs="PyThOn")

agregar("05 / Herramientas para strings", "Contar coincidencias",
        ["texto.count(fragmento) cuenta cuantas veces aparece ese fragmento.",
         "Un email del parcial necesita exactamente una arroba: contar sera una primera comprobacion, pero no alcanza para validarlo completo."],
        'frase = "banana"\nprint(frase.count("a"))',
        'Lee un texto y mostra cuantas arrobas @ contiene.',
        [salida("1", ["ana@mail.com"]), salida("2", ["ana@@mail.com"]), salida("0", ["sin arroba"])],
        ['Usa count con el texto "@".', "Mostra el numero de coincidencias, no un booleano."], inputs="ana@mail.com")

agregar("05 / Herramientas para strings", "Reemplazar sin borrar el original",
        ["replace(viejo, nuevo) devuelve un string con todas las coincidencias reemplazadas. Distingue mayusculas de minusculas.",
         "Guardar el resultado en otra variable permite comparar el antes y el despues."],
        'texto = "sol y sol"\nnuevo = texto.replace("sol", "luna")\nprint(texto)\nprint(nuevo)',
        'Crea frase = "gato y gato". Crea nueva reemplazando gato por perro. No cambies frase. Mostra nueva.',
        [variable("frase", "gato y gato", "El original debe mantenerse intacto."), variable("nueva", "perro y perro", "replace cambia todas las coincidencias."), salida("perro y perro")],
        ["No asignes el resultado otra vez a frase.", 'Guarda frase.replace("gato", "perro") en nueva.'])

agregar("06 / Primeras listas", "Separar un texto",
        ["split(separador) devuelve una lista de partes. Una lista agrupa varios valores entre corchetes.",
         "Si hay exactamente dos partes, usuario, dominio = partes guarda una en cada variable. Con otra cantidad, esa asignacion falla."],
        'fecha = "2026/10"\nanio, mes = fecha.split("/")\nprint(anio)\nprint(mes)',
        'Lee un email con exactamente una arroba. Separa y mostra primero el usuario y luego el dominio, en lineas distintas.',
        [salida("ana\nmail.com", ["ana@mail.com"]), salida("leo\nescuela.edu.ar", ["leo@escuela.edu.ar"])],
        ['Separa usando split("@").', "Guarda las dos partes y usa dos llamadas de print."], inputs="ana@mail.com")

agregar("06 / Primeras listas", "Posiciones de una lista",
        ["Una lista conserva el orden de sus elementos. La primera posicion es 0, la segunda es 1, y asi sucesivamente.",
         "lista[-1] obtiene el ultimo elemento. Pedir una posicion inexistente produce IndexError."],
        'colores = ["rojo", "verde", "azul"]\nprint(colores[0])\nprint(colores[-1])',
        'Crea numeros = [4, 7, 2]. Guarda el primer elemento en primero y el ultimo en ultimo. Mostralos en dos lineas.',
        [variable("primero", 4, "La posicion 0 contiene el primer elemento."), variable("ultimo", 2, "El ultimo valor es 2, no su posicion."), salida("4\n2")],
        ["Usa corchetes para acceder a una posicion.", "La ultima posicion puede escribirse -1."])

agregar("06 / Primeras listas", "Agregar un elemento",
        ["Una lista vacia se escribe []. append(valor) agrega un elemento al final de una lista existente.",
         "A diferencia de replace en strings, append modifica la lista y devuelve None. No hagas lista = lista.append(valor)."],
        'compras = ["pan"]\ncompras.append("leche")\nprint(compras)',
        'Crea letras = ["a", "b"]. Agrega "c" con append y mostra la lista.',
        [variable("letras", ["a", "b", "c"], "append debe agregar al final sin perder los valores anteriores."), salida("['a', 'b', 'c']")],
        ['Llama letras.append("c") sin asignar su retorno.', "Despues mostra letras."])

agregar("07 / Recorrer y acumular", "Una vuelta por elemento",
        ["for elemento in lista: ejecuta su bloque una vez por cada valor de la lista, en orden.",
         "La variable del bucle recibe el valor actual. Su nombre lo elegis vos; no necesitas crearla antes."],
        'for color in ["rojo", "azul"]:\n    print(color)',
        'Recorre [3, 1, 4] con for y mostra cada numero en una linea.',
        [salida("3\n1\n4", why="El bucle conserva el orden original; cada print produce una linea.")],
        ["Despues de for va un nombre de variable, in y la lista.", "El print debe estar dentro del bucle con sangria."], rules=[estructura("For", "Practica recorrer una lista con for.")])

agregar("07 / Recorrer y acumular", "Construir una suma",
        ["Un acumulador guarda un resultado parcial. Se inicializa antes del bucle y se actualiza en cada vuelta.",
         "total = total + numero usa el valor anterior para calcular el nuevo. Si reinicias total dentro del bucle, perdes lo acumulado."],
        'total = 0\nfor precio in [10, 20]:\n    total = total + precio\nprint(total)',
        'Suma [4, 7, 2] con un for, sin usar sum(). Guarda el resultado en total y mostralo una sola vez.',
        [variable("total", 13, "Se acumulan los tres numeros: 4 + 7 + 2."), salida("13")],
        ["Empieza con total = 0 fuera del bucle.", "El print final va despues del bucle, sin su sangria."],
        rules=[estructura("For", "El total se construye vuelta a vuelta."), {"kind": "forbid", "names": ["sum"], "title": "No usar sum", "why": "En esta practica construis el acumulador."}])

agregar("07 / Recorrer y acumular", "Filtrar una lista",
        ["Dentro de un for podes usar if para decidir que elementos conservar.",
         "Una lista de resultados empieza vacia. append agrega solo los valores que cumplen la condicion, sin cambiar el orden."],
        'pares = []\nfor numero in [1, 2, 3, 4]:\n    if numero % 2 == 0:\n        pares.append(numero)\nprint(pares)',
        'Recorre [4, 7, 2, 9, 5, 8]. Guarda solo los mayores a 5 en mayores y mostra esa lista.',
        [variable("mayores", [7, 9, 8], "El 5 no entra: mayor que 5 no significa mayor o igual."), salida("[7, 9, 8]")],
        ["Crea mayores = [] antes del for.", "append pertenece al bloque del if: lleva otra sangria."], rules=[estructura("For", "Recorre los datos para construir el filtro.")])

agregar("08 / Comparar y ordenar", "Encontrar los extremos",
        ["Para buscar un extremo, usa el primer valor como referencia y comparalo con los demas.",
         "No empieces el mayor en 0: eso falla si todos los numeros son negativos. La lista de esta practica no esta vacia."],
        'valores = [-8, -3, -5]\nmayor = valores[0]\nfor valor in valores:\n    if valor > mayor:\n        mayor = valor\nprint(mayor)',
        'Para numeros = [-4, -7, -2], calcula mayor y menor con un bucle. Mostra primero mayor y luego menor.',
        [variable("mayor", -2, "Entre numeros negativos, -2 es mayor que -4 y -7."), variable("menor", -7, "El menor debe ser un elemento real de la lista."), salida("-2\n-7")],
        ["Inicializa ambos extremos con numeros[0].", "Dentro del for, usa una comparacion para cada extremo."], rules=[SIN_ATAJOS, estructura("For", "Compara los elementos con un bucle.")])

agregar("08 / Comparar y ordenar", "Intercambiar sin perder datos",
        ["Si reemplazas una posicion, su valor anterior se pierde salvo que lo hayas guardado.",
         "Una variable temporal conserva uno de los valores durante un intercambio. Una copia de lista se obtiene con .copy()."],
        'datos = [9, 3]\ntemporal = datos[0]\ndatos[0] = datos[1]\ndatos[1] = temporal\nprint(datos)',
        'Crea numeros = [8, 2]. Intercambia sus dos elementos y mostra [2, 8].',
        [variable("numeros", [2, 8], "Deben conservarse ambos valores, solo cambia su posicion."), salida("[2, 8]")],
        ["Guarda el primer elemento antes de sobrescribirlo.", "Usa el valor guardado para completar la segunda posicion."])

agregar("08 / Comparar y ordenar", "Ordenar por pasadas",
        ["range(fin) produce posiciones desde 0 hasta fin - 1. range(len(lista) - 1) permite comparar un elemento con su vecino de la derecha.",
         "En burbuja se intercambian vecinos desordenados. Una pasada lleva el mayor al final; varias pasadas terminan de ordenar. Un for dentro de otro repite ese recorrido."],
        'datos = [2, 6, 4]\nfor posicion in range(len(datos) - 1):\n    print(datos[posicion], datos[posicion + 1])',
        'Crea numeros = [4, 1, 3, 2] y una copia ordenados. Ordena la copia de menor a mayor con bucles e intercambios. Mostra ordenados.',
        [variable("numeros", [4, 1, 3, 2], "La lista original se conserva."), variable("ordenados", [1, 2, 3, 4], "Una sola pasada puede no alcanzar para ordenar todos los valores."), salida("[1, 2, 3, 4]")],
        ["Copia numeros con .copy() y repite varias pasadas.", "Compara ordenados[posicion] con ordenados[posicion + 1]; intercambia solo si el izquierdo es mayor.", "El ultimo indice no tiene vecino derecho. Termina el range antes de ese indice."], rules=[SIN_ATAJOS, estructura("For", "El ordenamiento se construye con recorridos.")])

agregar("09 / Repetir con while", "Contar hasta un limite",
        ["while repite un bloque mientras su condicion sea verdadera. La condicion se revisa antes de cada vuelta.",
         "Algo dentro del bucle debe permitir que termine. Un contador se actualiza con contador = contador + 1."],
        'contador = 2\nwhile contador <= 4:\n    print(contador)\n    contador = contador + 1',
        'Usa while para mostrar 1, 2 y 3 en lineas separadas. El programa debe terminar.',
        [salida("1\n2\n3")],
        ["Inicializa un contador antes del while.", "Despues de imprimir, aumenta el contador para acercarte al limite."], rules=[estructura("While", "En esta practica el limite se controla con while.")])

agregar("09 / Repetir con while", "Seguir pidiendo una respuesta",
        ["Un bucle puede continuar hasta recibir una respuesta determinada. Pedir otro input dentro del bucle permite actualizar la condicion.",
         "Si la primera respuesta ya cumple la condicion de salida, el cuerpo del while puede ejecutarse cero veces."],
        'respuesta = input()\nwhile respuesta != "fin":\n    respuesta = input()\nprint("Terminado")',
        'Lee respuestas hasta recibir si. Entonces mostra Listo una sola vez. No imprimas mensajes al pedir entradas.',
        [salida("Listo", ["no", "quizas", "si"], "El programa debe seguir leyendo hasta encontrar si."), salida("Listo", ["si"])],
        ["Lee una respuesta antes del while.", 'Mientras la respuesta sea distinta de "si", lee otra.'], inputs="no\nsi", rules=[estructura("While", "La cantidad de vueltas depende de las respuestas.")])

agregar("09 / Repetir con while", "Saltar una vuelta",
        ["continue salta el resto de la vuelta actual y pasa a la siguiente. No termina todo el bucle.",
         "En un while, cuidado con saltar la actualizacion del contador: podria repetirse para siempre."],
        'for texto in ["hola", "", "chau"]:\n    if texto == "":\n        continue\n    print(texto)',
        'Recorre [2, 0, 3, 0, 1]. Usa continue para saltar los ceros y mostra solo los demas, uno por linea.',
        [salida("2\n3\n1", why="continue evita imprimir los ceros pero permite procesar los elementos siguientes.")],
        ["Pregunta si el numero es cero antes del print.", "Coloca continue dentro del if y print despues de ese bloque."], rules=[estructura("Continue", "El objetivo es practicar como se salta una vuelta.")])

agregar("10 / Crear funciones", "Recibir y devolver",
        ["def nombre(parametro): define una funcion. Su cuerpo se ejecuta cuando se la llama, no cuando se la define.",
         "Un parametro recibe un dato de la llamada. return devuelve un resultado y termina la funcion. print solo muestra texto y no reemplaza return."],
        'def triple(numero):\n    return numero * 3\n\nresultado = triple(4)\nprint(resultado)',
        'Define doble(numero) para devolver el doble del numero recibido. Debe funcionar con positivos, negativos y cero.',
        [funcion("doble", [number], number * 2, "La funcion debe devolver el valor calculado, no solamente imprimirlo.") for number in [4, -3, 0]],
        ["La funcion recibe numero; no uses input dentro de ella.", "Usa return con el producto por 2."], starter="def doble(numero):\n    pass\n")

agregar("10 / Crear funciones", "Una funcion que decide",
        ["Una funcion puede devolver True o False. Eso permite usarla como condicion en otro programa.",
         "isalpha() comprueba que un texto contenga letras, pero tambien acepta varias letras juntas. Para una sola letra, combina esa comprobacion con len(texto) == 1."],
        'def es_positivo(numero):\n    return numero > 0\n\nprint(es_positivo(-2))',
        'Define es_letra(texto): devuelve True solo si contiene exactamente una letra; False para numeros, vacio o varias letras.',
        [funcion("es_letra", [text], expected, "Deben cumplirse ambas condiciones: longitud 1 y contenido alfabetico.") for text, expected in [("a", True), ("Z", True), ("ab", False), ("2", False), ("", False), (" ", False)]],
        ["Combina len(texto) == 1 con texto.isalpha().", "Devuelve el booleano, no los strings 'True' o 'False'."], starter="def es_letra(texto):\n    pass\n")

agregar("10 / Crear funciones", "Una lista nueva como resultado",
        ["Una funcion tambien puede recibir y devolver listas. Si modificas la lista recibida, el cambio afecta a quien la entrego.",
         "Para conservar la entrada, construye una lista nueva y devolvela al terminar el for. Un return dentro del for puede terminar demasiado pronto."],
        'def sumar_uno(valores):\n    nuevos = []\n    for valor in valores:\n        nuevos.append(valor + 1)\n    return nuevos',
        'Define duplicar_lista(numeros): devuelve una nueva lista con cada numero duplicado, sin modificar la original.',
        [funcion("duplicar_lista", [values], [number * 2 for number in values], "Cada elemento debe procesarse, conservando el orden.", True) for values in [[1, 3, -2], [], [0]]],
        ["Empieza con una lista vacia dentro de la funcion.", "Agrega el doble de cada elemento.", "Devolve la lista despues de terminar el bucle."], starter="def duplicar_lista(numeros):\n    pass\n")

agregar("11 / Preparar el juego", "Mostrar letras descubiertas",
        ["in comprueba si un valor pertenece a una lista o si un fragmento aparece en un texto.",
         "' '.join(partes) une strings con un espacio entre ellos. Es util para mostrar letras y guiones sin imprimir una lista con corchetes."],
        'partes = ["a", "_", "c"]\nprint(" ".join(partes))\nprint("a" in ["a", "e"])',
        'Define mostrar_progreso(palabra_secreta, letras_intentadas). Devuelve las letras intentadas y _ para las que faltan, separados por espacios.',
        [funcion("mostrar_progreso", ["python", ["p", "o"]], "p _ _ _ o _", "Cada posicion representa una letra de la palabra."),
         funcion("mostrar_progreso", ["ala", ["a"]], "a _ a", "Una letra descubierta aparece en todas sus posiciones."),
         funcion("mostrar_progreso", ["sol", []], "_ _ _", "Sin intentos todas las posiciones permanecen ocultas.")],
        ["Recorre la palabra y arma una lista de strings.", 'Agrega la letra si esta intentada; si no, agrega "_".', 'Devuelve " ".join(progreso).'], starter="def mostrar_progreso(palabra_secreta, letras_intentadas):\n    pass\n")

agregar("11 / Preparar el juego", "Separar codigo en un modulo",
        ["Un modulo es un archivo Python. from juego import palabra_completa permite usar una funcion definida en juego.py.",
         "Un docstring es un string al principio del cuerpo de una funcion que explica su proposito. Una funcion puede terminar con False apenas encuentra una letra pendiente; solo devuelve True al revisar todas."],
        'def contiene_cero(numeros):\n    """Indica si hay al menos un cero."""\n    for numero in numeros:\n        if numero == 0:\n            return True\n    return False',
        'En juego.py define mostrar_progreso como en la practica anterior y palabra_completa, que devuelve True si todas las letras fueron intentadas. Agrega un docstring de una linea a cada funcion. Importa ambas en solucion.py.',
        [funcion("palabra_completa", ["ala", ["a", "l"]], True, "Una letra repetida no necesita intentarse dos veces."),
         funcion("palabra_completa", ["sol", ["s", "o"]], False, "Todavia falta la letra l."),
         funcion("mostrar_progreso", ["sol", ["o"]], "_ o _", "La funcion importada debe estar disponible en solucion.py.")],
        ["Completa las funciones en la pesta\u00f1a juego.py.", "Busca alguna letra de la palabra que no este en letras_intentadas. Si la hay, devolve False.", "Devolve True fuera del for, cuando ya revisaste todas."],
        starter="from juego import mostrar_progreso, palabra_completa\n", module="def mostrar_progreso(palabra_secreta, letras_intentadas):\n    pass\n\ndef palabra_completa(palabra_secreta, letras_intentadas):\n    pass\n",
        rules=[{"kind": "module", "names": ["mostrar_progreso", "palabra_completa"], "title": "Importar las dos funciones de juego.py con docstrings", "why": "El modulo separa las funciones auxiliares; cada docstring debe explicar su funcion en una linea."}])

agregar("12 / Practica del parcial", "Parcial 1: buscar y reemplazar",
        ["Este desafio combina listas, for, replace, append y return. Los argumentos son datos de entrada; no hace falta pedirlos con input.",
         "Una buena prueba incluye varias coincidencias, mayusculas distintas, frases sin la palabra y una lista vacia."],
        'def agregar_signo(frases):\n    nuevas = []\n    for frase in frases:\n        nuevas.append(frase + "!")\n    return nuevas',
        'Define buscar_reemplazar(lista, palabra, reemplazo). Devuelve una nueva lista reemplazando todas las coincidencias en cada frase. No modifiques la lista original.',
        [funcion("buscar_reemplazar", [["gato gato", "sin mascota"], "gato", "perro"], ["perro perro", "sin mascota"], "Cada frase conserva su posicion; todas las coincidencias se reemplazan.", True),
         funcion("buscar_reemplazar", [["Mate mate"], "Mate", "cafe"], ["cafe mate"], "replace distingue mayusculas de minusculas.", True),
         funcion("buscar_reemplazar", [[], "a", "b"], [], "Una entrada vacia debe devolver otra lista vacia.", True)],
        ["Dibuja el recorrido: lista original -> una frase -> frase nueva -> lista resultado.", "Crea una lista nueva antes del for; agrega cada reemplazo.", "El return debe estar fuera del bucle."], starter="def buscar_reemplazar(lista, palabra, reemplazo):\n    pass\n")

EMAILS = [("juan@gmail.com", True), ("maria.lopez@utn.edu.ar", True), ("correo@dominio.com.ar", True),
          ("usuario@@gmail.com", False), ("gmail.com", False), ("juan @gmail.com", False), ("juan\t@gmail.com", False),
          ("@gmail.com", False), ("juan@gmail", False), ("juan@.com", False), ("juan@gmail.c", False),
          (".juan@gmail.com", False), ("juan@gmail.com.", False), ("", False)]
agregar("12 / Practica del parcial", "Parcial 2: validar un email",
        ["Un validador puede descartar casos con return False y devolver True solo al superar todas las reglas. No se trata de validar todos los emails posibles, sino esta consigna.",
         "find('.') devuelve la posicion del primer punto o -1 si no existe. rsplit('.', 1) separa una vez desde la derecha. isspace() detecta espacios, tabulaciones y saltos de linea. startswith() y endswith() comprueban extremos."],
        'dominio = "escuela.edu.ar"\nprint(dominio.find("."))\nprint(dominio.rsplit(".", 1))\nprint(" ".isspace())',
        'Define validar_email(email). Reglas: exactamente una @; usuario no vacio; dominio con texto antes del primer punto; al menos un punto despues de @; al menos 2 caracteres tras el ultimo punto; ningun espacio en blanco; no empezar ni terminar con @ o . . Devuelve un booleano.',
        [funcion("validar_email", [email], valid, "Comprueba las siete reglas en orden. Evita separar con @ antes de verificar que hay exactamente una.") for email, valid in EMAILS],
        ["Descarta primero la cantidad incorrecta de arrobas y los espacios en blanco.", "Separa usuario y dominio. En el dominio, el primer punto debe tener una posicion mayor que 0.", "Revisa la longitud de la extension despues del ultimo punto. True va al final."], starter="def validar_email(email):\n    pass\n")

NUMBER_CASES = []
for values in [[4, 7, 2, 9, 1, 5, 8, 3, 6], [-4, -7, -2], [5, 5, 6], [3]]:
    NUMBER_CASES.extend([
        funcion("calcular_extremos", [values], (max(values), min(values)), "Devuelve una tupla: primero el mayor y despues el menor.", True),
        funcion("ordenar_lista", [values], sorted(values), "Ordena una copia sin alterar la entrada.", True),
        funcion("filtrar_mayores_a_cinco", [values], [number for number in values if number > 5], "Conserva el orden original de los numeros estrictamente mayores a 5.", True)])
agregar("12 / Practica del parcial", "Parcial 3: analizar numeros",
        ["Separar responsabilidades simplifica las pruebas: una funcion busca extremos, otra ordena y otra filtra.",
         "return mayor, menor devuelve una tupla con dos valores. Para extremos se garantiza una lista no vacia. La lista original se conserva en las tres funciones."],
        'def primero_y_ultimo(datos):\n    return datos[0], datos[-1]\n\nprimero, ultimo = primero_y_ultimo([4, 8, 2])\nprint(primero, ultimo)',
        'Define calcular_extremos(numeros), ordenar_lista(numeros) y filtrar_mayores_a_cinco(numeros). Devuelve respectivamente (mayor, menor), una copia ordenada y los mayores a 5 en su orden original. Usa bucles, sin max(), min(), sorted() ni sort().',
        NUMBER_CASES,
        ["Resuelve y prueba una funcion a la vez; las demas pueden quedar con pass mientras practicas.", "Para extremos toma numeros[0]. Para ordenar usa una copia e intercambios de vecinos.", "Para filtrar, crea una lista vacia y agrega los valores mayores a 5."],
        starter="def calcular_extremos(numeros):\n    pass\n\ndef ordenar_lista(numeros):\n    pass\n\ndef filtrar_mayores_a_cinco(numeros):\n    pass\n", rules=[SIN_ATAJOS, estructura("For", "Los resultados se calculan recorriendo los valores.")])

GAME_CASES = [
    {"kind": "game", "title": title, "call": {"function": "jugar_adivinanza", "args": [secret]},
     "inputs": inputs, "expected": {"won": won, "lost": not won}, "why": why}
    for title, secret, inputs, won, why in [
        ("Victoria con letras mayusculas", "sol", ["S", "O", "L"], True, "Normaliza las letras con lower para aceptar mayusculas."),
        ("Victoria con letras repetidas en la palabra", "ala", ["a", "l"], True, "Una letra descubierta revela todas sus apariciones."),
        ("Cinco fallos terminan la partida", "sol", ["a", "b", "c", "d", "e"], False, "La quinta letra incorrecta debe terminar el juego y revelar la palabra."),
        ("Entradas invalidas no consumen errores", "sol", ["", "12", "ab", " ", "3", "a", "b", "c", "d", "s", "o", "l"], True, "Las entradas invalidas se descartan sin sumar errores; cuatro fallos todavia permiten ganar."),
        ("Una letra incorrecta repetida no cuenta dos veces", "sol", ["a", "a", "b", "b", "c", "c", "d", "d", "s", "o", "l"], True, "Registra tambien las letras incorrectas y no vuelvas a contarlas.")]]
agregar("12 / Practica del parcial", "Parcial 4: el juego completo",
        ["El programa principal coordina el juego; juego.py contiene las funciones auxiliares. Una lista registra letras intentadas y un contador registra errores.",
         "while errores < 5 and not palabra_completa(...) continua mientras queden oportunidades y letras pendientes. Una entrada invalida o repetida usa continue antes de sumar errores.",
         "if __name__ == '__main__': permite iniciar una partida al ejecutar el archivo, pero no al importarlo para pruebas. Las pruebas llaman jugar_adivinanza con distintas palabras."],
        'def iniciar():\n    print("Comienza la practica")\n\nif __name__ == "__main__":\n    iniciar()',
        'Completa las funciones auxiliares en juego.py con docstrings de una linea. En solucion.py importa ambas y define jugar_adivinanza(palabra_secreta): pide una letra por turno, acepta mayusculas, avisa si la entrada es invalida o repetida sin sumar errores, muestra progreso tras cada intento y termina al completar la palabra o llegar a 5 errores. En victoria incluye Ganaste; en derrota incluye Perdiste y la palabra. Sin dibujo. Incluye un bloque principal para jugar con python.',
        GAME_CASES + [funcion("mostrar_progreso", ["sol", ["s"]], "s _ _", "El progreso debe usar guiones bajos separados por espacios."),
                      funcion("palabra_completa", ["sol", ["s"]], False, "Una palabra incompleta no debe terminar la partida.")],
        ["Primero termina y valida las funciones auxiliares en juego.py.", "Crea letras_intentadas y errores antes del while. Valida longitud, isalpha y repeticion antes de registrar la letra.", "Despues del bucle, distingue victoria de derrota. Proba tambien cinco errores y una entrada repetida."],
        starter="from juego import mostrar_progreso, palabra_completa\n\ndef jugar_adivinanza(palabra_secreta):\n    pass\n\nif __name__ == '__main__':\n    jugar_adivinanza('python')\n",
        module="def mostrar_progreso(palabra_secreta, letras_intentadas):\n    pass\n\ndef palabra_completa(palabra_secreta, letras_intentadas):\n    pass\n", inputs="p\ny\nt\nh\no\nn",
        rules=[estructura("While", "La partida repite turnos hasta una condicion de salida."),
               {"kind": "module", "names": ["mostrar_progreso", "palabra_completa"], "title": "Importar auxiliares con docstrings desde juego.py", "why": "Las funciones auxiliares pertenecen a un modulo separado."}])