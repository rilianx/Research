### TODO

- Dejar los parámetros como entrada por comando al algoritmo
- Implementar SA con restart
- Agrupar items por similaridad y analizar lo que se obtiene
- ==Ignacio: leer paper; pensar estrategia==
- Releer paper en buscar de técnicas clave que podrían mejorar el desempeño.

**Experimentos**

10 corridas (semillas aleatorias) para cada configuración -> script
Promedio, y la mejor solución encontrada
- Solución inicial: {Greedy, RGreedy}
- Porcentaje del RGreedy: {fijo, 5%, 10%, 20%}
- no_improvements (swap): {50,100}
- perturbation: {0-3} swaps (sin importar si mejoran o no)
- cantidad de movimientos: {1000,2000}
Reportar: RGreedy, perturbation, promedios y mejor (solución inicial, solución alcanzada)

**Graficar convergencia** (beneficio vs. iteraciones), para 1 o dos instancias --> sin perturbación
x: iteraciones de la búsqueda local  (swaps)
y: evaluación


---

### Plan

- Terminar algoritmo ILS base: Grasp + local search + perturbations
- Experimentos de validación
- Agregar aprendizaje: seleccionar solución prometedora (luego de perturbación) para recomenzar búsqueda local. 

----

### Algoritmo

**Eliminación de elemento random+items**
1. Eliminar elemento e items asociados
2. Iterar por los elementos de la mochila y eliminar los que no tengan padre al interior de la mochila

**Greedy/GRASP**
- Va seleccionando aleatoriamente entre el n% de los items con mayores *dynamic-ratios* para ir ingresando en la mochila.

**Swap**
  - Seleccionar elemento random, y sacar todos los items asociados de la mochila
  - Aplicar Greedy/GRASP a la solución 
	
**[Instancias de prueba](https://www.researchgate.net/publication/336126211_Three_kinds_of_SUKP_instances)**
- Profit de items
- Peso de elementos
- Matriz elementos x item





---

### Optimización

* Heap para guardar items de mayor a menor ratio. Cada vez que se seleccione un item, se recalcula su ratio, si se reduce, se manda de vuelta al Heap y se selecciona el siguiente. Si se mantiene, se selecciona


--- 

Ayuda C++. [link clase ejemplo](https://dis.unal.edu.co/~fgonza/courses/2003/poo/c++.htm), [documentación c++](http://www.cplusplus.com/reference/list/list/)

---



### Resultados paper

![image](https://i.imgur.com/J9p4CUq.png)

Idea
==

Inspirado en:
[Iterated two-phase local search for the Set-Union Knapsack Problem](https://sci-hub.se/10.1016/j.future.2019.07.062)

Algoritmo que mantiene la "esencia" del paper.

````python
def solve()
   s = random_greedy() #construcción de solución inicial
   sb = s #mejor solución
   while time < time_limit
      s = local_search(s) # e.g., hill climbing o Simmulated Annealing para mejorar resultados
      if f(s) > f(sb): sb = s
      s = perturbation(sb) # or random_greedy()
````

````python
def local_search(s): # hill_climbing
    #moves: (item a sacar, item a colocar, mejora)
    no_improvements = 0
    while no_improvements < 50:
       m = generar movimiento aletaroio (considerandos swaps) 
       si m mejora: 
	       s = s.apply(m)
	       no_improvements = 0
	   sino: no_improvements+=1
       
````


El `random_greedy` básicamente coloca los items uno a uno en la mochila. En el paper usan un greedy determinista. Yo lo haría aleatorio (e.g, escoger uno de los mejores en vez del mejor).

![image](https://i.imgur.com/ZCPDunx.png)

Para la `local search` se podría implementar un algoritmo que vaya haciendo swaps aleatorios y vaya aceptando sólo aquellos que mejoran la función objetivo (hill climbing). En el paper proponen estos movimientos. Yo me quedaría sólo con el primero. Generalmente, el algoritmo debería detenerse luego de un número consecutivo de swap fallidos (50?)

![image](https://i.imgur.com/B5CNEqK.png)

Para la `perturbation`, en el paper sacan algunos elementos de la mochila y colocan otros aleatoriamente hasta que la capacidad lo permita. El objetivo de esto es "comenzar" a buscar de nuevo con una solución *parecida* a la mejor encontrada previamente.

Otra opción es comenzar de cero haciendo un `random_greedy`.


¿Y dónde colocamos aprendizaje?
---

Se me ocurre lo siguiente. Mantener una lista con las soluciones/estados retornados por la búsqueda local.
En cada iteración debemos decidir si perturbamos un estado en el conjunto L, o si partimos de uno nuevo (`random_greedy`)

````python
def solve()
   S = []
   while time < time_limit
      s = select a state from S 
	         or create a new state with random_greedy 
      s' = local_search(s)  
      if f(s') > Sb: 
         Sb = f(s') #se actualiza mejor solución
      s' = perturbate(s')
      S.add(s')
````

Cada estado en `S` puede almacenar la siguiente información:

- Mejor solución encontrada a partir del estado (o máximo f(local_search(s) - f(s) ) )
- Promedio/desviación estándar de evaluaciones a partir del estado
- Número de veces que el estado ha sido seleccionado
- Otra información relacionada con el problema

Y a partir de esta información nos interesa identificar el estado con mayor probabilidad de mejorar el `Sb`. 

Para entrenar el asunto, se puede correr el algoritmo 100 veces con cada diferente estado de partida. Luego se ordenan las soluciones encontradas (sol) de peor a mejor y vamos creando muestras.

Información del estado s + f(sol_i)  -->  100-i%
Es decir hay un 100-i% de probabilidad de que el estado s produzca una solución mejor a sol_i.

----


$ alpha^{max\_iter} = t_{fin}/t_{ini}$



## Paper

We show that while CPLEX (version 12.8) can find the optimal solutions for the 6 small benchmark instances (with 85 to 100 items and elements) based on a simple 0/1 linear programming model, it fails to exactly solve the other 24 instances. These outcomes provide strong motivations for developing effective approximate algorithms to handle problem

**The SUKP algorithm**
![image](https://i.imgur.com/CdxOdHM.png)

Algorithm in two phases:
- The intensification-oriented component (first phase) employs a combined neighborhood search strategy to discover local optimal solutions (**VND and TS**)
- The diversification-oriented component (second phase) helps the search process to explore unvisited regions. (**Frequency based perturbation**)

**Construction**
The algorithm starts from a feasible initial solution that is obtained with a **greedy construction procedure**.
Compute the profit ratio for items and put them in order until the capacity is reached.

**Exploration**
Variable neighborhood descent (VND) search to locate a new local optimal solution within two neighborhoods (N1 and N2) and then runs a tabu search (TS) to explore additional local optima with a different neighborhood N3.

![image](https://i.imgur.com/J9G85dP.png)

The VND procedure exploits, with the best-improvement strategy, two neighborhoods N1 and N2 to locate a local optimal solution. Then from this solution, the TS procedure is triggered to examine additional local optimal solutions with another neighborhood N3.

**The VND algorithm**
Selecciona el mejor movimiento del vecindario N1.
Selecciona el mejor movimiento para una muestra del vecindario N2. Elementos de N2 son seleccionados con probabilidad $\rho$.
Repite mientras mejora la solución.
![image](https://i.imgur.com/Oc4qf9v.png)
==Idea: basarse en un sampling de movidas y escoger la mejor.==

**Tabu Search**
Se mueve hacia el mejor vecino sin importar que sea peor.
En la lista tabu se almacenan items involucrados en los últimos swaps.

![image](https://i.imgur.com/4qi22dr.png)


**Neighbourhoods**
Consisten en eliminar q items de la mochila y agregar p items nuevos.
N1: $(q,p) \in  \{(0,1);(1,1)\}$
N2: $(q,p) \in  \{(2,1);(1,2);(2,2)\}$
N3: $(q,p) \in  \{(0,1);)(1,0);(1,1)\}$

**Parameters**
![image](https://i.imgur.com/dgKnkhY.png)

Number of iterations ($T_i$) for item $i$ in tabu list:
![image](https://i.imgur.com/5SUToOX.png)



**Escape**

Frequency-based perturbation to displace the search to an unexplored region.

The algorithm keeps track of the **frequencies that each item has been displaced** and uses the frequency information to modify (perturb) the incumbent solution.

We delete the top η × |A| least frequently moved items from A and add randomly new items until the knapsack capacity is reached.


**Analysis of parameters**
![image](https://i.imgur.com/GJBE7pC.png)

**Observaciones**

- Si bien VND con $\rho=0.05$ ofrece los mejores resultados, usar un sólo vecindario no estan malo (peor en 3/30 instancias).
- Lo mismo ocurre con la perturbación. Hacer un restart empeora en 2/30 instancias (las mismas instancias que antes).

----

## Ideas y observaciones
- N1 "tiene sentido" cuando eliminar 1 item *implica eliminar al menos un elemento*. Es decir cuando hay cajas que sólo pertenecen al item que se desea eliminar.
- Se podrían proponer los siguientes movimientos análogos:
	- M1 $(q,p) \in  \{(0,1);(1,1)\}$: Se elimina elemento contenido en q item + q items asociados (y cajas adicionales si es necesario). Se colocan p items que caben en la mochila y, en conjunto, maximizan beneficio.
	- M2 $(q,p) \in  \{(2,1);(1,2);(2,2)\}$: Misma idea.
	- M3 $(q,p) \in  \{(0,1);(1,0);(1,1)\}$: Misma idea.
- Probar movimientos usando SA:
	- Aplicar M1 o M2 con 50%. Aplicar sólo M1. Aplicar sólo M3.
- Probar movimientos usando hill climbing con restarts (similar a VND del paper):
	-  mejor M1, sino mejor M2 (sampling con $\rho=0.05$)
	- primera mejora M1 (límite no improvements)
- Comparar **promedios** como en gráfico (10 corridas por instancia).
- Leer papers:
   - [Kernel based Tabu Search for the Set-Union Knapsack Problem](http://www.info.univ-angers.fr/~hao/papers/WeiHaoESWA2020.pdf)
   - [Multistart solution-based tabu search for the Set-Union Knapsack Problem](http://www.info.univ-angers.fr/~hao/papers/WeiHaoASC2021.pdf)

## Generar agrupaciones de items (pre-proceso?)

- Una agrupación de items: **grupo** no es más que un conjunto de items y la unión de sus elementos.
- Su beneficio es la suma de los beneficios de sus items.
- Su peso es la suma de pesos de sus elementos.
- Un grupo es *interesante de generar* cuando su ratio beneficio/costo es grande y cabe en la mochila.
- Los items de un grupo deberían compartir elementos para ser interesantes.
- Una vez creados, los grupos se pueden usar como si fueran items en cualquier algoritmo.
- Incluso se podría hacer un algoritmo que fuera creando grupos iterativamente uniendo grupos hasta alcanzar el tamaño de la mochila.



## Dual solving

Ir colocando elementos uno a uno con el objetivo de maximizar el beneficio esperado.
La idea es *ir viendo poco a poco* que item nos conviene antes de decidirnos.

Algoritmo:
1. Seleccionar elemento o item y agregarlo a la mochila.
2. Si no caben más elementos en la mochila, eliminar elementos sin item asociado.
3. Repetir.

**¿Cómo seleccionar elementos/items**

La **promesa** de un elemento tiene que ver con:
- El beneficio de los items que lo contienen
- Cuanto falta para materializar los items que lo contienen
- Su costo

Algo como beneficio esperado/costo, donde el beneficio esperado puede ser una suma ponderada de los beneficios de los items que lo contienen penalizada por cuanto falta para llenarlos.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExODM5Mzg3MjMsLTQxODcxODcxNCw2OD
Q1MzA1OTksLTU4MTcxMTYzNiwtMTI0Nzg3NjIxNCwtMTUxMzk4
MDM1MCwyODgzNTgyNjksLTE3MzE3MTMxLC04OTU3MjgwNCwyNT
AxNjc3NjAsMTIxOTc5MDg2LDE1MjI5MTUzMDUsOTc0NzI0MTYw
LC0xNTYwMjAzMjgwLDE1NTE3MDQ4NDQsNTMzNzE0NDgxLDUzMz
cxNDQ4MSw3MTQ1NzgyNDMsLTIwMTQ0MTAxMjIsLTE4MTczNTQ1
MDZdfQ==
-->