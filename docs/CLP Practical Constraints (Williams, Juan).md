CLP Practical Constraints (continuación).
--


**TODO**
- Terminar algoritmo de agrupamiento de cajas :ok:


---

**Modificaciones a clase block**
Clase **Block** tiene lista `AABBList* boxes` conteniendo todas las cajas (objetos AABB) y sus ubicaciones dentro del contenedor.
En el main hay un ejemplo de como reccorer la lista:
![image](https://i.imgur.com/gOW8cw2.png)

Además, cada AABB (box), almacena un puntero al `BoxShape` asociado, una lista con los AABBs (boxes) que lo "soportan" dentro del bloque, una variable que almacena la superficie en contacto (`bottom_contact_surface`) y otra variable que indica el peso soportado (`supported_weight`). Ambas variables se actualizan automáticamente al agregar bloques en otro bloque (el contenedor también es un bloque).

Por último, agregué la función `validate_BCS_and_LB()` para validar si al agregar un bloque dentro del bloque actual, se siguen cumpliendo las restricciones de *estabilidad vertical* y *load bearing*.

La función es usada dentro de VCS:
![image](https://i.imgur.com/U4Ee2Cc.png)

Y al construir bloques (`create_new_blocks`).

**Agregué id a cliente**
Y cree una nueva instancia . Ahora se ejecuta así:
````
./BSG_CLP problems/clp/benchs/BRpc2/BR8pc.txt -i 0 -t 1 -f BRpc --min_fr=0.98
````


**TODO**

- [ ] Modificar visualizador para colorear cajas de los clientes
 
**General Strategy (1)**
- [ ] Implementar algoritmo MCLP-BSG de paper

**Block Generator (2):**
- [ ] When vertical blocks are generated: **maximize the weight supported by the resulting block**: minimum between the upper boxes supported weight and the lower box supported weight minus the weight of the upper block.
- [X] Verify the vertical stability constraint
- [ ]  Verify the horizontal stability constraint

**Selecting location of the next block (3)**
- [X] Place the block in front or above the already placed blocks. Back and bottom locations are preferred.

**Selecting the next block (4)**
- [X] **Verify the vertical stability constraint** for each evaluated block.
- [X] **Verify the load bearing constraint** for each evaluated block. Compute the supported weight by blocks just below b.
- [ ] **Verify the horizontal stability constraint**, i.e., the back surfaces of the boxes inside the block should be supported by the already placed boxes,
- [ ] **Prioritize heavy blocks**
- [ ] **Compute the overturning angle**
- [X] **Verificar peso máximo soportado por el contendor**

**Evaluating solutions (5)**
- [ ] **Compute a factor for the overturning angle constraint**
- [ ] **Compute a factor for the complete shipment constraint**

### Blocks

Cada bloque tiene:
- Contenedor de AABBlocks
- Contenedor de AABBoxes

Luego, cada AABBox tiene
* supporting AABBoxes:
* supported_weight
* bottom_contact_surface

### Supported Weight

Cada vez que se inserta una caja, propagar recursiva y proporcionalmente el peso a las *supporting boxes*.


### Error?
![image](https://i.imgur.com/FI4c9J9.png)



---




**Observaciones presentación**
- Organizar mejor
- Solución más óptima x
- Explicar mejor el problema, restricciones prácticas
- Explicar procesos y momentos del BSG
- Adaptación de BSG a múltiples contenedores -> explicar con más claridad (grupos, clientes?)
- Mostrar tabla
- Resultados preliminares: qué restricciones se consideraron? Colores para cada cliente
- Siendo que se consideran más restricciones. A qué se debe que mejore la distribución?

---


### Momentos

![image](https://i.imgur.com/ZmXRUFK.png)

Resumen
----

[overleaf](https://www.overleaf.com/6689583734gwrmtknhtzmt)

El objetivo del trabajo original era el de incorporar restricciones prácticas a un solver para problemas de **carga de contenedores**.

El objetivo de esta continuación sería el de ajustar los componentes del solver (e.g., función de evaluación de acciones, generación inicial de bloques) para mejorar el desempeño tomando en cuenta estas restricciones. 

Links de interés:

> - [2017 - VCS: A new heuristic function for selecting boxes in the single container loading problem](https://drive.google.com/file/d/1q6AP892-bcuZ1LzkxNJmjHw-HVsfgwG4/view)
> - [2021 - Practical Constraints in the Container Loading Problem: Comprehensive Formulations and Exact Algorithm](https://drive.google.com/file/d/140Cc5hsvMkzfqlAbjS8LQZFJBCIu1YrL/view)
> - [202X - A MILP Approach for the Multi-Drop Container Loading Problem](https://drive.google.com/file/d/10DjpuIa6jcbinnr6foMSsag67MQvvm_w/view)
> - [Memoria de Adolfo y Seba](https://drive.google.com/file/d/15Hz83as3dUzeZaU2c3hhjcY_9ujwsBkG/view?usp=sharing).
> - [A biased random key genetic algorithm for 2D and 3D bin packing problems](https://sci-hub.se/10.1016/j.ijpe.2013.04.019)
> [The exact solutions of several types of container loading problems (2020)](https://www.researchgate.net/profile/Jose-Pecora-Jr/publication/337895771_The_exact_solutions_of_several_types_of_container_loading_problems/links/5f20130592851cd5fa4e3c7f/The-exact-solutions-of-several-types-of-container-loading-problems.pdf)

Habla de los pallets:
> - [2019 - A GRASP algorithm for multi container loading problems with practical constraints](https://link.springer.com/content/pdf/10.1007/s10288-018-0397-z.pdf): Colocar pallets en camiones. Dimensiones de pallets un poco restrictivas por lo que no se ajustan a nuestros bloques.









----

### Restricciones Duras

**Conflicting items+Separation of Item:** 
Tabla de conflictos. Artículos deben transportarse en distintos contenedores.

> Debería considerarse al momento de repartir los elementos entre distintos TUs


**Load Bearing:**
Límite de peso que puede soportar cada caja.

> Debería considerarse:
> * En función de evaluación de bloques(mayor soporte abajo)
> * Al construir los bloques  -> máximo soporte del bloque.

**Cargo Stability (horizontal):**
Mínimo área de contacto de la base de cada caja. La mínima área es definida por la instancia y es igual para todas las cajas. (% de la base)
> Debería considerarse al construir los bloques
> Calcular en función de evaluación de bloques como restricción dura

**¿Estabilidad vertical?**
Estudiar que ocurre entre entregas.

El área de contacto de las caras verticales de la caja.

Orden establecido de entregas.

**MultiDrop:**
No hay movimientos adicionales entre clientes.

> Llenar contenedor en orden de entrega.

### Restricciones blandas

**Complete Shipment** Se prioriza pedidos completos. --> 2021.
> Ordenamiento previo

**Load Balance**
Tomar en cuenta el peso del contenedor
Calcular ángulo de volcamiento

> Construir bloques con cajas más pesadas abajo
> Colocar bloques más pesados abajo/centro
> Evaluar a medida que se colocan los bloques 




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


Tipo de carga
Contenedor riffer
Balance del contenedor (punto de gravedad)
Soporte de cajas
Contenedores abiertos (neumáticos)

CPMP
Secuenciar contenedores
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTQzMDM3MjExNiwzMTA5Nzk1ODUsMTI5Nj
AyMzIxMCwtMjA4NTM0Njc4LC0xOTc3NTMwNDA4LDE1MzgzMTMx
NjYsLTE5MTA0MTQ0OTQsMTYwMTA5MzEyNSwxMjg2NjE1NzM1LC
0yMDI3MjUxOTUzLC02Mjk0OTMyNCwtMTQxNzcwMDE4MCwxNDE3
MTY4OTIsLTcwNzI5NDU2MiwtMTA3MjI2MjE0Miw4MzE3OTI1OT
IsLTE3ODcyODc3NTAsMTYzNDIwNDkzMCwxNTU3MzQ4NTAyLC0y
MTA2NzAzMzkyXX0=
-->