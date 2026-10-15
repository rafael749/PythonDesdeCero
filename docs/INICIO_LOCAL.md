# Ejecutar el proyecto localmente

## Desde el chat de VS Code

1. Clona el repositorio o descarga el ZIP y extraelo completamente.
2. Abre la carpeta que contiene `servidor.py` en VS Code, no un archivo aislado.
3. Revisa el proyecto y habilita la confianza del espacio de trabajo solo si confias en su contenido.
4. Abre GitHub Copilot Chat con una cuenta habilitada y selecciona el modo **Agente**.
5. Escribe **ejecutar proyecto localmente** y aprueba los comandos que correspondan.

El repositorio incluye instrucciones para reconocer esa solicitud. Como acceso
explicito, tambien podes escribir **/ejecutar-proyecto-localmente** en el chat.
Si no aparece el comando o no se cargan las instrucciones, actualiza VS Code y
Copilot, comprueba que las personalizaciones del repositorio esten habilitadas
y adjunta esta guia al chat.

Esto guia al asistente; no es un instalador automatico ni garantiza que todos
los chats o editores interpreten la frase. Sin herramientas, permisos o modo
Agente, el asistente solo podra indicarte los pasos manuales.

## Requisitos

| Componente | Necesidad |
| --- | --- |
| Python | Python 3.11 o posterior recomendado, en una version compatible con tu sistema operativo. |
| Navegador | Una version actual de Chrome, Edge, Firefox o Safari con JavaScript, WebAssembly y Web Workers habilitados. |
| Internet | Necesario para descargar Pyodide al iniciar las practicas; tambien para fuentes e iconos externos. |
| Git | Solo para clonar o actualizar. No hace falta si descargaste el ZIP. |
| VS Code y Copilot | Solo para el inicio asistido por chat. No son necesarios para ejecutar manualmente. |

El servidor no necesita paquetes externos: **no hay que ejecutar pip install
ni npm install**. No requiere Node.js, una base de datos, un archivo `.env`
ni claves de API. Pyodide se descarga en el navegador; no se instala con pip.

Las pruebas del proyecto se ejecutaron en macOS con Python 3.9.6. Eso no
significa que convenga instalar esa version antigua ni que se haya certificado
cada combinacion de sistema y version. Para una instalacion nueva usa una
version mantenida; en cualquier equipo, las pruebas de abajo permiten verificar
el interprete elegido. Consulta los requisitos del instalador si tu sistema
operativo es antiguo o si usas una arquitectura distinta (ARM64 o x64).

## Instalar Python si falta

- **Windows:** usa el instalador o gestor oficial de [python.org/downloads/windows](https://www.python.org/downloads/windows/). Comprueba la version de Windows y la arquitectura admitidas. Abre una terminal nueva tras instalar. El comando `py -3 --version` suele comprobar la instalacion; si solo funciona `python`, usa ese comando en los pasos siguientes. Si se abre la Microsoft Store en lugar de Python, el alias no confirma una instalacion: instala Python y vuelve a comprobarlo.
- **macOS:** usa [python.org/downloads/macos](https://www.python.org/downloads/macos/) o, si ya utilizas Homebrew, `brew install python`. Comprueba que la version elegida admita tu macOS. No reemplaces el Python que usa el sistema operativo. Verifica con `python3 --version`.
- **Linux:** identifica la distribucion y usa su gestor de paquetes. En Debian/Ubuntu normalmente se instala el paquete `python3` con `sudo apt install python3`; en Fedora, con `sudo dnf install python3`. Son alternativas, no comandos para ejecutar juntos. El paquete disponible depende de la version de la distribucion. Si no ofrece una version mantenida, revisa la documentacion de tu distribucion; no elimines ni reemplaces su Python de sistema.

Una instalacion puede pedir permisos de administrador o reiniciar la terminal.
Las contrasenas se escriben directamente en el instalador o terminal, nunca en
el chat. No ejecutes scripts de instalacion de sitios desconocidos.

## Inicio manual

Abre una terminal dentro de la carpeta extraida o clonada, donde esta
`servidor.py`. No abras directamente los HTML: necesitan el servidor local.

**Windows (PowerShell o terminal):**

```powershell
py -3 --version
py -3 -m unittest test_practica test_laboratorio -v
py -3 servidor.py --open
```

Si el interprete comprobado es `python`, reemplaza `py -3` por `python` en
los tres comandos. No es necesario modificar la politica de PowerShell.

**macOS o Linux:**

```sh
python3 --version
python3 -m unittest test_practica test_laboratorio -v
python3 servidor.py --open
```

En macOS tambien existe el acceso `Abrir laboratorio.command`. Si el ZIP
no conserva su permiso de ejecucion, usa los comandos anteriores.

El servidor informa la direccion real, normalmente `http://127.0.0.1:8765`.
Abri **http://127.0.0.1:8765/aprender** para empezar desde cero o la direccion
sin `/aprender` para el laboratorio del parcial. Si el puerto estaba ocupado,
el servidor elige otro: usa el numero que imprime, no asumas que sigue siendo
8765. Si no se abre el navegador automaticamente, abre ese enlace manualmente.

Manten la terminal abierta. Para detenerlo usa `Ctrl+C`. El servicio escucha
solo en tu equipo; esta guia no lo publica en Internet ni configura Render.
Los borradores pertenecen a ese navegador y a esa direccion/puerto. Un cambio
de puerto no borra el progreso anterior, pero hace que veas otro almacenamiento.

## Procedimiento para el agente

Cuando el usuario pida **ejecutar proyecto localmente**:

1. Confirma la raiz que contiene `servidor.py`, `curso.py` y `aprender.html`. Revisa las instrucciones del repositorio y el estado local sin modificar ejercicios ni descartar cambios del usuario.
2. Identifica sistema operativo, version y arquitectura con las herramientas del entorno o comandos de solo lectura: `sw_vers` y `uname -m` en macOS; `/etc/os-release` y `uname -m` en Linux; informacion del sistema de PowerShell en Windows. No deduzcas el sistema solo por el nombre de una carpeta.
3. Descubre un interprete disponible: `py -3` o `python` en Windows, `python3` en macOS/Linux. Comprueba su version, ruta y arquitectura con `--version` y `-c "import sys, platform; print(sys.executable); print(sys.version); print(platform.machine())"`. Si el editor ofrece herramientas para consultar el interprete seleccionado, usalas; el Python de la terminal puede ser distinto. Reutiliza un entorno existente valido sin recrearlo.
4. Si falta Python, su instalacion esta rota o no puede ejecutar el proyecto, explica el problema y propone una version mantenida compatible con el sistema detectado usando las fuentes oficiales. Pide permiso antes de instalar software. Si se necesita elevacion o una contrasena, deja esa instalacion al usuario y retoma tras su confirmacion. No pidas secretos en el chat, no uses sudo interactivo desde herramientas y no cambies el Python del sistema. Si el sistema es demasiado antiguo, informa el bloqueo sin forzar un instalador incompatible.
5. Confirma los requisitos actuales leyendo el servidor y esta guia. En esta version no hay dependencias de pip ni npm. No crees requirements.txt, un entorno virtual o package.json vacios solo para iniciar el proyecto. Si el repositorio cambia y agrega dependencias declaradas, sigue sus instrucciones reales antes de instalarlas.
6. Comprueba si ya hay una instancia de este proyecto iniciada. No mates procesos para liberar puertos. Si puedes confirmar que una instancia responde correctamente y corresponde a este proyecto, reutilizala. No confundas cualquier servicio en el puerto 8765 con este laboratorio.
7. Ejecuta `-m unittest test_practica test_laboratorio -v` con el interprete verificado desde la raiz. Si falla, informa el error concreto; no declares el entorno listo ni modifiques ejercicios para ocultar un problema de instalacion. Distingue entre incompatibilidad del entorno y cambios locales del usuario.
8. Inicia `servidor.py` como proceso persistente usando el interprete verificado y la ruta absoluta al archivo, para no depender del directorio inicial de una terminal nueva. Puedes agregar `--open` si hay escritorio disponible. No ejecutes un segundo servidor si ya confirmaste una instancia utilizable. No uses un puerto fijo si el servidor informa otro.
9. Lee la direccion informada y verifica por HTTP que `/aprender` devuelve la pagina del curso y `/api/curso` devuelve el listado JSON de ejercicios. Abre la pagina con las herramientas del navegador cuando esten disponibles. Informa si no pudiste probar la descarga de Pyodide; la disponibilidad del servidor no demuestra que el navegador pueda acceder al CDN.
10. Entrega el enlace real terminado en `/aprender`, el sistema y la version de Python verificados, el resultado de las pruebas y como detener el servidor. Dejalo funcionando. No hagas commit, push, despliegue ni instalaciones globales adicionales como parte de este flujo.

## Problemas frecuentes

- **Python no se reconoce:** abre una terminal nueva tras instalar y comprueba el comando correcto para tu sistema.
- **La pagina abre pero no ejecuta practicas:** verifica Internet y el acceso a `cdn.jsdelivr.net`; una red o extension puede bloquear Pyodide.
- **No aparece el progreso:** usa el mismo navegador y el mismo puerto. No borres sus datos para intentar recuperarlo.
- **No hay navegador en el equipo:** el servidor puede iniciar sin `--open`; usa un entorno con navegador para la interfaz. Una sesion remota no comparte automaticamente su localhost con tu computadora.