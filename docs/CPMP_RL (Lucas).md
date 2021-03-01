Reinforcement Learning - CPMP
==
> [Github-repo](https://github.com/Nyuku/CPMP-AI)  ∙ [Documento](https://docs.google.com/document/d/1FXGGseUqAwt7Xq0Ag-YquqwVLDhlQN-MSzf-r6vqV1I/edit))

TODO
---

### Trabajar en paper

Los objetivos de trabajar en la redacción del paper son:
1. Por un lado, tener algo más concreto, detallado y mejor explicado. Aunque sólo se tengan resultados preliminares, es posible enviarlo a alguna conferencia o revista para obtener feedback.
2. Trabajar en la redacción de un paper nos permitirá mejorar el entendimiento del algoritmo pudiendo vislumbrar maneras de mejorarlo u otras oportunidades.

### Estructura de paper

- Intro
- Background (CPMP, DQN)
- Greedy
- Descripción del algoritmo
- Experimentos
- Conclusiones

Paper referencia: [Deep learning assisted heuristic for CPMP](https://drive.google.com/file/d/1Ih_89cW38mUQYSc_YjrQXOjtKqTgw4KJ/view?usp=sharing)
	
### Pasos recomendados

- Background, Greedy  (basarse en [Greedy2021](https://www.overleaf.com/read/vfmzmfmbvqpt))
- Descripción de la propuesta DQN
- Experimentos y análisis



Representación del problema
---

Un **estado** se representa con la matriz de stacks con los tops de cada un en la primera fila. Los elementos nulos son representados con el máximo group_value,

El **valor de un estado** se calcula $e^{-(p+\alpha g)}$.
Donde $p$ es la cantidad de pasos hasta el **estado actual** y $g$ es la cantidad de pasos estimada hasta un **estado final** de acuerdo a algoritmo *greedy*. $\alpha$ es un parámetro que pondera la estimación (por defecto $\alpha=1$.

La **recompensa** de una acción es simplemente la diferencia de los valores entre el nuevo estado y el anterior.


¿Cómo generalizar tamaños?
--

Se puede entrenar la red con un tamaño estándar (por ejemplo 10 stacks, H=5). Luego, al usarla para predecir, simplemente se seleccionan aleatoriamente grupos de 10 stacks considerando los últimos 5 niveles (si H>5). Se selecciona el movimiento con más repeticiones.

Representación del estado
--
Los estados deberían ser representados por una matriz (o un vector ordenado por filas). En esta matriz los valores e encuentran:
* *compactados:* es decir, forzar a que las diferencias entre group_value seguidos sean iguales.
* *normalizados:* dividir los group_value por max_group_value
* con los top de los stacks en primera fila de la matriz
* espacios vacíos representados por max_group_value

Resultados
---
* Cantidad de problemos resueltos
* En problemas resueltos: pasos de la red v/s greedy inicial


Presentación
---

* Introducción
* Motivación: Hablar del aprendizaje por refuerzo. Objetivo: enseñar a una red a resolver problemas de optimización (premio/castigo)
* DQN: Explicar de manera general el acercamiento. Actor/crítico. Función Loss. (sin entrar en detalles complicados)
* Propuesta: Explicar propuesta de manera general (Uso de DQN para resolver problema de optimización CPMP).
* CPMP: Explicar problema y Greedy que lo resuelve
* Integración DQN+CPMP
	* Input y output de la red
	* Recompensa basada en "evaluación greedy". Explicar concepto de "evaluación greedy". Recompensa final depende de la cantidad de pasos que realizó el modelo (0.95^steps). Recompensas intermedias premian o castigan si mejoran/empeoran "evaluación greedy" y se calculan: Formula
* Resultados preliminares. 
	* Generación de instancias. Entrenamiento (¿en qué consiste?)
	* Pruebas. ¿en qué consisten?
	* Tabla de resultados
* Trabajo futuro: 
	* Aumento incremental de la dificultad de las instancias de prueba (por ejemplo: cantidad de contenedores).
	* Ajuste de hiper-parámetros del modelo. Uso de otras modelos DQN.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTg5MTUzOTI0XX0=
-->