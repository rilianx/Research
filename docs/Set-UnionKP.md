### TODO

- Reparar eliminación de elemento random
- Lanzar experimentos
	- 
- Perturbación y selección de soluciones
- Identificar cuellos de botella ([gprof](https://www.thegeekstuff.com/2012/08/gprof-tutorial/))

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
	
**Parámetros del algoritmo**

- Porcentaje del RGreedy: {10%, 20%, 50%}
- no_improvements (swap): 50
- perturbation: {1-3} swaps (sin importar si mejoran o no)
- iteraciones de la estrategia: 10

**[Instancias de prueba](https://www.researchgate.net/publication/336126211_Three_kinds_of_SUKP_instances)**
- Profit de items
- Peso de elementos
- Matriz elementos x item

**Experimentos**

Probar distintas combinaciones de parámetros. Comparar (10 corridas aleatorias):
- Greedy
- RGreedy
- RGreedy+swaps
- RGreedy+swaps+pert

Graficar convergencia (beneficio vs. iteraciones), para 1 o dos instancias.


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
    while no_improvements < 100:
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

<!--stackedit_data:
eyJoaXN0b3J5IjpbNzkxMzMyOTQxLC0xODI1NDQzNTY4LDEzNT
Y4Mjg1NjAsMTUzMzU2MTg1OSwtNDYyNTAwNTY1LC04MDMxODIy
NTMsLTE0MzIyODQwOTUsNDIyNDc3Nzg2LC0xNjkyNTM1MjkxLD
M4NTE4ODYxMiwtNzkxOTQ0MjM1LDExOTkxNDgyODIsLTEzNDY2
MjU5OTIsMzM5ODMyMzA1LDk1OTM2MTAzLDE0OTQ5OTAwNzIsMT
QwMDY3OTA0OCwtMTQ4ODg5NzU1NiwtNjY5MTAwNzUzLC0xMTgw
MjE0MDk2XX0=
-->