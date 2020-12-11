
Recommender system
==

TODO
---
* Estudio del estado del arte (hacer resúmenes en drive)

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

Algunos papers
--

[Recommender system based on pairwise association rules](https://www.sciencedirect.com/science/article/pii/S095741741830441X)
We describe a recommender algorithm that is **independent of any personal user model** and **does not require a complex system of ratings**. Based on a set of observed items selected by a user, the algorithm produces a set of items ranked by confidence of their being observed next. In designing the underlying algorithm, we review existing methods that aim to address similar tasks, adapt them to meet the constraints of the application context that is our primary concern (dietary surveys), and propose a novel alternative. The performance of three methods is compared through the task of recommending omitted foods in a real world dietary recall system. 

[Movie Recommendation using Random Walks over the Contextual Graph](http://curis.ku.dk/ws/files/47059698/recsys2010_cars_workshop.camera_ready.pdf)

![image](https://i.imgur.com/IsJ2cap.png)

Our recommendation algorithm, ContextWalk, is based on modeling the browsing process of a user on a movie database website. In this browsing process, we assume that the user starts with a specific movie (or possibly another entity or contextual feature), and browses the contextual graph, until he finds an interesting node and stops the browsing process. If that node happens to be a movie, this could represent a user taking an interest in that movie with regard to future viewing. ContextWalk was inspired by the work by Craswell et al. [5], who successfully applied a random walk model to image search by modeling the query formulation process of users using the bipartite image-query graph. It was also heavily influenced by the work by Clements et al. [4], who used a random walk model for tag-based search on social bookmarking websites. We extend their models here to include contextual information for movie recommendation and emulate the user’s browsing process by a random walk on the contextual graph.

[Content-based filtering for recommendation systems using multiattribute networks](https://www.sciencedirect.com/science/article/pii/S0957417417305468?casa_token=pc9wg60a1HcAAAAA:-iTxry9b6lQe3dBA4ADwveW1ycxM5ACQDO7fLPupJ-2OjRNRr72Eb0qEHLq2IDl1AvAL6KTvUu-b)
Content-based filtering (CBF), one of the most successful recommendation techniques, is based on correlations between contents. CBF uses item information, represented as attributes, to calculate the similarities between items. In this study, we propose a novel CBF method that uses a multiattribute network to effectively reflect several attributes when calculating correlations to recommend items to users. In the network analysis, we measure the similarities between directly and indirectly linked items. Moreover, our proposed method employs centrality and clustering techniques to consider the mutual relationships among items, as well as determine the structural patterns of these interactions. This mechanism ensures that a variety of items are recommended to the user, which improves the performance. We compared the proposed approach with existing approaches using MovieLens data, and found that our approach outperformed existing methods in terms of accuracy and robustness. Our proposed method can address the sparsity problem and over-specialization problem that frequently affect recommender systems. Furthermore, the proposed method depends only on ratings data obtained from a user's own past information, and so it is not affected by the cold start problem.

[How good your recommender system is? A survey on evaluations in recommendation](https://link.springer.com/article/10.1007/s13042-017-0762-9)
**¿Cómo evaluar sistemas de recomendación?**
Recommender Systems have become a very useful tool for a large variety of domains. Researchers have been attempting to improve their algorithms in order to issue better predictions to the users. However, one of the current challenges in the area refers to how to properly evaluate the predictions generated by a recommender system. In the extent of offline evaluations, some traditional concepts of evaluation have been explored, such as accuracy, Root Mean Square Error and P@N for top-k recommendations. In recent years, more research have proposed some new concepts such as novelty, diversity and serendipity. These concepts have been addressed with the goal to satisfy the users’ requirements. Numerous definitions and metrics have been proposed in previous work. On the absence of a specific summarization on evaluations of recommendation combining traditional metrics and recent progresses, this paper surveys and organizes the main research that present definitions about concepts and propose metrics or strategies to evaluate recommendations. In addition, this survey also settles the relationship between the concepts, categorizes them according to their objectives and suggests potential future topics on user satisfaction.


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
eyJoaXN0b3J5IjpbLTE1OTUyMDM3MzAsLTE4MjIwMzM5NjksLT
UyNjYzMDkwNiwtNTIxODA1NTU0LC0xODQxNDc2NjIwLC0xNTU4
NjA1NDIzLDExODExMzQ3NjldfQ==
-->