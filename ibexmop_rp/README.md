Removing points from the non-dominated set
==
[Link Colab](https://colab.research.google.com/drive/1obOynZeZWc2APFXb01ckSTlT0T5mtXEZ?usp=sharing)

[Link github](https://github.com/rilianx/Research/tree/main/ibexmop_rp)

### TODO

+ Una vez que se verifique el correcto funcionamiento, implementar en [solver ibex](https://github.com/rilianx/Research/blob/main/ibexmop_rp/README.md#solver-ibex).
+ [ibex_NDS.h](https://github.com/INFPUCV/ibex-lib/blob/ibexmop-plugin/plugins/optim-mop/src/strategy/ibex_NDS.h).
	+ ==Ordenar código y revisar==
	+ Juntar con NDSh
	+ Probar con instancias reales
	+ 
	+ 
````
python3 plugins/optim-mop/main/plot3.py &
./__build__/plugins/optim-mop/ibexmop plugins/optim-mop/benchs/binh.txt  --cy-contract-full --eps-contract --ub=ub1 --eps=1 --print_nds
````

### Tutorial (detalles faltantes)

* Mostrar figura antes y **después** de eliminar el punto junto al HV que se pierde (para comprobar).
Ejemplo (antes):

![image](https://i.imgur.com/dtwIAJ6.png)

**Faltaría imagen de después junto al HV perdido.**

* Verificar que el HV en este caso se esté calculando correctamente:

![RemovingPoints6](https://docs.google.com/drawings/d/e/2PACX-1vTcvvYJCAT8lhNVS9cfTyD0ISQW9vqGEPw0hNv3ev1yc3XDyXe_TjMUZl1S0KCRamwTdJXsyIHLosNt/pub?w=314&h=258)

El HV corresponde al área del triángulo generado con P (el punto eliminado), B'(el nuevo punto que se agrega) y B (el punto original que se corre).

- **Mantener una Lista de Puntos.** Un punto sería una estructura (clase) asociada a cada punto del gráfico. Cada punto almacena el punto que se encuentra antes y después (vecinos). Además de sus coordenadas el punto almacena el HV que se pierde si es eliminado.
Al  eliminar o agregar un nuevo punto es necesario actualizar el HV del punto y de sus vecinos.
Según Braulio, esto es similar al [Patrón Observador](https://es.wikipedia.org/wiki/Observer_(patr%C3%B3n_de_dise%C3%B1o)). El objetivo es lograr una eliminación de puntos y actualización de HV eficiente, y que no sea necesario calcular el HV para todos los puntos cada vez que queramos reducir la cantidad.

El objetivo final de este trabajo es crear un método eficiente de actualización y eliminación de puntos para luego ser embebido en un solver de optimización bi-objetivo.

Solver Ibex
---

El solver lo instalé en la carpeta `home/practica/ibex-rp`.
[Aquí](https://github.com/INFPUCV/ibex-lib/blob/ibexmop-plugin/plugins/optim-mop/README.md) puedes ver una introducción al solver (es el mismo que usas a través de jupyter).

Para correr un ejemplo:

    ./__build__/plugins/optim-mop/ibexmop plugins/optim-mop/benchs/binh.txt  --cy-contract-full --eps-contract --ub=ub1 --eps=0.1

Para imprimir los vectores solución de manera gráfica:

     python3 plugins/optim-mop/main/plot3.py

No es necesario entender al 100% el solver, sólo saber algunas cosas importantes como:

Las clases que permiten al solver resolver problemas con dos objetivos se encuentran [aquí](https://github.com/INFPUCV/ibex-lib/tree/ibexmop-plugin/plugins/optim-mop)

El método [`OptimizerMOP::optimize`](https://github.com/INFPUCV/ibex-lib/blob/fac74dc4a5bb9e3c854307d080e774def0425e01/plugins/optim-mop/src/strategy/ibex_OptimizerMOP.cpp#L327) es el corazón del solver. Realiza la búsqueda usando un árbol de búsqueda comenzando por la raíz, etc.

Luego, la función [`OptimizerMOP::upper_bounding`](https://github.com/INFPUCV/ibex-lib/blob/fac74dc4a5bb9e3c854307d080e774def0425e01/plugins/optim-mop/src/strategy/ibex_OptimizerMOP.cpp#L82), es una de las principales del solver. Esta función se encarga de buscar soluciones factibles (dominadas y no dominadas) para agregar al conjunto de soluciones.

En este código por ejemplo, obtenemos el punto central de una caja (`mid=box2.mid()`). Si el punto es factible (`is_inner==True`) lo evaluamos en los dos objetivos (`goal1` y `goal2`) y el vector resultante se intenta agregar en el conjunto de soluciones **ndsH** (variable de tipo `NDS_seg`).

![image](https://i.imgur.com/JBFfaDP.png)

La clase [`NDS_seg`](https://github.com/INFPUCV/ibex-lib/blob/ibexmop-plugin/plugins/optim-mop/src/strategy/ibex_NDS.h) es la que nos interesa ya que es la encargada de almacenar las soluciones no dominadas de la frontera de pareto.

Tiene un sinfín de operaciones que permiten agregar puntos o segmentos además de otras cosas cómo calcular distancias e intersecciones. Sin embargo, lo único que nos interesa es el mapa: `map< Vector, NDS_data, sorty2 > NDS2;` que es el que guarda los puntos o vectores.

Por lo tanto, lo que se podría hacer es agregar en la clase `NDS_seg` la estructura que generaste para guardar los puntos (con sus hv y punteros anterior/siguiente). Y luego una función (`remove_points(int n)`) que elimine `n` puntos seleccionando iterativamente el que minimiza el hv. Probablemente haya que copiar el mapa `NDS2` en tu estructura y luego volver a copiar de vuelta o algo por el estilo. Pero no importa, eso lo podemos optimizar más tarde.

Para probar la implementación se puede llamar desde el [`main`](https://github.com/INFPUCV/ibex-lib/blob/ibexmop-plugin/plugins/optim-mop/main/ibexmop.cpp). Antes del return 0 se puede llamar a la función (por ejemplo: `o->ndsH.remove_points(100);`)

![image](https://i.imgur.com/Uwvlnn5.png)

----

When solving multi-objetive problems with global optimization solvers, generally a set  <img src="https://render.githubusercontent.com/render/math?math=\mathcal{S}"> of non dominated points (upper envelope) is maintained and updated in each iteration (red points in the figure).

![upper_envelope22](https://docs.google.com/drawings/d/e/2PACX-1vRxeuOBhvGK2PVezyfyONOW6Ni5eXio6NnUCc1sdKnMEiRrbRg-ZOBLYXr6KuTw4VrkdFz8Shy5Xp27/pub?w=343&h=294)

The figure represents a biobjective optimization problem. The objectives are <img src="https://render.githubusercontent.com/render/math?math=f_1"> and <img src="https://render.githubusercontent.com/render/math?math=f_2"> and we want to minimize them. Red points (and segments between them) represent feasible solutions we have already found. Thus, we want to continue searching **only** in **the non-dominated region** (we can discard the other one).

New found points are included in <img src="https://render.githubusercontent.com/render/math?math=\mathcal{S}"> and some *dominated* points are removed from this set.
The set <img src="https://render.githubusercontent.com/render/math?math=\mathcal{S}"> may grow a lot, implying some methods  of the solver (which use this set) **begin to perform more slowly**. For instance:
* adding new points in <img src="https://render.githubusercontent.com/render/math?math=\mathcal{S}">
* generating dominated segments for filtering
* computing distance of boxes to the set <img src="https://render.githubusercontent.com/render/math?math=\mathcal{S}">

In order to keep a reduced size of the set <img src="https://render.githubusercontent.com/render/math?math=\mathcal{S}">, the idea of this work is to propose a mechanism for removing points from the set such that the quality of <img src="https://render.githubusercontent.com/render/math?math=\mathcal{S}"> *does not get too much worse*.

The figure shows an example of how to remove the **x** points without losing too much precision of the dominated region.

![RemovingPoints2](https://docs.google.com/drawings/d/e/2PACX-1vQ5EIfHG4pa3i3pmU9CGyzkUraHe-HAqmyp2hTlEyULjNFZO5XxyECfLAW07WRstE1LBMEY2YB8bUC3/pub?w=300&h=250)

The white point was moved to a new position in order to keep a valid *frontier*.
Note that the new frontier **MUST** pass over the old one (pointed one).

Algoritmo (idea)
--
Se puede recorrer el espacio de puntos (2D) e ir probando que pasaría si eliminamos el punto actual.

Al eliminar un punto P hay *tres casos posibles*:

- **El punto queda bajo la región dominada por el segmento que une el punto anterior con el siguiente (AB).** En este caso bastaría eliminar el punto.
![removingPoints4](https://docs.google.com/drawings/d/e/2PACX-1vTiTodnzPGuWtjfQ5GjtgoBlvhylYt8GO7afn0q8VFxvL47W-h90kbrbzx_pynVHHZAL38IPmy2ZOFK/pub?w=235&h=204)

- **El punto P está dominado por el segmento AB. Además el siguiente punto (B) se encuentra dominado por el segmento PC**. En este caso se puede proyectar el segmento que une A con P y el punto que une a B con el siguiente punto. Luego mover B a la intersección de ambas proyecciones (ver figura).
![RemovingPoints6](https://docs.google.com/drawings/d/e/2PACX-1vTcvvYJCAT8lhNVS9cfTyD0ISQW9vqGEPw0hNv3ev1yc3XDyXe_TjMUZl1S0KCRamwTdJXsyIHLosNt/pub?w=314&h=258)

- **Si el siguiente punto (B) queda bajo el segmento PC**, entonces el punto no puede ser eliminado (conviene eliminar directamente el siguiente punto)
![RemovingPoints5](https://docs.google.com/drawings/d/e/2PACX-1vRUicavl0tVtv4_aBu65RXZeIFqx1iwlfZWB7fRwmeZV5Xo2H5ajaDqEH2gk6Fi61vMNchMlW1V_kzL/pub?w=351&h=245)

Por último, al eliminar un punto P que pasa sobre la región dominada, existen dos posibles proyecciones: por la derecha y por la izquierda (como se muestra en la figura):
![RemovingPoints7](https://docs.google.com/drawings/d/e/2PACX-1vRCu6UbrKm1LSVwaiTuKFeluSi_aAoRY4CSl-DGNI1Bc1w5uRkFsl-ixSIxodU4nFkTvdfr1rpgTunl/pub?w=403&h=245)
Convendría escoger aquella que minimiza el hipervolumen perdido.

Se podrían ir eliminando puntos con un impacto menor en el hipervolumen.



[Aquí](https://github.com/rilianx/Research/blob/main/ibexmop_rp/example.ipynb) se puede ver un ejemplo para obtener puntos de instancias de prueba y poder comenzar a trabajar con ellos.


¿Cómo saber si un punto pasa por sobre o bajo una recta?
--
![PuntoRecta](https://docs.google.com/drawings/d/e/2PACX-1vQRYR8NyJxqYsSgqzB25h7siR8vQcHwZ49bHAszUk0YDeQfY3daOpJz7swLbkPAYf9b4QRvedzenxwE/pub?w=628&h=314)
<!--stackedit_data:
eyJoaXN0b3J5IjpbMzY1NTA2MDEzLC0xOTExNzE0NDI3LC0xOT
A1MzIyMjk0LC0xNjQyMTY1ODk1LDEwMzM3NjMwNDIsMTc1NDI2
NzE1OCwtNjA4MTYyNTc4LC0xNzU4MDQ1MjUxLDEwMTAzNjExMj
EsMTkzNzg3MzM5NCw3MDMxNDQ3MDcsMTY0NDAzODk5OCwtMTQz
MzkyNDQ1MiwtMTc0NzMxMzA4NiwtMTY1ODA0MjAyOCwxNzIxNj
g4ODU4LDk4NDU1NTYzMSwtOTg2OTg3MjU0LC0yMDYyMDAwNjMy
LDEzMzUyMTg5Nl19
-->