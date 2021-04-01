CPMP branch & bound
===

Implementar algoritmo completo (árbol de búsqueda, best-first, etc) para el problema CPMP. Aprovechando que tenemos el *mejor greedy*.

### TODO
Implementar siguiente algoritmo:

````c++
void solve(layout)    
    u = greedy(layout) 
    opt = DFS(layout,u) 
````

Basado en [paper]((https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view)):

![image](https://i.imgur.com/inpzkaD.png)

### Referencias
> - [2019 - A branch and bound approach for large pre-marshalling problems](https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view)
> - [??? - A new simple heuristic for the Container pre-marshalling problem](https://www.overleaf.com/read/vfmzmfmbvqpt): AKA el mejor greedy
> - [Repo greedy en C++ y Python](https://github.com/rilianx/cpmp/)
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTk4NTY2OTE4MCwtMTkyNzI0MTUxNCwxND
k5NTk1ODkxXX0=
-->