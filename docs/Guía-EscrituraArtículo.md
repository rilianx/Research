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

- Trabajando en background
- Calcular errores de predicción

- Introducción
	- Reescritura anti-plagio
	- Hablar de interpolación y métodos existentes
- Background
	- Intervals :ok: (revisión anti-plagio)
	- 
	- 

---
### Lucas Agullo

[Paper CPMP_RL](https://docs.google.com/file/d/1r_kHXnKd40upiHzVqo7C8qObaCLjnRpT/edit) - [overleaf](https://www.overleaf.com/project/60424d0a17d15d7bfaeabbf0)

- Diseño de experimentos

---
###  Gonzalo Tello

 [Paper BSG+Swapping](https://docs.google.com/file/d/1E_HygrzJMH3dG-WdwKXeX6GIxD5jt3mw/edit) - [overleaf](https://www.overleaf.com/project/6041a75784090c42d9685499) - [gdrive](https://docs.google.com/document/d/1RUuVHQWjizS74PkeBlamFq8MKApKk0CRcNDpMESahjU/edit) 

- Entender algoritmo para mejorar sección de bin packing
- Comenzar a redactar propuesta

---
### Stephanie Gómez

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
eyJoaXN0b3J5IjpbNjk4MjA2ODM4LDM3NjI5NDkwMCwxNzU0Nz
Y5MTYsMzQ2MTAzNjIsNzIxNDE0MDkyLDc0NzM4MjAyNiwtMTAx
NTU5OTI3NSwxMTIwNDc4ODUyLC0xMDEzMzMxNTg1LC0xNDQwOD
Y5Nzg0LDYwNDE4ODM2OSwtMTg0MjQ3NzQ0Miw5NzY1MTU3MTcs
LTc3NTI0MjM3MCwtODAwNDc4NDI4LC0xODIyMzg1MDk4LDE0Nj
czMDc0MTgsLTE3MDk3MzQ5NjMsOTcxMDU2NzcsLTE0OTUzMzA4
NjFdfQ==
-->