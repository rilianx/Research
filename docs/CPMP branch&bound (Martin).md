CPMP branch & bound
===
Basándose en [paper](https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view). [Resultados](https://docs.google.com/spreadsheets/d/1DOiAi34tXVthcDbHKlTgCApZ_v8UQxaq/edit#gid=376661203)

**Plan:** Implementar algoritmo completo (árbol de búsqueda, best-first, etc) para el problema CPMP. Aprovechando que tenemos el *mejor greedy*.

### TODO

- ==Implementar EstimateLB==
- ==Revisar lower bound== (instancia 3-3-3, por qué LB da más que 2)
- ==Usar valores de regresión lineal múltiple para evaluar nodos==
- Comparar stack vs pqueue (profe) --> [results](https://docs.google.com/spreadsheets/d/1DOiAi34tXVthcDbHKlTgCApZ_v8UQxaq/edit#gid=886426566)
- Implementar filtrado de acciones.

---

### Resultados estado del arte

![image](https://i.imgur.com/tRCtZ4H.png)

### Criterios para evaluar nodos

- lb, ub
- estimateUB -> calcular para estado inicial
![image](https://docs.google.com/drawings/d/e/2PACX-1vTb19uGv3c3yVvWNG4aoH9Bv2w107e6vbTyQDgyWjap3FYEEZh29RN1KlQR7DKk689qwQdxqVhYcTYI/pub?w=548&h=717)

### ¿Qué acciones filtrar?

Stack **invariante** a secuencia de movimientos.

**Unrelated move symmetries**
Si una secuencia $S$ es invariante para los stacks $s_o$ y $s_d$, con $s_o>s_d$, se descarta hacer el movimiento $(s_o,s_d)$ después de la secuencia $S$ (ya que se puede hacer antes). Salvo que el stack $s_d$ se haya llenado en algún momento de la secuencia.

**Implementation**
````python
def validate(seq, s_o, s_d):
    for s_o', s_d' in seq:
       if 
````


**Evitar mover el mismo contenedor varias veces**
Si una secuencia de movimientos $S$ es invariante para los stacks$s_o$, $s_d$, $s_t$. Y justo antes de la secuencia se realizó el movimiento $(s_o,s_t)$. Entonces el movimiento $(s_t,s_d)$, se puede descartar, ya que hubiera sido mejor realizar el movimiento $(s_o,s_d)$ desde un comienzo.

¿Cómo estandarizar secuencia de movimientos?

### Future Work

* ¿**Cómo filtrar acciones** usando reglas de dominancia?. Ver cómo lo hacen en paper.
* Implementar Feasible Diving -> Estrategia de selección de nodo. Selecciona el nodo que minimiza l, busca en profundidad a partir de ese nodo y repite.

---
### LowerBound

````python
def lower_bound():
    bx <- contenedores mal ubicados 
    bx <- bx + contenedores mal ubicados en stack con menos contenedores mal ubicados
    for gv in G: # para cada prioridad (calculo de demanda)
       D[gv] <- cantidad de contenedores con prioridad >= gv
    for gv in G: # cálculo de available slots
	   AS[gv] <- slots disponibles en Layout limpio (sin contar mal ubicados) para colocar contenedores con prioridad >= gv
	max_diff <- 0
	for gv in G:
		diff <- D[gv] - AS[gv]
		if diff>max_diff: max_diff <- diff
	min_vacate_stacks <- sup(diff/H) #redondeo hacia arriba
	sorted_stacks <- stacks.sort()  #de menos a más contenedores ordenados
	gx <- 0
	for i=0; i<min_vacate_stacks ; i++:
		gx+=sorted_stacks[i].sorted_containers
	return bx+gx
```` 



---
* Implementar siguiente algoritmo:

````c++
void solve(layout)    
    u = greedy(layout) 
    l = LB() # contar contenedores mal ubicados
    opt = DFS(layout,l,u) 
````

* Ver en paper como calculan LB y tratar de implementar algo
* Ver en paper que es `Memoization_Heuristic`
* Comparar version normal vs version con orden de hijos

````python
def search(layout, L, U): #lower y upperbound
   S = stack() # por ahora
   S.push(layout)
   lbs = multiset() # aquí se guardan todos los lbs de menor a mayor
   lbs.add(layout.unsorted_containers)
   while S is not empty:
      n = S.pop(); lbs.remove(n.unsorted_containers)
      u = greedy(n) # compute upper bound
      if u < U: 
         U = ub
         if L==U: return #termina algoritmo
      ##
      n.l = lower_bound(n)+n.steps;
      if n.l >= U: continue
      children = get_children(n) 
      # en paper ordenan los nodos antes de guardarlos usando 7 criterios
      for each c in children:
         S.push(c)
         lbs.add(c.unsorted_containers)
      L = first(lbs) # primer valor del multiset
````


### Búsqueda Diving
Bastaría con modificar la función de evaluación:
1000*greedy_child - lb


### Componentes claves del paper (deberíamos replicar)

- Cálculo del lower_bound (se usa para descartar nodos sub-óptimos)
- Movimientos son filtrados usando **reglas de dominancia**, es decir, se eliminan movimientos que con 100% de certeza no llegarán a la solución óptima del problema.
- Nodos se ordenan antes de ser almacenados en el stack. De esta manera se exploran ramas más prometedoras primero.


---

![image](https://i.imgur.com/inpzkaD.png)

We extend this approach by adding:
- tighter lower bounds, 
- a new branching comparison algorithm, 
- new dominance rules, 
- an initial memoization-based heuristic

At each node, all possible **non-dominated moves** are performed and the branches are ordered according to our **branching comparison algorithm**.

A move is dominated when one of the dominance rules is satisfied
or the **lower bound of the layout** is larger than the current depth
limit. --> calcula lower-bounds en cada nodo.

We try to complete partial solutions by using the **greedy heuristic algorithm**. In this way, the value u is updated during the search every time a better solution is found. The search ends if a solution of value l is reached.


### Referencias
> - [2019 - A branch and bound approach for large pre-marshalling problems](https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view)
> - [??? - A new simple heuristic for the Container pre-marshalling problem](https://www.overleaf.com/read/vfmzmfmbvqpt): AKA el mejor greedy
> - [Repo greedy en C++ y Python](https://github.com/rilianx/cpmp/)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTg5ODE3Nzc2Niw5Nzg5NjcxNTksLTE2Mj
E1ODQ4NjcsMTI4MTIyNzIwNSwtODU5MjI2NTQ4LC0xMzA2NTg3
NDA3LDE1MDkzMDkzMzcsMTczNDUzMTY0MCwxOTExMDk0Mjg3LD
EzMjYwNjE3ODUsLTkyMDY5NTU0MywtMTIyNzkzMTI1LC0xMTM5
MjAyMzQyLDg4OTkyNTY5NCw1OTg5MTU2MDQsLTIxMDc5NzU0MD
ksMTE2MzY4ODExMCwtMTczNjcxNTUyOSwtOTcwNTQwMzAyLC02
MjQ4MTk1MDFdfQ==
-->