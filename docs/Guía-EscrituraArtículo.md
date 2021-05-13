Trabajo en paper
==

### Links

[How to write high quality papers in algorithmic or experimental Computer Science](https://www.ae-info.org/attach/Acad_Main/Sections/Informatics/Activities/12-08-14-Paper-VM-for-AE.pdf) (ver sección 4)

## Instrucciones

- Creen documento en overleaf con la estructura del paper. Pueden basarse en la estructura de [este paper](https://www.overleaf.com/read/vfmzmfmbvqpt).

- Escriban bosquejo de **abstract**. Quizás yo ya haya escrito alguno en sus documentos en github. Pueden basarse en el que está en el paper. Es sólo un bosquejo, la idea por ahora es que ayude a recordarnos hacia donde estamos apuntando.
Generalmente lo divido en párrafos:
	- Descripción del problema
	- Estado del arte (lo que hay hecho hasta ahora)
	- Propuesta (qué es lo **nuevo** que se propone?)
	- Resultados

![image](https://i.imgur.com/zpn4DKO.png)

- Escriban el **background**, es decir todo aquello que necesitan para poder explicar la propuesta con claridad. Por ejemplo, en qué consiste el problema, como se realiza una búsqueda en árbol, detalles sobre las redes neuronales, etc. El detalle tiene que ser suficiente como para que alguien no muy experto del tema entienda. También tienen que referenciar los métodos y algoritmos existentes.

- Pueden continuar con la **descripción de la propuesta**. Esta debe ser escrita de manera detallada y rigurosa. Con pseudocódigos explicados y figuras si es necesario. A partir de esta descripción deberíamos ser capaces de implementarla.

- Luego se puede pasar a diseñar los experimentos que se realizarán para validar la propuesta. Esto lo podemos ir conversando más adelante.

[Aquí](https://www.froihofer.net/en/students/how-to-write-a-computer-science-paper.html) más tips sobre escritura de artículos.

---

## Alumnos

### Giselle Vásquez

[Paper LazyMOP](https://docs.google.com/file/d/1AZIy2D-M7aiV5irKOq5omrjrNANl3MTL/edit) -- [overleaf](https://www.overleaf.com/project/604179927232b1516ad3ee84)

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
- (**Experimentos**) Definir

---

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
### Lucas Agullo

[Paper CPMP_RL](https://docs.google.com/file/d/1r_kHXnKd40upiHzVqo7C8qObaCLjnRpT/edit) - [overleaf](https://www.overleaf.com/project/60424d0a17d15d7bfaeabbf0)

- Diseño de experimentos

---
###  Gonzalo Tello


[code](https://github.com/skjolber/3d-bin-container-packing)

 [Paper BSG+Swapping](https://docs.google.com/file/d/1E_HygrzJMH3dG-WdwKXeX6GIxD5jt3mw/edit) - [overleaf](https://www.overleaf.com/project/6041a75784090c42d9685499) - [gdrive](https://docs.google.com/document/d/1RUuVHQWjizS74PkeBlamFq8MKApKk0CRcNDpMESahjU/edit) 

- Terminar de armar la propuesta
- ¿En qué consiste algoritmo de la competencia?

Tareas:
- Usar instancias BRx50
- Buscar algoritmo de la competencia para comparar [paper](https://www.sciencedirect.com/science/article/pii/S0925527313001837)

---
### Stephanie Gómez

Modificaciones al código:
- Que se puedan simular varios nodos a la vez
- Que las simulaciones se vayan agregando en el mismo archivo


 [Paper Interactive MCTS](https://docs.google.com/file/d/1U_rvqVXLuZcC21dXv1MnQ4ytoFIhBZyO/edit) - [overleaf](https://www.overleaf.com/5616249127ygnkmzvpjbty) - [gdrive](https://docs.google.com/document/d/1WTBcwIJcoCwo_973JQEIFvmzvkvucJ6cFBYIrxb_Vw0/edit?ts=6055111a) - [diagrama](https://app.diagrams.net/#G1sG15EXnp0rAfnC4jNbBuJybQTwiKGhvm)

- Traducción
- Diagrama de la estrategia general

Atributos de nodos
![image](https://i.imgur.com/Tayv9cj.png =500x)

````python
def best_first(self): 
	return self.s
````

````python
def diving(self):
	return 1000*(self.parent == last_selected) + self.s
````

````python
def dfs_greedy(self):
    return 1000*self.depth + self.s
````

sat: nodes_in_level/max_nodes_in_level

````python
def bfs(self):
	return -10000*sat - 10*self.depth + self.s + c*sqrt(1/(len(self.ch)+1))
````




### KD-Tree

[Overleaf](https://www.overleaf.com/project/5f7cc504d82a7900017178fa)

- Descripción del KD-Tree tradicional
- Descripción de algoritmo IKD-Tree

### Practical Constraints

- Revisar contenido. 
- Ajustar secciones de integración con algoritmo --> dejar trabajo a Williams.
<!--stackedit_data:
eyJoaXN0b3J5IjpbOTk1OTgwMzQxLDY0MzkzODQ3MywxOTI2MT
E5MTc1LDk5MDExOTIwNywtMTA0MjU4Nzc1MywtNDcwNzUyOTI0
LC0yMDY3OTM1NDk4LC0yMzEyNTI3MTEsMzc2Mjk0OTAwLDE3NT
Q3NjkxNiwzNDYxMDM2Miw3MjE0MTQwOTIsNzQ3MzgyMDI2LC0x
MDE1NTk5Mjc1LDExMjA0Nzg4NTIsLTEwMTMzMzE1ODUsLTE0ND
A4Njk3ODQsNjA0MTg4MzY5LC0xODQyNDc3NDQyLDk3NjUxNTcx
N119
-->