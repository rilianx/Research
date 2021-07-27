[Escritura Papers](https://docs.google.com/file/d/15zz-n1lxaeyiZhJYtRrL0X-gYwOn6I41/edit)

### A. Giselle Vásquez

[Paper LazyMOP](https://docs.google.com/file/d/1AZIy2D-M7aiV5irKOq5omrjrNANl3MTL/edit) -- [overleaf](https://www.overleaf.com/project/604179927232b1516ad3ee84)

**TODO**
- Si el punto se encuentra en parte inferior de la caja pequeña, expandir la caja en Y2.
- Eliminar puntos dominados
- Calcular cantidad de veces que se agreandó la caja, cuantas veces falló (estadísticas)
- Cálculo de hipervolumen
- Graficar resultados de Ibex para comparar
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
 [(2013) A biased random key genetic algorithm for 2D and 3D binpacking problems](https://www.sciencedirect.com/science/article/pii/S0925527313001837)
 
**TODO**

- Buscar algoritmo de la competencia para comparar ([Rust code](https://github.com/bobotu/kaosu-packer))
- BSG solo debería verificar bins modificados
- Al verificar soluciones, para acelerar el proceso, BSG podría descartar estado que no puedan ubicar todas las cajas.

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

- Repetir experimentos
	- Hill-Climbing para optimizar vector de pesos
	- Usar atributos normales, +director-likeness, +emotion, +both




<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIwMTMxNDUwNjgsMTM1MTY5NTQxOSwtMT
E0NzAwNjI0OSwyMDYyOTE0NTQ0LC0xMDc1NTkwNjIwLC0xNDM5
MDU0MzYzLC02NTU3NTA2NzQsMTI1OTYwNDA2MywxMTkxMDYxMz
U4LC0xOTkwODQ5NzcwLC0xMjYwOTQ2NTg2LC01NDcyMjMyMzEs
NDQ4NzkxNzY0LDE3NDgwMjM2MTYsMTcxNzExNTA0NCwtODE4NT
MwNDE5LDQ1NzQ4NTk2LC0xNjg2ODY2MTMsNDU4ODE3Mjc4LDg3
NTMzNzkwMl19
-->