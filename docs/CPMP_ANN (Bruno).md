Training an ANN for solving CPMP
==
La idea es entrenar una red para resolver el CPMP.
Para hacerlo se entrena la red usando estados->acciones presentes en resoluciones óptimas del problema.

TODO
---
- weight sharing (locality connected networks)
- terminar implementación
- ¿Qué tan modificable son las redes en keras? (ver arquitectura propuesta)

Pasos
--

**1. Generación de instancias**
Generar instancias 4 stacks x 4 contenedores (+2 espacios libres). Group value aleatorios entre 0 y 100.

**2. Generación de muestras**
Resolución óptima. Las muestras corresponden a todos los estados (x) con la acción correspondiente (y1,y2). Se pueden generar estados equivalentes haciendo intercambios entre stacks.

**3. Entrenamiento**
Usar red neuronal.
Se pueden entrenar dos redes: una que aprenda a seleccionar stacks de origen y otra que aprenda a seleccionar stacks de destino. 

La red de los stacks de destino debería recibir como entrada un estado modificado de tal manera que **siempre** la primera columna corresponda al stack de origen. Para esta red, la salida 0 no debería considerarse (stack destino = stack origen)

Para obtener buenos parámetros para la red se puede usar *RandomSearchCV*.

**4. Pruebas**
Intentar resolver instancias de prueba (100 instancias).  Reportar:
* Porcentaje de instancias resueltas
* Promedio de pasos en instancias resueltas vs. promedio óptimo en **mismas instancias**

Representación del estado
--
Los estados deberían ser representados por una matriz (o un vector ordenado por filas). En esta matriz los valores se encuentran:
* *compactados:* es decir, diferencias entre group_value seguidos son igual a 1.
* *normalizados:* dividir los group_value por max_group_value
* *elevados*: los top de los stacks en primera fila de la matriz, los espacios vacíos representados por 1.0
![cpmp_state_ann](https://docs.google.com/drawings/d/e/2PACX-1vQNLBGwH7vfOOtnZwdv0_26tHkpk_2FxjkDKQF_BeOBGL5e5Dgok7myEZwSoNizxTMmzm_o7W61cHnF/pub?w=960&h=723)
Creo que los tops de los stacks son generalmente los elementos más importantes. La elevación permite que los tops de cada stack se encuentren siempre en la primera fila de la matriz. De esta manera la red puede ubicarlos más fácilmente.

Paper relacionado
--
[Deep learning assisted heuristic for CPMP](https://drive.google.com/file/d/1Ih_89cW38mUQYSc_YjrQXOjtKqTgw4KJ/view?usp=sharing)
![image](https://i.imgur.com/YbTDCdb.png)
- The network is dependent on the size of the instance, however once trained for a particular instance size, instances with less stacks and tiers can also be solved by using dummy containers.
- The branching DNN’s input layer consists of a single node for each stack/tier position in the instance. Directly following the input layer are locally connected layers (as opposed to fully connected layers) that bind each stack together. This provides the network with knowledge about the stack structure of the CPMP. We include several locally connected layers, followed by fully connected layers that then connect to the output layer.
- We use a technique called weight sharing directly following the input layer in which each tier is assigned a single weight, wi, as opposed to assigning each container a weight. As can be seen in the figure, for example in the topmost tier, the weight w3 is applied to each stack at that tier. The group value is multiplied by this weight, and then inserted into the next layer of the DNN. The propagation of the group values through these first layers can be thought of as a feature extraction process, where the same features are generated for each stack. The subsequent layers process these features and are fully connected: Each node processes its inputs with an activation function and sends its output into all nodes of the next layer. All nodes of the hidden layers use the rectifier activation function, defined as ReLU(x) = max{0, x}.

**Results**
![image](https://i.imgur.com/ElghiQr.png)

**Propuesta de arquitectura**
El resultado es independiente de la permutación entre stacks iniciales.
![cpmp_network](https://docs.google.com/drawings/d/e/2PACX-1vS6-C3mMF9-f1LOhvOGXyJlQ6bmlaimgx_AK8LvVfDH8xjQk4XIKeLGZzEzs73E-sZLNJFj1Zdwke7a/pub?w=960&h=720)

![image](https://docs.google.com/drawings/d/e/2PACX-1vQ_byCKarTmf34z_XpmTrZaIIqZlg9v_7xNFx1TapeUZ4xd8LWuJNQIoBxexe1eh4Z1sFjEsZPSie3s/pub?w=476&h=349)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIxMjYzMTg1MTAsMTQxNDM3NjQ4OF19
-->