CPMP branch & bound
===
Basándose en [paper](https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view).

Implementar algoritmo completo (árbol de búsqueda, best-first, etc) para el problema CPMP. Aprovechando que tenemos el *mejor greedy*.

### TODO

* :ok: Ordenar de los hijos 
* ==Explicar lo que hacen en  [paper](https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view) vs lo propuesto==
* ==Contar cantidad de nodos que tarda en llegar a la mejor solución==
* ==`update(L)`: menor l de los nodos guardados en el stack (profe) Listo!==
*  `lower_bound(nodo)`: ver lo que hacen en paper y proponer versión parecida (hace una buena función lower_bound es *very difficult*)
* ¿Cómo filtrar acciones usando reglas de dominancia?. Ver cómo lo hacen en paper.
* Feasible Diving? -> Estrategia de selección de nodo. Selecciona el nodo que minimiza l, busca en profundidad a partir de ese nodo y repite.



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
eyJoaXN0b3J5IjpbLTYyNDM2MTI0OCwtMTMyMDc5MTcyLDE2Nz
M4MTk0MjMsMTc1MDQ5Mzk4OCwtMTcwMDkwMzk2NSwtMTU2ODMw
MzM0MywtMTg0MzQ0NzMzMCwtMzM2OTgyNjI4LC00NjY2NTczMD
AsMjczNjAxNTA2LDE1NTc1MjM2OCwxNDE1NTQxMTUzLC0xMjAz
MzE5OTQ0LC0xOTI3MjQxNTE0LDE0OTk1OTU4OTFdfQ==
-->