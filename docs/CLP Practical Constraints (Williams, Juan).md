CLP Practical Constraints (continuación).
==

Resumen
----

Continuar con el trabajo realizado por Adolfo y Sebastián.

El objetivo del trabajo original era el de incorporar restricciones prácticas a un solver para problemas de **carga de contenedores**.

El objetivo de esta continuación sería el de ajustar los componentes del solver (e.g., función de evaluación de acciones, generación inicial de bloques) para mejorar el desempeño tomando en cuenta estas restricciones. 

Links de interés:

> - [2017 - VCS: A new heuristic function for selecting boxes in the single container loading problem](ttps://drive.google.com/file/d/1q6AP892-bcuZ1LzkxNJmjHw-HVsfgwG4/view)
> - [2021 - Practical Constraints in the Container Loading Problem: Comprehensive Formulations and Exact Algorithm](https://drive.google.com/file/d/140Cc5hsvMkzfqlAbjS8LQZFJBCIu1YrL/view)
> - [202X - A MILP Approach for the Multi-Drop Container Loading Problem](https://drive.google.com/file/d/10DjpuIa6jcbinnr6foMSsag67MQvvm_w/view)
> - [Memoria de Adolfo y Seba](https://drive.google.com/file/d/15Hz83as3dUzeZaU2c3hhjcY_9ujwsBkG/view?usp=sharing).

TODO
--

### Antes de comenzar
- Leer papers, y este documento.
- Echar un vistazo a archivos de código principales (main, estado, funciones para cálculo de restricciones blandas).


### Williams

**Objetivo:** Mejorar implementaciones de las **restricciones blandas** (multi-drop, load balance y complete shipment).

- **Definir propuesta de restricciones duras y blandas basadas en las del documento y de los papers para conversar en próxima reunión.**
- Definir detalladamente cómo calcular y utilizar las distintas restricciones en las siguientes secciones del algoritmo.
	- Función de evaluación para Greedy par evaluar bloques
	- Al evaluar un estado
	- Al construir los bloques
- Partiendo como base de los algoritmos implementados actualmente, repararlos/modificarlos/optimizarlos para que se comporten de la manera deseada.

----

### Restricciones Duras

**Conflicting items+Separation of Item:** 
Tabla de conflictos.
Artículos deben transportarse en distintos contenedores.

**Load Bearing:**
Límite de peso que puede soportar cada caja.

**Cargo Stability (horizontal):**
Mínimo área de contacto de la base de cada caja. La m´nima área es definida por la instancia y es igual para todas las cajas. (% de la base)

**¿Estabilidad vertical?**
Estudiar que ocurre entre entregas.

El área de contacto de las caras verticales de la caja.

Orden establecido de entregas.

**MultiDrop:**
No hay movimientos adicionales entre clientes.

Puede ser considerada por forma de llenado.

### Restricciones blandas

**Complete Shipment** Se prioriza pedidos completos. --> 2021.

**Load Balance**

- Priorizar cajas pesadas más abajo (tanto en generación de bloques como al llenar el contenedor).


----





### Juan Ávila

**Objetivo:** Proponer un formato adecuado para las instancias e implementar un algoritmo para trabajar con múltiples contenedores.

- Integrar algoritmo para múltiples contenedores que se basa en particionamiento de cajas previo.
- Diseñar formato de instancias que permita trabajar con MCLP y restricciones prácticas. 
- Diseñar generador de instancias para problema MCLP con restricciones prácticas.

### TODO

- Describir criterio de selección de cajas para cada contenedor.
Trabajar en pseudocódigo para multiple-CLP.
- Comenzar a diseñar formato para instancias considerando las restricciones prácticas y múltiples contenedores. **Revisar si ya existe este formato en estado del arte.**


Multiple CLP
--
````python
def multiple_clp(C, TU):
    for each c in customers:
       if vol(boxes(c)) > available_volume...
             ...
             ...
             clp_solver(boxes, TU_i)
     return TUs
````     


Notas sobre las restricciones
---

### Restricciones duras

Se incorporan a momento de evaluar las acciones para un estado. Si la restricción no se cumple para la acción, simplemente no se considera

* **Conflicting items.** Se evalúa que las **cajas del nuevo bloque** mantenga distancia adecuada con los elementos en conflicto. Para una implementación eficiente se puede agregar un mapa `type2simple_aabb` que asocie cada tipo de caja con la lista de cajas de ese tipo ya ubicadas en el contenedor.

* **Load bearing.** Se considera que peso de cajas se distribuye proporcional al **área de contacto** de las cajas que se encuentran justo debajo.
Para evaluar una acción se verifica que las cajas **debajo del bloque** que se agrega respeten la restricción.
Para evitar buscar intersecciones de cajas, cada caja colocada o `simple_aabb` puede mantener la lista de simple_aabbs que se encuentran justo por debajo junto al área de contacto. Esta lista se crea al momento de crear un bloque o agregarlo en el contenedor.

* **Cargo stability.** Para cumplir esta restricción, el área de contacto de las cajas inferiores del nuevo bloque debe ser mayor a un $\alpha$%. Esta area se puede obtener directamente usando la estructura especificada más arriba.

### Restricciones blandas
Se incorporan directamente al momento de evaluar una solucióna modo de penalización, por lo que la función objetivo quedaría:

$\max V(s) - A*MD(s) - B*CS(s) - C*LB(s)$

donde $V(s)$, corresponde al volumen usado por la solución, $MD$ corresponde al *multidrop*, $CS$ a *complete shipment* y $LB$ al *load balance*.

* **Multidrop**: Tiene que ver con la cantidad de movimientos de cajas *adicionales* que se necesitaría realizar para extraer los items de los clientes. El multidrop para un cliente $i$, se estima considerando el número de cajas que se encuentran arriba, y al frente de todas las cajas del cliente $i$ que correspondan a clientes mayores a $i$. Para un cálculo efectivo, cada `simple_aabb` puede guardar la lista de `simple_aabbs` que la están bloqueando. En la función, el término $MD$ puede ser una sigmoide $(c_1,c_2)$.
![image](https://i.imgur.com/AsVnj6w.png)

* **Complete shipment**: Cada caja en la instancia está asignada a un cliente en particular. Complete shipments es el cuociente entre la *cantidad de entregas completas* correspondientes a la solución vs. la cantidad de entregas totales. Se podría sumar el **máximo porcentaje de pedido no completado** (al cuadrado?).
* **Load balance**: Tiene que ver con lo estable que debería estar el contenedor en vista de un futuro traslado. Como factor determinante se considera el ángulo de volcamiento que se genera con el vector que pasa por el centro de masa y un vértice inferior del contenedor y el eje horizontal. El término LB podría ser una sigmoide $(c_1, c_2)$

### ¿Cómo *ayudar* al greedy a satisfacer las restricciones?


* **Conflicting items:** premiar acciones que coloquen items del mismo tipo cerca. Premiar/castigar proporcional a cantidad de cajas por colocar en conflicto.
* **Load bearing**. Premiar cajas que soportan más peso
* **Cargo stability**. Premiar cajas con mayor área
* **Multidrop**. Premiar cajas de clientes con mayor prioridad
* **Complete shipment**. Premiar pedidos más completos
La estrategia podría asignar configuraciones de pesos de manera aleatoria por simulación a los criterios para así obtener mayor diversidad de soluciones.
También, se podría evaluar un sampling aleatorio de acciones.


Ejecución del solver
---

Puedes ejecutarlo remotamente en el servidor.

**Conexión al servidor:**
````
ssh 158.251.88.197
login: practica
pass: ScHrOdL223
````


**Descarga**
````
mkdir clp_pc_williams
cd clp_pc_williams
git clone https://github.com/rilianx/Metasolver.git .
git checkout -t origin/practical_constraints
````

**Compilación**
````
make BSG_CLP
````

**Ejecución de ejemplos**

Instancia *sin atributos prácticos*, es decir una instancia que sólo considera dimensiones de las cajas (ni pesos, ni parámetros adicionales).

````
./BSG_CLP problems/clp/benchs/BR/BR8.txt -i 0 -t 10
````

Instancia con atributos prácticos como peso, tipo, peso que soporta, etc.

````
./BSG_CLP problems/clp/benchs/BRpc/BRrwtm0.txt -i 9 -t 1 -f BRpc
````

Notar que la instancia se resuelve de la misma forma que la anterior (intentando maximizar el volumen), sin embargo imprime los valores de *multidrop*, *ángulo de volcamiento* y factor de *completeShipment*:
````
multidrop:117
angle:0.78049876
completeShipment:0.068342204
````


Notas sobre el código 
---
Recomiendo usar Visual Studio Code para trabajar en el código de manera remota ya que permite conectarse mediante SFTP (luego de instalar el plugin).

Para entender un poco en que consiste deberías primero leer el paper [2017 - VCS: A new heuristic function for selecting boxes in the single container loading problem](ttps://drive.google.com/file/d/1q6AP892-bcuZ1LzkxNJmjHw-HVsfgwG4/view).

### main

El main se encuentra en [main_clp.cpp](https://github.com/rilianx/Metasolver/blob/practical_constraints/problems/clp/main/main_clp.cpp). 

Aquí se construye la estrategia (el evaluador vcs, el greedy, el algoritmo BSG y finalmente una estrategia que llama al BSG iterativamente cada vez duplicando el esfuerzo DE):

![image](https://i.imgur.com/0M8Fn65.png)

Luego se corre la estrategia:

![image](https://i.imgur.com/cC3sGU6.png)

### CLP_state

Una de las clases más importantes es la del estado o nodo. Esta clase se declara [aquí](https://github.com/rilianx/Metasolver/blob/practical_constraints/problems/clp/clpState.h)

Además de tener muchas funciones, los miembros de esta clase son los siguientes:

![image](https://i.imgur.com/lfX7URV.png)

El contenedor con las cajas/bloques que han sido colocados (`cont`), las cajas que aún falta colocar (`nb_left_boxes`) y una lista de bloques que se puede construir con las cajas restantes (`valid_blocks`).

La función para evaluar estados se llama `get_value()` y lo único que hacer por ahora es obtener el volumen ocupado de cajas dentro del contenedor (en porcentaje).

![image](https://i.imgur.com/RzUlQze.png)

### Lectura de instancias

- La lectura de archivos se realiza en `clpState.cpp`
![image](https://i.imgur.com/lVnJ8C5.png)

**Formato de instancias**
````
n_instancias
id_instancia seed
L W H
Wmax
n_boxes
id_box l rot_l w rot_w h rot_h n w type w_support alpha beta gamma
...
````

### Restricciones duras y blandas

- Restricciones blandas se encuentran implementadas en el archivo [`clpState_pc.cpp`]. Estas restricciones son:
	- multidrop
	- load balance (angle)
	- complete shipment

- Restricciones duras aun las tengo que copiar del código de Adolfo y Sebastián en `VCS_Function::eval_action`.
![image](https://i.imgur.com/DUVnuvl.png)
<!--stackedit_data:
eyJoaXN0b3J5IjpbNTcyMTkzMTg0LC0xMzcwMDQ3MDA2LC0xMT
IyMTc0NDc2LDE2Njk5Nzc0NjgsLTMzNzg4ODk5NiwyMDY2NDUw
NTc2LC0xNDIzMDM0OTY1LDE3Njg5MjQxODIsLTcyMDE2NjE4My
wtNjA2MTE1NDg4LDE2ODY5MzE1MDYsNjExNjUyNDc5XX0=
-->