[Escritura Papers](https://docs.google.com/file/d/15zz-n1lxaeyiZhJYtRrL0X-gYwOn6I41/edit)


---
###  B. Gonzalo Tello

[overleaf](https://www.overleaf.com/project/6041a75784090c42d9685499)
 [(2013) A biased random key genetic algorithm for 2D and 3D binpacking problems](https://www.sciencedirect.com/science/article/pii/S0925527313001837) - [github](https://github.com/gtello79/MCLP_BinPackingProblem.git) - [A biased random...](https://github.com/charlesjlee/Kaggle/tree/master/Packing_Santas_Sleigh/Code/Matlab/GA)
 
**TODO**

- Buscar algoritmo de la competencia para comparar ([Rust code](https://github.com/bobotu/kaosu-packer))
- Revisar gráficamente soluciones que BSG no pudo validar. Como esta:
![image](https://i.imgur.com/MsZ4s0k.png)
- Pensar en otro criterio de evaluación que incluya complejidad de cajas. Por ejemplo, puede convenir reducir diferencia en volúmenes, si bin más pequeño ha logrado deshacerse de caja complicada.

**Plan**

- Reparar y revisar el algoritmo
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
### C. Luciano

[Sistema de recomendación](https://docs.google.com/file/d/1-IDaFVlcMcUOo11KTW5NSwaQE5_Sc-VV/edit) - [overleaf](https://www.overleaf.com/project/6053a175fa465c69f71acdd6)

**TODO**

- Escritura de paper:
	- Agregar muchas citas en la intro (bibtex)
- Repetir experimentos
	- Optimizar vector de pesos con PSO --> Ignacio
	- Usar atributos normales, +director-likeness, +emotion, +both




<!--stackedit_data:
eyJoaXN0b3J5IjpbMTMzMjgzNjksLTY3MjUzOTU3OSwtMTE5NT
E0MDY2NiwtMTg5Njg4MzM1NSwtMTc1MzQwNjcxOCwxNzg2MTI5
NzA5LDQ3NTYzODQyOSwtMTgyOTY3MDg2LDg2MzU5NDMzMSwtOD
kzOTQwNjQ1LDIwOTkwMjIwMTYsLTg5Mzk0MDY0NSwxMzUxNjk1
NDE5LC0xMTQ3MDA2MjQ5LDIwNjI5MTQ1NDQsLTEwNzU1OTA2Mj
AsLTE0MzkwNTQzNjMsLTY1NTc1MDY3NCwxMjU5NjA0MDYzLDEx
OTEwNjEzNThdfQ==
-->