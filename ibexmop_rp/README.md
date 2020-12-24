
Removing points from the non-dominated set
==

TODO (Kevin)
---
* Eliminar punto superior al segmento
* Algoritmo general que reciba lista de puntos y número de puntos a eliminar
* Calcular hipervolumen



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

Al eliminar un punto hay dos casos posibles:
- El punto queda bajo la región dominada por el segmento que une el punto anterior con el siguiente. En este caso bastaría eliminar el punto.
![revobingPoints4](https://docs.google.com/drawings/d/e/2PACX-1vTiTodnzPGuWtjfQ5GjtgoBlvhylYt8GO7afn0q8VFxvL47W-h90kbrbzx_pynVHHZAL38IPmy2ZOFK/pub?w=235&h=205)
- El punto P está dominado por el segmento que une el punto anterior A con el siguiente B. En este caso se puede proyectar el segmento que une A con P y el punto que une a B con el siguiente punto. Luego mover B a la intersección de ambas proyecciones (ver figura).
![RemovingPoints3](https://docs.google.com/drawings/d/e/2PACX-1vQYv_zNoCcyN20SzdW7ljjCey-6BRfmbkbYXEbgUtJaBoZE51WVgoasiBFeZJ9gat6ceyt775fcm7Tn/pub?w=235&h=205)

Se podrían ir eliminando puntos con un impacto menor en el hipervolumen.

[Aquí](https://github.com/rilianx/Research/blob/main/ibexmop_rp/example.ipynb) se puede ver un ejemplo para obtener puntos de instancias de prueba y poder comenzar a trabajar con ellos.


¿Cómo saber si un punto pasa por sobre o bajo una recta?
--
![PuntoRecta](https://docs.google.com/drawings/d/e/2PACX-1vQRYR8NyJxqYsSgqzB25h7siR8vQcHwZ49bHAszUk0YDeQfY3daOpJz7swLbkPAYf9b4QRvedzenxwE/pub?w=628&h=314)
<!--stackedit_data:
eyJoaXN0b3J5IjpbOTkxMjY3MjAzLDY2ODQ3Mjg5MiwtMTkzNj
AxODk2MywxNjMzNjM1Mjk1LDE3Nzc1MTU1OTgsMjEzMTIzNzAz
OSwxMDU2NjM4Mjk2LC0xMDA2NzEzMTU3XX0=
-->