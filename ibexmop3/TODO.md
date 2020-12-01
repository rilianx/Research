IbexMop3
==
**Objetivos:**
- Implementar programa en Python que permita ir viendo paso a paso cómo el solver va explorando el espacio de búsqueda y encontrando soluciones factibles.
- Implementar método para generar hiperplano factible.
- Generar plano contractante


Ejecución interactiva
--
El objetivo es, a partir del historial guardado por el solver relacionado con la resolución de instancias de prueba, construir un visualizador interactivo que permita ir viendo lo que ocurre. Es decir, en cada iteración del solver, se debería poder ver:
* cuál fue la caja seleccionada
* los puntos factibles que se encontraron usando esta caja
* la bisección y las nuevas cajas incorporadas a la búsqueda
* ¿cuáles son las cajas que hay actualmente en el árbol de búsqueda?
* ¿cuáles son los puntos del conjunto no dominado actual?

[Aquí](https://github.com/rilianx/Research/blob/main/ibexmop3/tutorial_ibexmop.ipynb) se puede ver un breve tutorial en jupyter lab.

Generación de hiperplano factible
---
Para generar un hiperplano factible es necesario linearizar las restricciones y las funciones objetivo (e.g., usando AbsTaylor). La linearización de las funciones objetivo debe cumplir que:
$f(x)<=fl(x)$

además, para cada objetivo $i$ agregamos una variable y una restricción:  
$y_i=fl_i(x)$

Luego, politopo formado por vértices  $y^i = \argmin (fl_i (x,y))$  es factible.

Para encontrar el politopo optimo:

- *Ver algoritmo de Benson.*
- [Ver este paper también](https://journals.sagepub.com/doi/full/10.1177/1748302619870424)

Usar hiperplano para contractar
---
En la imagen se muestra la idea.
La imagen izquierda sería un hiperplano *óptimo* pero difícil de calcular 
La imagen de la derecha serían hiperplanos más fáciles de calcular (proyección de puntos extremos de cada hiperplano factible con las caras de la caja)
![contracting with hyperplanes](https://docs.google.com/drawings/d/e/2PACX-1vSyFzHheVWKpZe6Y7YJJle5PJKqWzZxwrserwnCx2he6LsQj5QqYSb_e0WxMYRQSaM2b0Wvr4FOqSvC/pub?w=1320&h=547)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTk1NDE0MDUxNiwtMjEzNjE5Mzg4OV19
-->