
Recommender system
==

TODO
---

**Algoritmo basado en *calificaciones* y similitud de películas.**

* Evaluar la precisión del algoritmo.
 
Para evaluar los resultados se pueden usar listas de películas ranqueadas de distintos usuarios.
Para obtener la info se puede acceder a [esta página](https://letterboxd.com/members/)

Con la lista de películas calificadas de un usuario, se divide un un conjunto de entrenamiento (conjunto con el que se obtienen los valores R_ij = S_ij * c_i), y un conjunto que se usará para evaluar la predicción.
 
---


Usar como referencia paper: [2018 - Recommender system techniques applied to Netflix movie data](https://science.vu.nl/en/Images/werkstuk-postmus_tcm296-877824.pdf) 


* Comparar algoritmos de recomendación:
  * Basado en contenido (content-based)
  * Collaborative filtering (usando matrices no?)
  * ...
* Definir experimentos (¿en qué consisten?):
  * Tipos de datos, atributos, cantidad
  * ¿Cómo se evalúa qué tan buena es una recomendación? Por ejemplo, el objetivo de la recomendación puede ser el de predecir la nota que el usuario pondrá a una película, por lo tanto la recomendación se puede evaluar usando el **error en la predicción**.
  * Definir métrica para comparar algoritmos.

Plan
--

**A. Estudiar papers sobre sistemas de recomendación**.

1. Usar string de búsqueda (google scholar):
	* *"Recommender system"* (year > 2016)
	* *"Recommender system" survey* (year > 2016)
	* *"Recommender system" movies* (year > 2010)
	* *"recommender system" issues challenges* (year > 2016)
2. Identificar tipos de sistemas de recomendación y componentes principales. 
3. Identificar sistemas de recomendación para películas. Identificar entrada y salida del sistema. ¿Datos de entrenamiento? ¿Qué trata de predecir?
4. Identificar desafíos (challenges) que enfrentan los sistemas de recomendación actuales (ojalá de películas).
5. Hacer resúmenes de trabajos más relevantes.

**B. Implementar grafo implícito de películas/listas** en Python (reusar partes del código de [Luciano](https://github.com/LucianoSm20/SistemaRecomencion/tree/RamaA))
* Acceder a películas por `id_imdb`
* Obtener listas (de películas) asociadas a una película
* Obtener películas de una lista
* Almacenar datos en archivos para listas y para películas

![Recommender](https://docs.google.com/drawings/d/e/2PACX-1vRurmmKDmPIcA1du6WLIfr10vU2IAUpZINUD3e9tSEGi5C4Sd2xhek7eQ1aYGsomN8x_Fsb5c-GCyow/pub?w=595&h=431)

**C. Diseñar e implementar sistema de recomendación en Python.**
IDEA: A partir de un *conjunto de películas*, recomendar películas parecidas.

Aquí una idea: [Random-walk-based](https://docs.google.com/document/d/1MwCHRQrpEGXJ_ZP05_yOf6V1xlLX0rtAHdaS2zDs1Ro/edit#heading=h.a9hq177vtke9)



Algoritmo (idea)
---
El objetivo del algoritmo es recomendar películas en base a un pequeño conjunto de películas de origen o *películas fuente*.

Imaginemos que cada película fuente tiene una esencia o *color*. La idea del algoritmo es:
1. Propagar estos colores a través de las otras películas del grafo. El grafo se comporta similar a una *cadena de Markov*. En cada iteración, los últimos valores propagados se propagan a los nodos adyacentes.
2. Recomendar las películas con mayor diversidad de colores.

Sea $F$ el conjunto de películas fuente. 
El grafo es bipartito, que se compone de nodos de tipo *Película* y nodos de tipo *Lista de pelis*. Los nodos de tipo película `m`cuentan con dos atributos importantes:
* `color[m]`    Vector con valores en $[0,1]$, que indican la presencia de cada uno de los colores de las películas fuente.
* `P[m]` Vector con el valor que se debe propagar en la siguiente iteración o *timestep* del algoritmo 

````python
import numpy as np

def main(F, M, steps=5):
  #inicalizando la fuente
  P = dict()
  for m in F:
     color[m] = np.array(len(F))
	 color[m][F.index(m)] = 1.0
     P[m] = np.array(len(F))
	 P[m][F.index(m)] = 1.0 
	 
  #propagación por algunas iteraciones
  for timestep in range(steps):
	P= propagate(P)
	
  #recomendación
  return recommend(M)
````  

Notar `F` es una lista con las películas fuente. Por lo que al colocar: `color[m][F.index(m)]=1.0`, estamos creando un vector: $[0,...,1,...,0]$ donde el $1$ se encuentra en la posición correspondiente a la película fuente en la lista `F`. Lo mismo ocurre con `c_propag`. `M` es la colección con todas las películas.

`P` es un diccionario que guarda en cada iteración la películas que debieran propagar sus valores. Cada película se asocia al vector de colores que se debe propagar.

La función `propagate` propaga los cambios a partir del diccionario de películas `P` y retorna un nuevo diccionario con las películas modificadas para seguir propagando.

````python
def propagate(P, t_factor=0.1):
  P2 = dict() #películas que se propagarán en 
                # la siguiente iteración
  for each m in P:
     for each l in adj_lists(m):
       for each adj_m in l.movies:
         size_list = len(l.movies)
         propag_value = (P[m]*t_factor)/size_list
         P2[adj_m] = max(propag_value, P[adj_m]) 

  #se actualiza el color de las películas
  for each m in P2: color[m] += P2[m]
  
  return P2
````

`t_factor` es la tasa de propagación de los colores de un nodo a otro.

La función `recommend(G)` debería usar algún criterio para entregar una lista de películas en base a sus colores. Idealmente queremos maximizar todos los colores del vector, ya que valores altos para **todos los colores** indicarían que la película se parece a todas las películas fuente.

La función propuesta simplemente retorna la película que **maximiza el mínimo valor del vector**.

````python
def recommend(M):
  maxmin=0.0
  for each m in M.movies():
    min_color = np.min(color[m])
    if min_color > maxmin:
      maxmin = min_color
      rec_movie = m
  return rec_movie, maxmin
````

Mejora
---
**Idea:** 
1. Generar árboles de decisión que agrupen películas fuente con alta pureza. Basarse en atributos genéricos (año, director, guionista, país, géneros, actores principales)
2. Generar *listas auxiliares* con grupos obtenidos.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzMDg5NTQ4NiwyMDgwMjUwOTc1LDEyMT
I3ODgzNzAsLTE4ODQ1NzAwNzgsODgyODkzMjQwLC0xODM3NjM4
Mjk1LDE3NjU1ODUzNTIsLTcyMjMxMDgzNSwyODY4Njk3MjAsLT
E5NDcyOTQ0NSwtMTU5NTIwMzczMCwtMTgyMjAzMzk2OSwtNTI2
NjMwOTA2LC01MjE4MDU1NTQsLTE4NDE0NzY2MjAsLTE1NTg2MD
U0MjMsMTE4MTEzNDc2OV19
-->