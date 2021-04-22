IbexOpt: Primeros pasos
==

### Links de interés

* [Código en github](https://github.com/ibex-team/ibex-lib)
* [Documentación](http://www.ibex-lib.org/doc/)
* [Documentación ibexOpt](http://www.ibex-lib.org/doc/optim.html)

### Archivos, clases y funciones importantes:

* Main de ibexOpt: [src/bin/ibexopt.cpp](https://github.com/ibex-team/ibex-lib/blob/master/src/bin/ibexopt.cpp)
* Función  `optimize` de la clase `Optimizer`: [src/optim/ibex_Optimizer.cpp](https://github.com/ibex-team/ibex-lib/blob/master/src/optim/ibex_Optimizer.cpp#L415) 
* Implementación de la clase `CellBeamSearch` (FeasibleDiving): [src/cell/ibex_CellBeamSearch.cpp](https://github.com/ibex-team/ibex-lib/blob/master/src/cell/ibex_CellBeamSearch.cpp)
* Instancias de prueba: [benchs/optim](https://github.com/ibex-team/ibex-lib/tree/master/benchs/optim)
* La clase Cell (ya tiene una variable depth): [src/cell/ibex_Cell.h](https://github.com/ibex-team/ibex-lib/blob/master/src/cell/ibex_Cell.h)

Por defecto el Optimizer usa `CellBeamSearch` para la selección de nodo:

![image](https://i.imgur.com/0yru4dk.png)


La decisión de si queremos continuar con FeasibleDiving o pasar a otro nodo se debería tomar aquí ([CellBeamSearch.cpp](https://github.com/ibex-team/ibex-lib/blob/master/src/cell/ibex_CellBeamSearch.cpp#L61)):

![image](https://i.imgur.com/V4gdnik.png)

Aquí es donde se encuentran soluciones dentro de la caja.  [(`Optimizer::update_loup`](https://github.com/ibex-team/ibex-lib/blob/master/src/optim/ibex_Optimizer.cpp#L103)). Sin embargo, creo que `loup_finder.find` sólo retorna soluciones mejores al UB actual (`loup`). Si no encuentra lanza excepción.


![image](https://i.imgur.com/LOn1q6z.png)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEwNTUwMTI5NDUsMTc5Mjk2MDM0NCwtND
cwMjM0MTQyXX0=
-->