### ** IMPORTANTE **

1. **Dividan su código en funciones más pequeñas y manejables**  
   Esto no solo hace que el programa sea más fácil de entender y depurar, sino que también les permite reutilizar partes del código cuando lo necesiten. Cada función debería tener una única responsabilidad.  
   Pregúntense: *¿Qué hace esta función? ¿Cumple solo con una tarea?*

2. **Usen siempre docstrings en sus funciones** (esto lo vamos a ver en módulo 3 y 4, ahora no hace falta)  
   Cada función debería empezar con un **docstring** que explique qué hace, qué parámetros recibe y qué devuelve.  
   Esto no solo es útil para ustedes cuando revisan el código meses después, sino también para otros programadores que lo lean.  

   Por ejemplo:  
   ```python
   def calcular_promedio(notas: list[int]) -> float:
       """
       Calcula el promedio de una lista de notas.
       :param notas: Lista de números enteros que representan las notas.
       :return: El promedio de las notas como un número flotante.
       """
       return sum(notas) / len(notas)
   ```

3. **Mejorar su código al siguiente nivel**  (idem anterior, lo vemos en módulo 3 y 4, no hace falta ahora)
   Comiencen a usar anotaciones de tipo para las funciones, como el ejemplo anterior. Nombrar los tipos ayuda a otros —y a ustedes mismos— a entender mejor cómo usar la función. Les facilitará detectar errores más rápido.

4. **Piensen antes de codificar**  
   Antes de escribir una sola línea de código, tómense un momento para planificar.  
   - Dibujen en papel un esquema de lo que quieren lograr.  
   - Visualicen cómo se conectarán las partes del programa.  

   Recuerden: *un poco de planificación al principio ahorra horas de frustración más adelante.*

5. **Usen herramientas como ChatGPT / Gemini / Claude para aprender, no para saltarse el proceso**  
   ChatGPT puede ser un gran apoyo cuando no entienden algo. Pero no caigan en el error de usarlo para resolver un problema sin pensar. Ustedes son los programadores, y entender el problema es parte de la solución.

6. **Comenten todo lo importante**  
   No tengan miedo de dejar comentarios que expliquen cómo pensaron las cosas.  
   Los comentarios son un puente entre ustedes y quien lea su código en el futuro, incluso si ese lector son ustedes mismos.  
   Recuerden: "No solo programamos para las máquinas, programamos para las personas."

7. **Sean conscientes de quienes vendrán después de ustedes**  
   En programación, siempre habrá alguien que tendrá que trabajar con su código. Tal vez un colega, un futuro compañero, o incluso ustedes mismos en seis meses. Ayuden a esas personas:  
   - Usen nombres claros y descriptivos para variables, objetos, funciones y métodos.  
   - Piensen en que su código cuente una historia clara y comprensible.

*piensen en su código como si fuera una carta que están escribiendo. Esa carta debe ser legible, comprensible y, sobre todo, funcional.*

** Suerte! ** 😊
