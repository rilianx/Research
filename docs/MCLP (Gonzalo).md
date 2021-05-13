MCLP: BSG+SC
==
> [doc](https://docs.google.com/document/d/1TRWv4af10Jyh4goY24D_6VWgwhACgEXA5_oy5xT-0Is/edit#) ∙ [tabla](https://docs.google.com/spreadsheets/d/15AYwB3ZHXsmz7WtOKGfcs_KSLPa9o9C7867i-EdrH1E/edit?usp=sharing) ∙ [drive folder](https://drive.google.com/drive/folders/1GZ2jEtGTgQFn9_W_hulqalN3K7sN_19Y)

TODO
---


### Trabajar en paper

Los objetivos de trabajar en la redacción del paper son:
1. Por un lado, tener algo más concreto, detallado y mejor explicado. Aunque sólo se tengan resultados preliminares, es posible enviarlo a alguna conferencia o revista para obtener feedback.
2. Trabajar en la redacción de un paper nos permitirá mejorar el entendimiento del algoritmo pudiendo vislumbrar maneras de mejorarlo u otras oportunidades.

### Pasos

- Estructura de paper (seguir estructura de presentación)
- Background (sacar de [BSG-CLP](https://www.sciencedirect.com/science/article/abs/pii/S0305054817300023) y [BinPacking](https://www.sciencedirect.com/science/article/abs/pii/S0305054800000824)
- Descripción de Algoritmo propuesto
- Diseño de Experimentos

Implementación de BinPacking en python
---
La idea es modular algoritmo e implementar la resolución del bin packing usando *python* y *Jupyter notebooks*.
El objetivo es facilitar la edición, modificación y pruebas de este módulo.

A grandes rasgos el algoritmo hace los siguiente:
1. Generación de bins iniciales usando **BSG**
2. Selección de bin a desarmar y almacenar cajas en $C$
3. Mientras $C$ no quede vacío o máximo de iteraciones:
   a. Seleccionar caja $c$ de $C$
   b. Seleccionar bin de destino $B$
   c. Usar **BSG** para generar bin $B'$ usando cajas $B \cup \{c\}$, priorizando $c$. Es posible que **BSG** retorne conjunto de cajas residuales $R$
   d. Si $R$ es mejor que $c$, $B$ se reemplaza por $B'$ en el conjunto de bins y $C \gets C \cup R$
 4. Volver a 2 (seleccionar otro bin para desarmar)

Comunicación con solver BSG
--
El solver BSG debería realizar dos tareas principales:

**Generación de bins iniciales**
Se podría implementar un solver básico para MCLP (`basicsolver_mclp.cpp`). Lo que haría este solver sería:
- cargar la instancia desde un archivo en el servidor
- generar bins sin repetir cajas (como ya lo hace una de las funciones del solver)
- retornar por salida estándar la lista de bins generados con los ids de cajas y sus porcentajes de llenado (para ser leído usando *python*)

Los parámetros pueden ser los que tienen relación con la función heurística, la generación de bloques (`min_fr`, `max_blocks`), `n_beams`, y quizás alguno que permita randomizar un poco la generación de bins.

**BSG priorizando subconjunto de cajas**
Idealmente, el solver puede quedar escuchando instrucciones usando el protocolo TCP.
Si es así, el solver no necesitaría volver a cargar la instancia cada vez que es utilizado.

Para hacerlo, en el main se puede implementar una función `listen_instruction()`, la cuál se quede escuchando un puerto específico y retorne el string de instrucciones que reciba. [Aquí](https://www.geeksforgeeks.org/socket-programming-cc/) puedes ver como implementar un socket en c++ (parte del servidor).

Este string podría tener un formato como este:
	
	generate_bin [lista_id_cajas] [lista_cajas_prioritarias]
	
Luego, el string es leído y delegado a la función correspondiente del solver.
Finalmente, el solver debería retornar (por el mismo puerto) una la lista de cajas residuales.

Para enviar instrucciones al servidor por consola:

	echo <instruccion> | netcat localhost <puerto>

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTI3MzY2NjM3NCwtMTE0NDY5NDQzNiwtMT
QyOTc0NDE3NV19
-->