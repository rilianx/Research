CPMP branch & bound
===
Basándose en [paper](https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view).
[resultados](https://docs.google.com/spreadsheets/d/1DOiAi34tXVthcDbHKlTgCApZ_v8UQxaq/edit#gid=376661203)

Implementar algoritmo completo (árbol de búsqueda, best-first, etc) para el problema CPMP. Aprovechando que tenemos el *mejor greedy*.

### TODO

- ==Probar distintos criterios de Branching==
	- cantidad de slots disponibles de stack menos (mientras menos mejor)
	- diferencia entre tops bien ubicados
- Cambiar Stack por Heap.
- ¿**Cómo filtrar acciones** usando reglas de dominancia?. Ver cómo lo hacen en paper.

![image](https://i.imgur.com/tRCtZ4H.png)

### Criterios para evaluar nodos
- lb, ub
- slots disponibles en stack ordenados ponderado con 

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
eyJoaXN0b3J5IjpbLTExMjM4NDU3MjQsNzMyOTEwNjgzLC0yMD
M4MzU3MDY1LC05MjYwNTgzMzAsLTE3NTQwMTQyNzgsMTY3OTg0
ODM2MywtMjc1ODUxODE5LDk1OTQ4MDI4NywtNjk3NDU2Mjc3LC
0xODI2MzIyODYsNzg4NzgwMDIwLC0yMDkyNjQ1MDIyLDExMjk5
NTMzMjIsMTE4MzA2MjUwMSwxNjIwMjY0NDI0LC0xMjA3OTk3Nj
Q4LC0xNzM0NDk5MzE3LC03NTQ2NzY2MzIsLTYyNDM2MTI0OCwt
MTMyMDc5MTcyXX0=
-->