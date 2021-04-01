Recomendador de películas (Luciano)
==

**Abstract**
In order to improve the prediction of movie recommender systems we propose to add classification attributes to the movies. We include classifications based on emotions and director-likeness for each movie. In order to classify movies we train machine learning predictors based on user's comments of selected sets of movies.

We implement a recommender system which uses a simple similarity function for comparing attributes of pair of movies. Parameters of the similarity function are fitted according to some defined scores. We show that by adding the new classification attributes, the recommendations improves significantly in terms of utility, diversity and serendipity.

### Papers
> [2018 - Recommender system techniques applied to Netflix movie data](https://science.vu.nl/en/Images/werkstuk-postmus_tcm296-877824.pdf) --> Resumen de sistemas de recomendación
>  [2017 - How good your recommender system is? A survey on evaluations in recommendation](https://link.springer.com/article/10.1007/s13042-017-0762-9)
>  [2011 - Fusion-based Recommender System for Improving Serendipity](http://ceur-ws.org/Vol-816/divers2011.pdf#page=29) --> función de similitud y Serendipity


TODO
---
- Leer [paper](https://mail.google.com/mail/u/0/#search/serendipity/KtbxLwGkKGhCrrMZSPkZQhlpcPcdTdDdxV?projector=1&messagePartId=0.1)
- Diseñar función de similitud (item similarity) en base a parámetros/pesos ajustables --> para próxima semana.
- Diseñar experimentos (basados en listas de usuarios) y que apunten a *utility*, *diversity* y *serendipity*.
- Función `eval_utility` que reciba el vector de pesos v y el conjunto de listas. Selecciona una película random de cada lista, llama al recomendador para que retorne N películas las que se comparan con las películas de la lista. La función retorna la cantidad de aciertos dividida por la cantidad de listas.

### Paper

- Abstract
- Introduction
	- Contexto del problema
	- Se menciona un poco lo que se ha hecho (estado del arte en general y lo más relacionado con nuestra propuesta)
	- Se resume la propuesta destacando la contribución (adición de vectores usando análisis de texto)
- Background
	- Explicar el problema de manera más formal
	- Conceptos y definiciones (utilidad, serendipity)
	- Se explicar fórmula para calcular similitud (sacada de otros trabajos)





**Experimentos**

**Utility**
- Instancias de prueba: Listas en internet de a lo más 100 películas.
- A partir de 10 películas de cada lista, buscar las 10 más parecidas según *función de similitud*.
- El éxito puede medirse como el % de películas recomendadas que se encuentran en la misma lista que la película original.
- Ajuste automático de parámetros con el objetivo de maximizar éxito.
- Comparar usando atributos simples y atributos basados en comentarios (emotions & director-likeness)

* Serendipity, unexpectedness, coverage, utility 

**Función de similitud**
Suma ponderada de distancia entre atributos.

<img src="https://render.githubusercontent.com/render/math?math=s(m_1,m_2)= 1- \frac{\sum_{i=1}^n w_i * d(a_i^{m_1},a_i^{m_2})}{\sum_{i=1}^n w_i}">

Distancia entre atributos numéricos (e.g., año, votos, rating):

<img src="https://render.githubusercontent.com/render/math?math=d(a_i^{m_1},a_i^{m_2}) =\frac{|a_i^{m_1}-a_i^{m_2}|}{\max a_i - \min a_i}">

Para atributos que consisten en listas de categorías (e.g., lista de géneros, lista de actores, lista de directores), la distancia se puede calcular:

<img src="https://render.githubusercontent.com/render/math?math=d(a_i^{m_1},a_i^{m_2}) =\frac{|a_i^{m_1} \cap a_i^{m_2}|}{|a_i^{m_1} \cup a_i^{m_2}|}">,

es decir, la cardinalidad de la intersección de categorías dividida por la cardinalidad de la unión de ellas. Por ejemplo si la película m_1 tiene los géneros de {terror, acción} y la película m_2 cuenta con los géneros de {terror, romance y comedia}, entonces la distancia entre ellas será: 1/4=0.25

**Función para evaluar utilidad en base al vector de pesos**

N listas

1. Toma la primera lista L
2. Selecciona una película al azar P
3. Se obtienen 10 recomendaciones para P ( R )
4. Se cuentan los aciertos.

Retornar promedio de aciertos (hits) por lista.

**Ajustar valores de los pesos **

````python
def hill-climbing(initial_weights):
   v = initial_weights
   max_hits = eval_utility(v)
   no_improvements = 0
   while no_improvements<50:
      i = random_weight(v)
      old_value = v[i]
      v[i] = random_value (v[i])
      hits = eval_utility(v)
      if hits > max_hits :
         max_hits = hits
         no_improvements = 0
      else:
         v[i]= old_value
         no_improvements += 1
````

-----


Paper
---

* Abstract
* Introducción. Basarse en papers de más arriba.
	* Sistemas de recomendación (tipos)
	* Evaluación de sistemas de recomendación (utility, serendipity, etc.)
	* Análisis/clasificación de texto
* Background
	* [Función de similitud](http://ceur-ws.org/Vol-816/divers2011.pdf#page=29)
	* Clasificación de texto. Metodología usada por nosotros. Random Forest.
* Propuesta
	* Clasificador de películas en base a comentarios
	* Agregar atributos a la función de similitud
* Experimentos
	* Explicar el experimento propuesto y los objetivos



Links
--
- [doc Luciano](https://docs.google.com/document/d/19U-QQPkoYKXeftjGTMlqgTik4FUdhxtOGscaIN46cA8/edit#)
- [carpeta](https://drive.google.com/drive/folders/1dx_I57lU3nh45LKvq-spKqGjat4LsEIT)
- [colab](https://colab.research.google.com/drive/1xmwnyA3oZazqGUSLQKT-3OYBDESkGdc_)

<!--stackedit_data:
eyJoaXN0b3J5IjpbMjc0NzYzOTcsOTY3OTI3NjgxLC0xNDIzNT
Y0Njg3LDE4OTMxNzIyMzMsLTE2NTk4OTAzNSwyMjU2OTQxMTgs
LTE4NjAxMDE4MDNdfQ==
-->