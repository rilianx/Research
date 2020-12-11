IMRT Beam Angle Optimization
==
Usando como base el solver `DAO_ILS`, la idea es crear un algoritmo que permita encontrar los mejores ángulos para realizar el tratamiento.


IMRT (TODO)
---

* Algoritmo Hill Climbing
* Algoritmo Greedy (que iría agregando ángulos de uno en uno)
* Probar todas las combinaciones (3)
* Estudiar estado del arte

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
**Notas para el profe**

Las siguientes funcionalidades del framework IMRT falta por implementar:
* *perturbation(neigh,nmoves)*: realiza una perturbación a la solución actual.
* *update_fluence_map(changes)*: modifica el fluence map usando una lista de cambios puntuales. Retorna la nueva evaluación.
* *update_dose_vectors(dose_vectors)*: modifica los vectores de dosis irradiada de acuerdo a la ùltima actualización del fluence map.

**Idea:**
Al seleccionar una porción de todos los voxels, considerar



<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA5NDM5NzI1OSwtMjA2NzQwMjM5MCw2Mz
AyNjA5MDMsMTE4NjQxMTU1MSwtMjAwNjM1OTcwOCwtNjIyODcy
MDg2LDUxNjAyNjA2OV19
-->