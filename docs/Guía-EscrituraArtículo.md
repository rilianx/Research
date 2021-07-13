[Escritura Papers](https://docs.google.com/file/d/15zz-n1lxaeyiZhJYtRrL0X-gYwOn6I41/edit)

### A. Giselle Vásquez

[Paper LazyMOP](https://docs.google.com/file/d/1AZIy2D-M7aiV5irKOq5omrjrNANl3MTL/edit) -- [overleaf](https://www.overleaf.com/project/604179927232b1516ad3ee84)

**TODO**
- Graficar resultados de Ibex para comparar
- Identificar errores SearchEfficient
- Reparar algoritmo

**Plan**

- Experimentos
	- Comparar con algoritmo completo: tiempos, HV
	- Cálculo de error (interpolación vs. SearchEfficient)
	- Graficar interpolación vs. curva original
	- Incorporar hull(x)
- Volver redacción de paper

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
###  B. Gonzalo Tello

[overleaf](https://www.overleaf.com/project/6041a75784090c42d9685499)

**Plan**
- 

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
### C. Luciano

**TODO**

- ==HillClimbing **1 vector x todas las listas**==
- ==Avance en paper (sección experimentos)==

[Sistema de recomendación](https://docs.google.com/file/d/1-IDaFVlcMcUOo11KTW5NSwaQE5_Sc-VV/edit) - [overleaf](https://www.overleaf.com/project/6053a175fa465c69f71acdd6)

---



<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1NDU1ODQ4MzgsNDQ4NzkxNzY0LDE3ND
gwMjM2MTYsMTcxNzExNTA0NCwtODE4NTMwNDE5LDQ1NzQ4NTk2
LC0xNjg2ODY2MTMsNDU4ODE3Mjc4LDg3NTMzNzkwMiwxODczMz
M3MDA3LDIwODk1NjQ5NjgsLTE4NTU3ODk1NzIsMTY4Mzk3MjQ3
NCw5NDY5NTY1NzMsMTM5NTM5MzI1NiwtMTc5NDEzNDYwLC0yNT
c2NDI5LDE3NDM4MTM1LC0yMTEyMDg4ODkwLC01ODU4MDE1NF19

-->