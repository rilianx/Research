CPMP branch & bound
===
Basándose en [paper](https://drive.google.com/file/d/1Lo2IArfDTUvpzhTbkrUWXqi7PfQr_tvQ/view). [Resultados](https://docs.google.com/spreadsheets/d/1DOiAi34tXVthcDbHKlTgCApZ_v8UQxaq/edit#gid=376661203)

**Plan:** Implementar algoritmo completo (árbol de búsqueda, best-first, etc) para el problema CPMP. Aprovechando que tenemos el *mejor greedy*.

### TODO

- ==Martín: Incorporar nuevo LB (LBATman) al solver==
- ==Ignacio: Revisar LBATman, comparar con LB estado-del-arte==
- Comparar stack vs pqueue (profe) --> [results](https://docs.google.com/spreadsheets/d/1DOiAi34tXVthcDbHKlTgCApZ_v8UQxaq/edit#gid=886426566)
- Implementar filtrado de acciones :ok: (filtrado básico)


## Nuevo LB
Ver [aquí](https://docs.google.com/presentation/d/1P5Cm_yDFzWqpIwLdj5uQBox3X-UQ0tMnvIXDciF2M60/edit#slide=id.ge7514acd31_0_359%29)

## ¿Qué modificaciones integrar?

**Filtrado de movimientos**

Implementé dos funciones para validar movimientos en `Layout.h`:

![image](https://i.imgur.com/5hXsXMM.png)

Estas funciones necesitan que el Layout guarde la secuencia de movimientos:

![image](https://i.imgur.com/q5PbdHb.png)

Que deben ser actualizados al final de la función `Layout::move`

![image](https://i.imgur.com/FBShbue.png)

Las funciones de validación se usan en `get_children` para evitar generar todos los hijos. Dejé todos los criterios de selección en un sólo if.

![image](https://i.imgur.com/8HqTtNO.png)

**Uso de PQueue (en vez de stack)**
En clase Tree:

![image](https://i.imgur.com/0beW3Ew.png)

Se debe implementar función para comparar/ordenar los nodos dentro de la cola con prioridad (en `main_cpmp.cpp`)

![image](https://i.imgur.com/lR0UNsN.png)

Dejé casi todo el algoritmo en la función `search2` de `main_cpmp`. Revísala y si no has cambiado search2, puedes pegar todo el contenido.

![image](https://i.imgur.com/T9sSG0g.png)

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
def validate(seq, s1, s2):
    if s1 < s2: return True
	h2 = size(s2); h1 = size(s1)
	h20 = h2; h10 = h1
	#se desea saber si el mov: s1->s2 se puede realizar antes,
	#si es así: return False
    for so, sd in seq: # vuelve en la secuencia
       if so==s1: h1+=1 elif sd==s1: h1-=1
       if so==s2: h2+=1 elif sd==s2: h2-=1
       if h2==H: return True
       if h2<h20 or h1<h10: return True #stacks variantes
       if h20==h2 and h10==h1: return False #stacks invariantes
    return True #first move
````


**Evitar mover el mismo contenedor varias veces**
Si una secuencia de movimientos $S$ es invariante para los stacks$s_o$, $s_d$, $s_t$. Y justo antes de la secuencia se realizó el movimiento $(s_o,s_t)$. Entonces el movimiento $(s_t,s_d)$, se puede descartar, ya que hubiera sido mejor realizar el movimiento $(s_o,s_d)$ desde un comienzo.

````python
def validate2(seq, st, sd):
	h = size_stacks(); h0=h 
    for so, sdd in seq: # vuelve en la secuencia
       if sdd==st and so not in variant_stacks:
	       if h[so]=h0[so] and h[st]==h0[st] and h[sd]==h0[sd]: 
		       return False
       h[so]+=1; h[sdd]-=1
       if h[sdd]<h0[sdd]: #variant stack
	       if sdd==st or sdd=sd: return True 
	       variant_stacks.insert(sdd)
    return True #first move
````

**Evitar XB moves?**
Fuerzan a encontrar solución sin movimientos adicionales. Esto es como preferir nodos que minimizan lb.
![image](https://i.imgur.com/eZG1njX.png)
¿Cómo estandarizar secuencia de movimientos?

### Future Work

* Implementar Feasible Diving -> Estrategia de selección de nodo. Selecciona el nodo que minimiza l, busca en profundidad a partir de ese nodo y repite.

---
### LowerBound

![image](https://i.imgur.com/lx4HlDz.png)
Quizás se puede hacer para cada gv, en vez de sólo usar el que maximiza la carencia

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
eyJoaXN0b3J5IjpbMTI3MTUxNjE2NSw1NTQ0NDc4MjMsLTEzNj
IyMzUyNzcsLTc4NzMyOTgyOSw3OTYyMTc3NjUsLTE0MTg0MzQw
NTgsLTEzNzQ0MjU5OTUsLTEzNDIxODA5NTgsNDMwMzI5NDkyLD
Y2MzAwMjczOSwyMDg0OTMxMTM1LC0yMTQzNTcyNTM1LDU3NTc3
Mjc3NCwtMjUwNTcyNjY0LC0xNTEzNjA3NjksLTIwOTg5Njc4MD
YsLTEwMTE0OTcyMjUsLTExNDkyMjQ4NzEsOTc4OTY3MTU5LC0x
NjIxNTg0ODY3XX0=
-->