IMRT Beam Angle Optimization
==
Acceso al código: **VisualStudio -> ctrl+R -- imrt-bao**
 
>- [Link Trello](https://trello.com/b/WmPgDVQH/practica)
> - [github](https://github.com/MatiasZunigaL/Practica-imrt)

Usando como base el solver `DAO_ILS`, la idea es crear un algoritmo que permita encontrar los mejores ángulos para realizar el tratamiento.


IMRT (TODO)
---
- Nelder Mead
	- Eliminar ángulos repetidos de x
	- Ajustar al más cercano
	- Límite por iteraciones de búsqueda local (1.000.000).
- Gráfico convergencia (mejor_evaluación vs).

* Implementar algoritmo bayesian optimization
* Diseñar técnica sofisticada que *decida* de manera adaptativa la cantidad de iteraciones a realizar cada vez que se realiza una búsqueda local. El objetivo es llegar a buenas soluciones con una cantidad *más reducida* de iteraciones. Una idea más abajo:

**Idea (partial local search)**
- Limitar evaluaciones por búsqueda local (e.g., 1000)
- Aplicar HC o SA para encontrar soluciones candidatas
- Explotar soluciones candidatas (e.g., 10000 iteraciones)

Objetivos
--
1. Estudiar estado del arte sobre BAO, hacer resúmenes.
2. Diseñar e implementar algoritmo en Python.

¿Qué es IMRT BAO?
---
Es un problema que surge del tratamiento de cáncer usando radiación.

El paciente es colocado en una cámara y es irradiado por distintos ángulos usando un acelerador lineal o *beam*. El objetivo es *entregar* al tumor una dosis de radiación prescrita por el médico tratante.

![image](https://i.imgur.com/pcHMsyF.png)

Para enfocarse en el tumor y evitar demasiado daño en órganos sanos, cada *beam* cuenta con unas plaquitas que impiden el paso de la radiación, las cuáles son ajustables. Estas plaquitas pueden ser representadas como una matriz de **beamlets**. Un ajuste de plaquitas se conoce como **aperture shape**.

![image](https://i.imgur.com/FGb9GLX.png)

El tumor y los órganos son representados por **voxels** (cajitas 3D)

![image](https://i.imgur.com/A5yhCAo.png)

**La matriz de deposición** establece la cantidad de radiación que un beamlet (en un ángulo específico) irradia a cada voxel del tumor y de los órganos por unidad de tiempo. Cada beamlet puede irradiar a varios voxels.

![image](https://i.imgur.com/kMVBrfA.png)

La radiación total entregada por los beamlets en un ángulo específico puede ser representada por una matriz de intensidades o **fluence map**. Esta matriz agrega las radiaciones asociadas a cada aperture shape considerada en ese ángulo. 
En la figura se muestran fluence maps asociados a tres ángulos de radiación. Cada uno considera 5 aperture shapes.

![image](https://i.imgur.com/s8e9syt.png)

**Solución y función objetivo**

Una solución para el problema consiste en:

1. Una configuración de ángulos (**BAC**) para los beams
2. Un fluence map **Y** para cada ángulo.

El **objetivo** es intentar irradiar *todos los voxels* del tumor la dosis prescrita por el médico dañando *lo menos posible* los órganos sanos del paciente.
El objetivo se suele expresar con una función que penaliza los voxels *v* que reciben una dosis mayor a la recomendada, es decir, si <img src="https://render.githubusercontent.com/render/math?math=d_v(x) - D>0">:

<img src="https://render.githubusercontent.com/render/math?math=Pen(v) = \lambda \cdot (d_v(x) - D)^2">,

con <img src="https://render.githubusercontent.com/render/math?math=d_v(x)">, la dosis recibida por el voxel *v* y **D**, es la dosis recomendada para el órgano. <img src="https://render.githubusercontent.com/render/math?math=\lambda"> es un peso asociado a la función y es inversamente proporcional a la cantidad de voxels que tiene el órgano.

Los voxels del tumor $v_t$ que reciben menos radiación que la prescrita también son penalizados:

<img src="https://render.githubusercontent.com/render/math?math=Pen(v_t) = \lambda \cdot (D_t - d_{v_t}(x))^2">,, 

con <img src="https://render.githubusercontent.com/render/math?math=D_t"> la dosis prescrita para el tumor.

**¿Cómo resolver el problema?**
El problema se puede dividir en dos partes:

- *Direct Angle Optimization (DAO)*: Para un BAC dado, encontrar la mejor configuración de aperturas e intensidades. 
Este problema ya lo tenemos más o menos resuelto, el solver [`DAO_ILS`](https://github.com/rilianx/IMRTsolver) realiza una *búsqueda local iterada* para encontrar buenas soluciones (fluence maps) para un conjunto de ángulos de entrada (BAC).
* *Beam Angle Optimization (BAO)*: Encontrar una buena configuración de ángulos con el objetivo de reducir las penalizaciones. (Hill Climbing)
Primero que nada hay que investigar un poco para ver lo que existe al respecto.
Una idea simple consiste en:
	* Comenzar con un BAC inicial y modificar un ángulo de manera aleatoria una pequeña cantidad. 
	* Optimizar usando `DAO_ILS` y comparar el resultado con el que se tenía previamente. Aceptar la modificación si mejora.
	* Iterar

**Tutorial en jupyter notebook**
Preparé un [tutorial](https://github.com/rilianx/Research/blob/main/imrt_bao/tutorial.ipynb) para poder comenzar de lleno a implementar funcionalidades en el framework.


**Más información**
* [Paper](https://drive.google.com/file/d/1M0Pmn-tt4PVj5pRmWOJrnCF7j72p1tg4/view?usp=sharing)
* Buscar en [google scholar](https://scholar.google.com/):
	* "IMRT BAO" (año > 2016)

----

### TODO (profe)

* Agregar perturbación a ILS (en C++ y en python)
* Agregar opción para considerar porcentaje del vecindario -> acelerar perturbaciones


**Idea (cotas para problema con voxels reducidos):**
Al seleccionar una pequeña porción de voxels *representativos*, considerar la máxima y mínima deposición por beamlet para el conjunto de voxels representados. De esta manera sería posible obtener un intervalo para el costo alcanzado por una solución.

**Idea (partial local search)**
- Limitar evaluaciones por búsqueda local (e.g., 1000)
- Aplicar greedy o SA para encontrar soluciones candidatas
- Explotar soluciones candidatas (e.g., 10000 iteraciones)

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEyMjU3NTIwNTEsLTE1NjE2ODU2OTEsMT
k1NjA2MDA2NSwtMTE4MDAzODA2MCwtNDU3NTMzNjgwLC04NTQ3
ODY5MjYsMTU4NDMzNTMyMywxODMxODcwMjEwLDEzNTM2ODcxOD
gsLTIwMjczMTc5NDgsLTIwMTAzODAxNzAsODcxNDM2NTQxLC0y
MDY3NDAyMzkwLDYzMDI2MDkwMywxMTg2NDExNTUxLC0yMDA2Mz
U5NzA4LC02MjI4NzIwODYsNTE2MDI2MDY5XX0=
-->