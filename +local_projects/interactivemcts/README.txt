------------------------------------------------- INICIAR EL CÓDIGO --------------------------------------------------
Usé Visual Studio para hacer este código. Para correr el código, ejecute el archivo main.py.
--------------------------------------------- DEFINICIÓN DE LOS ARCHIVOS ---------------------------------------------
1) Camera.py: actualiza el estado de la cámara (pantalla) y establece una posición X e Y

2) Function1.py: función que calcula la evaluación de cada nodo (puede ser modificada sin afectar el funcionamiento del programa)

3) Function2.py: función que calcula la evaluación de cada nodo (puede ser modificada sin afectar el funcionamiento del programa)

4) Graphics.py: detecta la posición del click en cada nodo (si apreta fuera del nodo, el programa se cierra) y ordena los nodos

5) Main.py: pide por consola datos iniciales y llama a graphics.py para dibujar el grafo

6) Node_manipulator.py: dibuja los nodos y les asigna propiedades como el color y el tamaño. En este archivo se imprime información 
al pasar por encima de los nodos y configurar el tamaño y color según las funciones del archivo properties.py

7) Node.py: Almacena los datos principales del nodo (Ahora: state.py (?))

8) NodeProp.py: Contiene atributos de la figura o dibujo del arbol 

9) Properties.py: contiene funciones que definen color y tamaño de los nodos segun su evaluación

10) Simulation.py: lee desde el simulador el resultado de una simulacion y guarda la información en el nodo correspondiente

11) Tree.py: organiza el arbol, asignando hijos y padre a cada nodo

12) Update.py: (***aun no está implementada***) al apretar afuera de un nodo se simulan los mejores N nodos, N veces

* ¿qué más debería agregar en el README?