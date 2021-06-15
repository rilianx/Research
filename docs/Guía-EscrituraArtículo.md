[Escritura Papers](https://docs.google.com/file/d/15zz-n1lxaeyiZhJYtRrL0X-gYwOn6I41/edit)

### Giselle Vásquez

[Paper LazyMOP](https://docs.google.com/file/d/1AZIy2D-M7aiV5irKOq5omrjrNANl3MTL/edit) -- [overleaf](https://www.overleaf.com/project/604179927232b1516ad3ee84)

**TODO**

- Organizar algoritmo para dejar como en el paper

----

- (**En background**) Agregar figura de ejemplo para explicar spline
- Calcular errores de predicción
- (**En propuesta**) Agregar pseudocódigo al algoritmo de la estrategia general. También agregar imágenes que muestren:
	- Creación de la primera caja y
	- Estimación del punto eficiente usando spline y creación de caja
	- Segunda caja (en caso de fallo)
- En subsecciones explicar detalles de las distintas partes del algoritmo.
	- Selección de $y_1$
	- Creación de caja para búsqueda. ¿Qué pasa si falla?
	- Reducción en x (mejora?)
	- Search Efficient
- (**Experimentos**) Algoritmo de base (2000) -> HV
Y sin reducir y. Comparación con/sin reducir en x. 


**Estructura paper**

- Introducción
	- Reescritura anti-plagio
	- Hablar de interpolación y métodos existentes
- Background
	- Intervals :ok: (falta corrección anti-plagio)
	- Biobjective problems (revisar y arreglar)
	- Interpolación (traducir, faltan referencias)
- Propuesta
- Experimentos
	- Definir
- Conclusiones


---
###  Gonzalo Tello

[overleaf](https://www.overleaf.com/project/6041a75784090c42d9685499)

**TODO**

- Leer archivo de instancias
- Ejecutar BSG y retornar mapas de cajas

**Generación de bins**
Pasar al contenedor cajas suficientes para llenar 1-2 contenedores.

````python
def generate_bins(B, Vmax):
	bins <- {}
	while B is not empty:
		C <- {}
		while vol(C) < 1.5*Vmax and B is not empty:
			b <- pop box from B
			C <- C U {b}
		bin, B' <- BSG(C)
		B <- B U B'
		bins <-- bins U {bin}
	return bins
````

- Para tener una buena distribución, la probabilidad de seleccionar una caja (pop box) debiera ser **proporcional al volumen**.
- Si hay varias cajas del mismo tipo, seleccionar un máximo de 8 (2x2x2).

----

- Terminar de armar la propuesta
	- ==Generación de bins:== Incorporar al paper
	- Swapping :ok:
	- ==Check==
- Cambiar figuras
- ¿En qué consiste algoritmo de la competencia?

**Tareas (Ignacio):**

- Usar instancias BRx50
- Buscar algoritmo de la competencia para comparar [paper](https://www.sciencedirect.com/science/article/pii/S0925527313001837)
- BSG: pruning branches that cannot place all the boxes

**Paper**

- Abstract :ok:
- Introduction
- Background
	- MCLP :ok:
	- BSG :ok:
	- Bin Packing :ok:
- Proposal :ok:
	- Generación inicial
	- Transfer&Swap

---

[code](https://github.com/skjolber/3d-bin-container-packing)
[code2](https://github.com/Janet-19/3d-bin-packing-problem)

 [Paper BSG+Swapping](https://docs.google.com/file/d/1E_HygrzJMH3dG-WdwKXeX6GIxD5jt3mw/edit) - [overleaf](https://www.overleaf.com/project/6041a75784090c42d9685499) - [gdrive](https://docs.google.com/document/d/1RUuVHQWjizS74PkeBlamFq8MKApKk0CRcNDpMESahjU/edit) - [dibujos](https://docs.google.com/presentation/d/1aCljdmWoufgoqwiAFanbBSE-pys-2VLXnzDEegMWQB0/edit#slide=id.gb694a9189a_0_32)


---
### Stephanie Gómez (Tifa)

**TODO**

Modificaciones al código:

- CollectedData mantiene una lista de muestras (Data)
- Cada muestra (Data) debería estar compuesta de: ==información del árbol==, nodos (N) y nodos seleccionados (S)
- En el archivo cada vez que llego a un ;, debería resetear StateMap. ==Y resetear state==
- Probar si se están guardando
- La función eval_heuristic(v, data), debería recibir un Data de CollectedData y generar el ranking
- ==Verificar que eval_heuristic funcione correctamente==
- HC y verificar correcto funcionamiento
- Experimentos con simulación --> pasar a paper
- ==Integración de Solvers (profe)==

**Estructura Paper**
0. Abstract :ok:
1.  Introducción :ok:
2. MCTS :ok:
3. Policy
	3.0. Intro :ok: (en spanglish). Faltaría diagrama
	3.1. Data Collection :ok:
	3.2. Training Phase
	    3.2.1. Parameterized heuristic (falta explicar HC)
	    3.2.2. Training a regression model :ok:
4. Node Attributes :ok:
5. Experiments
	5.1 Simulaciones
	5.2. Solvers (CPMP, BSG-CLP, IbexOpt)
6. Conclusions

**Links**

 [Paper Interactive MCTS](https://docs.google.com/file/d/1U_rvqVXLuZcC21dXv1MnQ4ytoFIhBZyO/edit) - [overleaf](https://www.overleaf.com/5616249127ygnkmzvpjbty) - [gdrive](https://docs.google.com/document/d/1WTBcwIJcoCwo_973JQEIFvmzvkvucJ6cFBYIrxb_Vw0/edit?ts=6055111a) - [diagrama](https://app.diagrams.net/#G1sG15EXnp0rAfnC4jNbBuJybQTwiKGhvm)

Atributos de nodos
![image](https://i.imgur.com/Tayv9cj.png =500x)

````python
def best_first(self): 
	return self.s
````

````python
def diving(self):
	return 1000*(self.parent == last_selected) + self.s
````

````python
def dfs_greedy(self):
    return 1000*self.depth + self.s
````

sat: nodes_in_level/max_nodes_in_level

````python
def bfs(self):
	return -10000*sat - 10*self.depth + self.s + c*sqrt(1/(len(self.ch)+1))
````


---
### Luciano

**TODO**

- ==HillClimbing **1 vector x todas las listas**==
- ==Avance en paper (sección experimentos)==

[Sistema de recomendación](https://docs.google.com/file/d/1-IDaFVlcMcUOo11KTW5NSwaQE5_Sc-VV/edit) - [overleaf](https://www.overleaf.com/project/6053a175fa465c69f71acdd6)

---

### Lucas Agullo (en pausa)

[Paper CPMP_RL](https://docs.google.com/file/d/1r_kHXnKd40upiHzVqo7C8qObaCLjnRpT/edit) - [overleaf](https://www.overleaf.com/project/60424d0a17d15d7bfaeabbf0)

- Diseño de experimentos


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE2ODY4NjYxMyw0NTg4MTcyNzgsODc1Mz
M3OTAyLDE4NzMzMzcwMDcsMjA4OTU2NDk2OCwtMTg1NTc4OTU3
MiwxNjgzOTcyNDc0LDk0Njk1NjU3MywxMzk1MzkzMjU2LC0xNz
k0MTM0NjAsLTI1NzY0MjksMTc0MzgxMzUsLTIxMTIwODg4OTAs
LTU4NTgwMTU0LDg3ODM5NjAxNSwtNTAwNDA0NDY0LC0xMTUyMj
A3NTMwLDE0MzgxMjczMzUsMjAxMzE1MjgyOCwtNTkyMDU2NzM3
XX0=
-->