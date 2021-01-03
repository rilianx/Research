
Recommender system
==

TODO
---
* Estudio del estado del arte (hacer resúmenes en drive)
	* En general
	* Películas, música, libro
* Estudiar en más detalle algunos tipo de sistemas de recomendación interesantes
* Estudiar en más detalle sistemas de recomendación basados en reglas asociativas
	* ¿Cómo se extraen/generan las reglas?
	* ¿Cómo se usan en el modelo?

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

### [Recommender system based on pairwise association rules](https://www.sciencedirect.com/science/article/pii/S095741741830441X)
We describe a recommender algorithm that is **independent of any personal user model** and **does not require a complex system of ratings**. Based on a set of observed items selected by a user, the algorithm produces a set of items ranked by confidence of their being observed next. In designing the underlying algorithm, we review existing methods that aim to address similar tasks, adapt them to meet the constraints of the application context that is our primary concern (dietary surveys), and propose a novel alternative. The performance of three methods is compared through the task of recommending omitted foods in a real world dietary recall system. 

---

### [Movie Recommendation using Random Walks over the Contextual Graph](http://curis.ku.dk/ws/files/47059698/recsys2010_cars_workshop.camera_ready.pdf)

![image](https://i.imgur.com/IsJ2cap.png)

Our recommendation algorithm, ContextWalk, is based on modeling the browsing process of a user on a movie database website. In this browsing process, we assume that the user starts with a specific movie (or possibly another entity or contextual feature), and browses the contextual graph, until he finds an interesting node and stops the browsing process. If that node happens to be a movie, this could represent a user taking an interest in that movie with regard to future viewing. ContextWalk was inspired by the work by Craswell et al. [5], who successfully applied a random walk model to image search by modeling the query formulation process of users using the bipartite image-query graph. It was also heavily influenced by the work by Clements et al. [4], who used a random walk model for tag-based search on social bookmarking websites. We extend their models here to include contextual information for movie recommendation and emulate the user’s browsing process by a random walk on the contextual graph.

---

### [Content-based filtering for recommendation systems using multiattribute networks](https://www.sciencedirect.com/science/article/pii/S0957417417305468?casa_token=pc9wg60a1HcAAAAA:-iTxry9b6lQe3dBA4ADwveW1ycxM5ACQDO7fLPupJ-2OjRNRr72Eb0qEHLq2IDl1AvAL6KTvUu-b)
Content-based filtering (CBF), one of the most successful recommendation techniques, is based on correlations between contents. CBF uses item information, represented as attributes, to calculate the similarities between items. In this study, we propose a novel CBF method that uses a multiattribute network to effectively reflect several attributes when calculating correlations to recommend items to users. In the network analysis, we measure the similarities between directly and indirectly linked items. Moreover, our proposed method employs centrality and clustering techniques to consider the mutual relationships among items, as well as determine the structural patterns of these interactions. This mechanism ensures that a variety of items are recommended to the user, which improves the performance. We compared the proposed approach with existing approaches using MovieLens data, and found that our approach outperformed existing methods in terms of accuracy and robustness. Our proposed method can address the sparsity problem and over-specialization problem that frequently affect recommender systems. Furthermore, the proposed method depends only on ratings data obtained from a user's own past information, and so it is not affected by the cold start problem.

### [How good your recommender system is? A survey on evaluations in recommendation](https://link.springer.com/article/10.1007/s13042-017-0762-9)
**¿Cómo evaluar sistemas de recomendación?**
Recommender Systems have become a very useful tool for a large variety of domains. Researchers have been attempting to improve their algorithms in order to issue better predictions to the users. However, one of the current challenges in the area refers to how to properly evaluate the predictions generated by a recommender system. In the extent of offline evaluations, some traditional concepts of evaluation have been explored, such as accuracy, Root Mean Square Error and P@N for top-k recommendations. In recent years, more research have proposed some new concepts such as novelty, diversity and serendipity. These concepts have been addressed with the goal to satisfy the users’ requirements. Numerous definitions and metrics have been proposed in previous work. On the absence of a specific summarization on evaluations of recommendation combining traditional metrics and recent progresses, this paper surveys and organizes the main research that present definitions about concepts and propose metrics or strategies to evaluate recommendations. In addition, this survey also settles the relationship between the concepts, categorizes them according to their objectives and suggests potential future topics on user satisfaction.

---

### [2015 - A Movie Recommender System: MOVREC](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.736.6037&rep=rep1&type=pdf)

It is based on collaborative filtering approach that makes use of the information provided by users, analyzes them and then recommends the movies that is best suited to the user at that time. The recommended movie list is sorted according to the ratings given to these movies by previous users and it uses K-means algorithm for this purpose.

The presented recommender system generates recommendations using various types of knowledge and data about users, the available items, and previous transactions stored in customized databases.

###  Collaborative filtering
Collaborative filtering system recommends items based on similarity measures between users and/or items. The system recommends those items that are preferred by similar kind of users.

### Content-based filtering
Content-based filtering is based on the profile of the user’s preference and the item’s description. In CBF to describe items we use keywords apart from user’s profile to indicate user’s preferred liked or dislikes. In other words CBF algorithms recommend those items or similar to those items that were liked in the past. It examines previously rated items and recommends best matching item.

---
### [2011 - Fusion-based Recommender System for Improving Serendipity](http://ceur-ws.org/Vol-816/divers2011.pdf#page=29)

The system is based on the novel notion that the system finds **new items**, which have the **mixed features of two user-input items**, produced by mixing the two items together. The system consists of item-fusion methods and scoring methods. The item-fusion methods generate a recommendation list based on mixed features of two user-input items. Scoring methods are used to rank the recommendation list. This paper describes these methods and gives experimental results.

**Serendipity** is defined as a measure that indicates how the recommender system can find *unexpected* and *useful* items for users.

Murakami et al. [7] assume that unexpectedness is the distance between the results produced by the system to be evaluated and those produced by primitive prediction methods. Here, primitive prediction methods mean naive methods such as recommendation methods based on user profiles or action histories. They defined an unexpected (U) set of recommendations as follows:

$U = R / P$

$P$ denotes a set of recommendations generated by primitive prediction models and $R$ denotes the recommendations generated by a recommender system to be evaluated. Then, serendipity is defined as follows:

$S = \frac{\sum{u(U)}}{|U|}$, i.e., the utility of the unexpected set divided by the total unexpected elements. 

Database format:
* Item table (Item ID, Feature 1, Feature 2, . . . ) 
* User table (User ID, Profile 1, Profile 2, . . . ) 
* Rating table (User ID, Item ID, Rating)

Public datasets such as MovieLens Data Sets and BookCrossing Data Sets1 already include the above tables.

**Item similarity**
![image](https://i.imgur.com/EBmSm4u.png)

**Collaborative-based similarity**
![image](https://i.imgur.com/dgqES0R.png)

Similar-set for $a$:
$S_a = \{x|sim(x, a) ≥ θ\}$

### Experiments
We conducted the experiments by using 1000 pairs of items selected from the item table at random. Given an item pair (a, b), the xperimental steps are as follows: 

1. Generate a recommendation list R by each item-fusion method (see Section 3.3) for the item pair (a, b). step 
2. 2 Make a ranking list R ′ for the recommendation list R by each scoring method and by each baseline method.
![image](https://i.imgur.com/GymPE42.png)

### [Movie Recommender System Using K-Means Clustering AND K-Nearest Neighbor](https://www.researchgate.net/profile/Arun_Solanki2/publication/334763301_Movie_Recommender_System_Using_K-Means_Clustering_AND_K-Nearest_Neighbor/links/5ed727a7299bf1c67d34e356/Movie-Recommender-System-Using-K-Means-Clustering-AND-K-Nearest-Neighbor.pdf)

### [Artwork Personalization at Netflix](https://netflixtechblog.com/artwork-personalization-c589f074ad76)

### [Recommender system techniques applied to Netflix movie data](https://science.vu.nl/en/Images/werkstuk-postmus_tcm296-877824.pdf)

Recommender systems can be roughly divided into three groups: collaborative filtering, content-based filtering, and hybrid filtering. 

**Collaborative filtering** is a recommender technique that focuses on the interest of the user, by using preferences of other similar users. The psychology behind this approach is that if user 1 and user 2 can be considered as having the same interests, one can assume user 1 has also the same opinion about a new item only user 2 has already an opinion of. Sarwar et al. (2001) [5] divide collaborative filtering into two categories: *memory-based collaborative filtering* algorithms and *model-based collaborative filtering* algorithms.

**Memory-based algorithms** or **user-based collaborative filtering** use all available user-item data to generate a prediction. Based on all data it determines the most related users, similar to the target user. These neighbours are similar because they have statistically common interests. To determine these so-called neighbours, several statistical techniques are used. Finally, the top 𝑛 most similar items are recommended for the target user.

The advantage of user-based collaborative filtering is the **sparsity and scalability**. Many recommender systems use data with lots of users and items, but with relatively few number of actual ratings. User-based collaborative filtering only uses necessary data, which reduces the run time.

**Model-based collaborative filtering** first builds a model of user ratings only. To do this, it uses several machine learning techniques, such as clustering, rule-based and Bayesian network approaches. Each of the machine learning techniques uses its own approach. The clustering model formulates collaborative filtering as a classification problem, while the Bayesian network model treats it as a probabilistic model and the rule-based model as an association-rule model. The model-based collaborative filtering algorithms are also called item-based collaborative filtering algorithms.

Next to collaborative filtering, one is also able to build recommender systems by using the content of items, and a profile matched to items. This approach is called **content-based filtering**. Lops et al. (2011) [6] stated that the recommendation process of a content-based recommender system basically consists of *matching the attributes of a user profile against the attributes of a content object*. The outcome of this process is just the level of the user’s interest in an object. It is crucial for a content-based model that the user profile is accurate.

A weakness of collaborative and content-based filtering mentioned by Lika et al. (2014) [7] is the problem of handling new users or items. Both techniques mentioned before are based on historic data of the users or items. This well-known problem is often called 7 the **cold-start problem**. 

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
eyJoaXN0b3J5IjpbODgyODkzMjQwLC0xODM3NjM4Mjk1LDE3Nj
U1ODUzNTIsLTcyMjMxMDgzNSwyODY4Njk3MjAsLTE5NDcyOTQ0
NSwtMTU5NTIwMzczMCwtMTgyMjAzMzk2OSwtNTI2NjMwOTA2LC
01MjE4MDU1NTQsLTE4NDE0NzY2MjAsLTE1NTg2MDU0MjMsMTE4
MTEzNDc2OV19
-->