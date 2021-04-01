CPMP branch & bound
===

Implementar algoritmo completo (árbol de búsqueda, best-first, etc) para el problema CPMP. Aprovechando que tenemos el *mejor greedy*.

### TODO

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
def search(layout, LB, UB):
   S = stack() # por ahora
   while S is not empty:
      n = S.pop()
      ub = greedy(n) # compute upper bound
      if ub < UB: 
         UB = ub
         if UB=LB: return #
      ##
      lb = LB(n) #compute the lower bound of the node
      if lb >= UB: continue
      children = get_children(n)
      # en paper ordenan los nodos antes de guardarlos
      for each c in children:
         S.push(c)
````

Basado en [paper](https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view):

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
eyJoaXN0b3J5IjpbLTEyMTE5NzIyNDgsLTEyMDMzMTk5NDQsLT
E5MjcyNDE1MTQsMTQ5OTU5NTg5MV19
-->