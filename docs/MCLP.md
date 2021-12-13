###  B. Gonzalo Tello

[paper](http://scm.snu.ac.kr/publication/paper/81.pdf)
[resultados](https://docs.google.com/spreadsheets/d/1k2gZSq8wCGzTfX_YCRvm3CPwF5RNuE7jh4pmN5sxzSM/edit)

### TODO
- Comparar column generation con BSG-generator
- Column generation
- Revisar que todo calce (pallets)
- 

### Papers

- [2015 - Hybrid genetic algorithms for the three-dimensional multiple container packing problem](http://scm.snu.ac.kr/publication/paper/81.pdf) -- Large Instances 1
- [Martello code - Algorithm 865](http://hjemmesider.diku.dk/~pisinger/codes.html)
- [Three-Dimensional Bin Packing and Mixed-Case Palletization](https://pubsonline.informs.org/doi/pdf/10.1287/ijoo.2019.0013) -- [Python code](https://github.com/Wadaboa/3d-bpp) -- Large Instances 2


### Propuesta

In this work we plan to solve the MCLP by combining two algorithms: a state-of-the-art beam-search-based algorithm for solving the single CLP from a set of defined boxes, and a bin-packing algorithm for selecting and swapping boxes among the containers.

In this paper we show how we can solve a MCLP, by combining a CLP state-of-the-art algorithm and a simple strategy for swapping boxes among bins and validating the generated solutions.


### TODO

- Probar con distintos  valores para r_param=1 | 1.5 | 2 | 5 | 100
- Correr algoritmo de los swaps (2500). 1000 iteraciones
    - Por iteración guardar si trató de validar el swap, si hizo el swap, volumen mínimo y volumen ajustado mínimo
- Graficar volumen mínimo vs iteraciones
- **Swap con volumen ajustado.** Jugar con parámetros n={1,2,4}, max_vol_accept (por defecto= 1.1), tolerance (por defecto = 0.3)
- Swap sin volumen ajustado max_vol_accept (por defecto= 0.8), tolerance (por defecto = 0.2)
- Probar con instancias de Martello.

### Experimentos

- Comparar en instancias clásicas.
	- Ajuste de parámetros para generación de solución inicial. 
	- Ajuste para swapping
- Correr en instancias difíciles. Buscar instancias 73x


### Formato paper

 **Paper**

- Abstract :ok:
- Introduction
	- Armar copiando de otros papers
- Background
	- MCLP :ok:
	- BSG :ok:
	- Bin Packing :ok:
- Proposal :ok:
	- Generación inicial
	- Transfer&Swap
- Experiments
	- Generación inicial y ajuste de parámetros BSG
		- Classical instances
		- Large instances
	- Algoritmo de swaps
		- Classical instances
		- Large instances



**Probar solamente generate_initial_solution (2500 cajas)**

r_param = 1.0 | 1.2 | 1.5 | 2.0 | 100.0

**sin greedy (bsg)**
generate_candidate_solution(ssh,L,W,H,boxes,id2box, r_param=r_param, bsg_time=1, extra_args="--min_fr=0.98")
con distintos tiempos: 1|2|5|10

--min_fr=0.95 | 0.98 | 0.99 | 1.00

--max_bl=1000 | 10000
extra_args="--max_bl=10000 --min_fr=0.99"

**Random swap (listo el algoritmo!)**
1. Seleccionar 2 bins (A y B) de manera aleatoria
2. Sacar [1..n] items de A
3. Sacar [0..n] items de B
4. Aceptar si varianza aumenta y:
  5. Aceptar swap si suma de adj_vol < 1.0
  6. Aceptar con probabilidad decreciente si 1.0 < suma <1.05

**Estrategia general**
- Compute the adjusted volumes
- Start the algorithm
- Increase: n, max_acceptance, tolerance, bsg_time

### Links
[overleaf](https://www.overleaf.com/project/6041a75784090c42d9685499)
 [(2013) A biased random key genetic algorithm for 2D and 3D binpacking problems](https://www.sciencedirect.com/science/article/pii/S0925527313001837) - [github](https://github.com/gtello79/MCLP_BinPackingProblem.git) 
[best results for small instances](https://www.researchgate.net/profile/Anjali-Awasthi-4/publication/314657085_A_column_generation-based_heuristic_for_the_three-dimensional_bin_packing_problem_with_rotation/links/5f4bbef4458515a88b8e1796/A-column-generation-based-heuristic-for-the-three-dimensional-bin-packing-problem-with-rotation.pdf)
(https://github.com/charlesjlee/Kaggle/tree/master/Packing_Santas_Sleigh/Code/Matlab/GA)
[Resultados BRKGA](https://docs.google.com/spreadsheets/d/129OeCag-I1odJJrFbRBDa3V9y_8QgQWDGIsxHtEAVgY/edit#gid=0)
Results with rotation allowed (6r) and not allowed (aNB)
![image](https://i.imgur.com/1xYs4Ls.png)
 
[jupyter](http://localhost:8888/lab/tree/Documents/research_on_github/%2Blocal_projects/mclp-gonzalo/base/execute_bsg-profe.ipynb)

https://sci-hub.se/10.1016/j.ejor.2016.07.033
![similar idea](https://i.imgur.com/4Lh64R3.png)


### Criterio de evaluación se swaps

**Idea:** 

- Estimar un *adjusted volume* para cada tipo de caja. Este volumen "ajustado" consideraría el volumen real de la caja y cierto factor que tiene que ver con la dificultad para colocarla.
- Realizar swaps con el objetivo de incrementar *desviación absoluta promedio* del *adjusted volume* para el conjunto de bins.
![image](https://i.imgur.com/3isuYgo.png)

**Cómo estimar *adjusted volume***
Llenar bins seleccionando distintos conjuntos de cajas con volumen total igual a X% del volumen del contenedor (con X>100). 

Input: cajas del bin
Output: 1
Regresión lineal con bias = 0

![image](https://i.imgur.com/HnGijQB.png)







**Plan**

- Realizar experimentos
	- Instancias originales
	- Instancias aumentadas (x100 cajas, x2x2x2 bin size)

**Resultados de la competencia**
![image](https://i.imgur.com/pcr6qSW.png)

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




---

[code](https://github.com/skjolber/3d-bin-container-packing)
[code2](https://github.com/Janet-19/3d-bin-packing-problem)

 [Paper BSG+Swapping](https://docs.google.com/file/d/1E_HygrzJMH3dG-WdwKXeX6GIxD5jt3mw/edit) - [overleaf](https://www.overleaf.com/project/6041a75784090c42d9685499) - [gdrive](https://docs.google.com/document/d/1RUuVHQWjizS74PkeBlamFq8MKApKk0CRcNDpMESahjU/edit) - [dibujos](https://docs.google.com/presentation/d/1aCljdmWoufgoqwiAFanbBSE-pys-2VLXnzDEegMWQB0/edit#slide=id.gb694a9189a_0_32)


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzNzE5OTgwMiwtMzYyMzA0MTU1LDE1OD
Q3ODE0MTksNjYzNDcwMTY4LC0xMzEyNzU1ODQzLDEwMTE5Mjg4
MSwzNjU1MTcyNzgsLTE4MDE1MDEwNzUsLTQ4OTgxNzE4NSwtMj
AxMjExOTAxNiwtMjc5NzA5MDMyXX0=
-->