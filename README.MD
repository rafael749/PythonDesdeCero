# Parcial 01

## Inicio rápido al clonar o descargar

Abrí la carpeta del proyecto en **VS Code**, seleccioná **Agente** en Copilot
Chat y escribí:

> ejecutar proyecto localmente

También podés usar **/ejecutar-proyecto-localmente**. El repositorio incluye
instrucciones para comprobar el sistema operativo, la versión de Python y los
requisitos, ejecutar las pruebas e iniciar el laboratorio. Si falta Python,
el asistente debe pedir autorización antes de instalarlo. Requiere Copilot
habilitado, instrucciones del repositorio activas y permiso para ejecutar herramientas;
no es una instalación automática al descargar el proyecto.

**No se necesitan paquetes de pip ni Node.js.** Para una instalación nueva se
recomienda Python 3.11 o posterior compatible con tu sistema y un navegador
moderno. La primera ejecución de las prácticas necesita Internet para Pyodide.

Consultá [la guía de inicio local](docs/INICIO_LOCAL.md) para Windows, macOS y
Linux, instalación de Python, comandos manuales y solución de problemas.

## Laboratorio visual de Python

En macOS, hacé doble clic en **Abrir laboratorio.command** desde Finder.
Se abre el navegador y una ventana de Terminal que mantiene Python funcionando:
no necesitás escribir en ella, pero debe quedar abierta mientras usás el laboratorio.
Requiere Python 3 instalado y no necesita paquetes adicionales.

El laboratorio permite interactuar con los cuatro ejercicios, cambiar las entradas,
ver los resultados y recorrer las líneas ejecutadas con sus variables reales.
El botón de reproducción avanza automáticamente; las flechas y la barra permiten
examinar cada paso. El estado de las variables corresponde al momento **anterior**
a ejecutar la línea resaltada. Los retornos y las esperas de `input()` se distinguen.

Se importan los archivos originales sin modificarlos. Para adaptar `input()` al
navegador, cada turno reconstruye la partida usando los intentos anteriores;
el registro del juego incluye esa ejecución completa. Las palabras son visibles
porque se trata de una práctica de código, no de una partida a ciegas.
El validador de email aplica las reglas de la consigna, no una validación completa
de todas las direcciones posibles en Internet.

La lista numérica admite entre 1 y 25 enteros, de -10¹² a 10¹², para que las trazas
sean manejables y los resultados se representen exactamente en el navegador.
Las fuentes y los iconos de controles se descargan de Internet; el logo oficial
de Python se incluye localmente desde https://www.python.org/static/favicon.ico.
Los ejercicios se
ejecutan localmente. No se envían tus entradas a servicios externos.

Inicio alternativo: `python3 servidor.py --open`. El puerto predeterminado es 8765;
si está ocupado, se elige otro libre. Para detenerlo, cerrá su ventana de Terminal
o presioná `Ctrl+C`. Si editás las funciones de Python, reiniciá el laboratorio.

Pruebas: `python3 -m unittest test_laboratorio -v`.

## Aprender desde cero

La seccion **Aprender desde cero**, accesible desde el laboratorio, incluye
36 practicas distribuidas en 12 etapas. Empieza por `print`, variables y tipos;
continua con entradas, condiciones, textos, listas, bucles y funciones; termina
con modulos y los cuatro ejercicios del parcial.

Cada practica tiene teoria breve, un ejemplo distinto de la consigna, pistas
graduales y un editor. **Ejecutar** muestra la salida de tu programa con las
respuestas del campo Entradas (una por linea). **Validar solucion** usa los
casos del ejercicio, con entradas independientes de ese campo, y compara los
resultados obtenidos con los esperados. Cada comprobacion explica su motivo.
Los errores de Python incluyen una explicacion en castellano y su linea.
En las practicas con funciones, definir una funcion sin llamarla puede no
producir salida al ejecutar; la validacion si llama a esas funciones.

Los borradores, las entradas y el progreso se guardan en el navegador. No se
marca un ejercicio como completado hasta superar sus pruebas; modificar el
codigo obliga a validarlo de nuevo. El almacenamiento es local al navegador
y a la direccion/puerto: no se sincroniza entre equipos ni entre puertos.
En las practicas de modulos hay dos archivos virtuales, `solucion.py` y
`juego.py`; no reemplazan los archivos originales de la carpeta.

El codigo escrito por el alumno se ejecuta con **Pyodide 0.27.7** en un Web
Worker, no con `exec` en el servidor de la computadora. La primera ejecucion
descarga Python desde jsDelivr y requiere Internet. Cada ejecucion usa un
worker nuevo; **Detener** lo termina y hay un limite de 6 segundos de ejecucion
(la carga inicial tiene su propio limite). No se montan carpetas del equipo.
Esto no es un servicio de evaluacion resistente a codigo hostil: ejecuta solo
codigo propio o de confianza. Los programas pueden usar capacidades web
disponibles en Pyodide. La correccion usa reglas y casos deterministas, no IA,
y superar los casos no demuestra que una solucion cubra todas las entradas
posibles ni que su estilo sea el mejor.

La guia requiere el servidor local para cargar sus recursos, aunque Python
se ejecute en el navegador. Inicio: `python3 servidor.py --open`. Acceso:
`http://127.0.0.1:8765/aprender` (usa el puerto informado si cambia).
Pruebas de ambos espacios: `python3 -m unittest test_practica test_laboratorio -v`.

## 📬 Entrega

El parcial debe entregarse por mail a
[juan.pablo.sosa@istea.com.ar](mailto:juan.pablo.sosa@istea.com.ar) con el
asunto:

> **CDProgr1 | Parcial 01 | MIERCOLES | Apellido, Nombre**

📅 **Fecha límite:** miércoles 30 de Septiembre de 2026, 21:00 hs.

A medida que vaya corrigiendo cargo las notas en la intranet. Si querés una
devolución personalizada, pedímela.

> ⚠️ **Importante:** deben estar presentes para rendir el examen y avisarme
> cuando me envían el mail. Si no avisan que enviaron, no se tiene en cuenta.
> No corten la conexión hasta que confirme que el mail llegó.

Para consultas durante el examen abro un Meet aparte (link en el chat) para no
interrumpir a quienes están resolviendo. Entrar, consultar y salir.

---

## ✅ Recomendaciones

(Ver también el archivo [`Importante.md`](Importante.md))

- Leé **muy bien** el enunciado de cada ejercicio antes de empezar.
- Hacé un pseudocódigo o un diagrama de flujo para pensar la solución antes de
  escribir código.
- Pensá el **algoritmo** antes de tirar líneas.
- Dividí en **funciones pequeñas**, cada una con una sola responsabilidad, y
  llamálas desde el archivo principal.
- Resolvé primero que **funcione**; después refactorizá para que quede
  prolijo.
- En esa refactorización, evaluá si hace falta **validar la entrada del
  usuario**.
- La parte teórica (si la hubiera) podés escribirla como comentario o hacer
  que se imprima en pantalla al ejecutar el script.

---

## 📝 Ejercicios

### Ejercicio 1 — Buscar y Reemplazar en una Lista
Definí `buscar_reemplazar(lista, palabra, reemplazo)` que reciba una lista de
strings y devuelva una **nueva lista** donde todas las ocurrencias de `palabra`
estén reemplazadas por `reemplazo`.

### Ejercicio 2 — Validar Email
Definí `validar_email(email)` que retorne `True` si el email cumple **todas**
las reglas de formato indicadas en el archivo, o `False` en caso contrario.

### Ejercicio 3 — Análisis de una Lista de Números
Dada una lista de enteros, mostrar la lista original, su valor **máximo** y
**mínimo**, la lista **ordenada** de menor a mayor y los números **mayores
a 5**. **Sin usar** `sorted()`, `max()` ni `min()`: hay que recorrer la lista
con bucles.

### Ejercicio 4 — Juego de Adivinanza de Palabras con Módulo
Definí `jugar_adivinanza(palabra_secreta)` que implemente un juego tipo
ahorcado **sin dibujo**: el usuario ingresa letras de a una, se muestra el
progreso con guiones bajos y el juego termina al adivinar la palabra o tras
**5 errores** acumulados. Las funciones auxiliares deben estar en un módulo
separado `juego.py` con docstrings.

---

## 🎯 Puntaje

| Ejercicio | Puntos |
|:---------:|:------:|
| 1 | 25% |
| 2 | 25% |
| 3 | 25% |
| 4 | 25% |

**Aprobación con nota 4 = 60% bien hecho del examen.**

---

¡Suerte! 🍀
