Predicting student performance in computing courses based on programming behavior
==

### TODO
- Terminar con análisis de atributos :ok:
- Matriz de correlación labs 3 y 4 (predictoras vs objetivo)
- Repetir experimento (conglomerado lab3-4) para obtención de coeficientes Gini de variables predictoras. Realizar también para regresión lineal.
- Explicar procedimiento
- Repasar introducción (contribuciones)
- Conclusiones



### Paper

- Abstract
- Intro :ok:
- Metrics
- Experiments
	- Data Collection y variables :ok:
	- Procedure
	- Correlación de variables
	- Modelos predictivos
	- Análisis de predictores
- Conclusiones

Links:

> - [Using Programming Process Data to Detect Differences in Students' Patterns of Programming](https://sci-hub.se/10.1145/3017680.3017785)

Abstract
---

Ayudar de manera temprana y personalizada a los alumnos que tienen mayores dificultades resolviendo problemas de código es fundamental para  mejorar el desempeño en las asignaturas de programación.

Para tal fin, se hace deseable y necesario detectar a tiempo a aquellos alumnos que presenten patrones conductuales de bajo rendimiento.

En este trabajo, analizaremos, con un modelo estadístico, la relación existente entre una serie de datos extraídos de una plataforma de programación virtual y las calificaciones obtenidas por los estudiantes  en las instancias de evaluación individuales. La herramienta CodeRunner permite realizar ejercicios de código y entrega retroalimentación inmediata a los estudiantes sobre errores de compilación y ejecución. En la escuela se utiliza hace algún tiempo en los ramos de Fundamentos de Programación (8 semestres) y Estructura de Datos (6 semestres).

>  [tablita de resultados](https://docs.google.com/spreadsheets/d/1xsDs9ov-X9dYYZN2RpkTmVngrGAhJww1FxfhFckyhi0/edit?ts=5f7b6447#gid=0): atributos más importantes para cada modelo
> [Paper](https://www.overleaf.com/7645516685xtwjkrbxrqfv) ∙ [Breve Escrito](https://drive.google.com/file/d/1-v2PCrE5WWuAHUAM8brDkWSPJb7qPPXu/view?usp=sharing) ∙ [Documento](https://docs.google.com/document/d/1dUICocY5QTchHlduz-gUTFHLoHi2ZSNOctBCjjNcpDc/edit#) ∙ [Tabla resultados](https://docs.google.com/spreadsheets/d/1xsDs9ov-X9dYYZN2RpkTmVngrGAhJww1FxfhFckyhi0/edit?ts=5f7b6447#gid=0) ∙ [Entrevista](https://drive.google.com/file/d/1JTUxY0T8-jlIMr-DVqbL-TkDwSS2l_8x/view?usp=sharing) ∙ [Colab](https://colab.research.google.com/drive/1wxa3EcwF5qdCBR7LuuvRtR6zbvAmN9yW?usp=sharingiKhAqXwgqj_9NRDyX9_DCG7_4415Urpy)

Experimentos finales
---
**Estrategia:** RandomSearchCV/GridSearch (AttributeSelector +FeatureElimination + Estimador).

* Estimadores: SVR, RF, Lineal, ANN
* Mejores características
* Data (lab1, lab1-lab2, lab1-lab3, lab1-lab4)
*Obtener mejores atributos
* Buscar mejores hiper-parámetros usando usando GridSearch o RandomSearch
* Data (lab1, lab1-lab2, lab1-lab3, lab1-lab4)
	* Consolidados por lab
	* Aplicar log a contadores (intentos, desconexiones)
	* Normalizar por semestre (y no por columna completa)
* Target: p1p2, np, prom
* Métricas: $R^2$, $MSE$


Ideas para mejorar predicción (preprocesamiento)
--

Para mejorar los resultados propongo las siguientes modificaciones en el preprocesamiento de datos:
* `max_attempts` (intentos en pregunta con máxima cantidad de intentos)
* `avg_time_attempt` (tiempo promedio por intento)
* attempts -> log(attempts+1)
* disconnections -> log(disconnections+1)

Además normalizar **por semestre** (en vez de todos juntos) entorno al promedio (**Zero Mean Unit Variance**)

```python
import numpy as np
eg_array = 5 + (np.random.randn(10, 10) * 2) #arreglo de ejemplo

# normalizing Zero Mean Unit Variance
normed = (eg_array - eg_array.mean(axis=0)) / eg_array.std(axis=0)
```
Esto con el objetivo de reducir impacto de atributos que dependen del semestre, por ejemplo, dificultad en la prueba, ayuda en el laboratorio, modificaciones menores de algunas preguntas, tiempo disponible para hacer el laboratorio.


Atributos
--

**TARGET**

	'p1': ['p1'],
	'p2': ['p2'],
	'np': ['np'],
	'p1p2': ['p1p2'], # Promedio p1p2 y p2p2
	'p2p2': ['p2p2'],

**FEATURES**

*Por Lab*

	'mean(p$p2)', 
	'g_lab1', 
	'a_lab1', #attempts
	'ut_lab1', #user time
	'act_lab1', #active time
	'norm_log(dis_lab1)', 
	'ct_lab1', #compilation time
	'rt_lab1', #relative time?
	'ctr_lab1', #relative compilation time
	'rtr_lab1', 
	'err_lab1', #errors?
	'cer_lab1', 
	'actq1_lab1', #active quartiles
	'actq2_lab1', 
	'actq3_lab1', 
	'mean(qg$_lab1)', 
	'norm_log(sum(qat$_lab1))', 
	'mean(qact$_lab1)', 
	'mean(qavt$_lab1)', 
	'max(qme$_lab1)', 
	'max(qmce$_lab1)', 
	'mean(qmsr$_lab1)', 
	'mean(qc$_lab1)'

*Por pregunta*

	'questionsdifficulty': ['qd$_lab#'],
	'questionsgrades': ['qg$_lab#'], # Promedio
	'questionsattempts': ['qat$_lab#'], # Sumar - Max
	'questionsactivetime': ['qact$_lab#'], # Promedio
	'questionsavgtime': ['qavt$_lab#'], # Promedio
	'questionsmaxerrors': ['qme$_lab#'], # Max
	'questionsmaxconsecutiveerrors': ['qmce$_lab#'], # Max
	'questionsmaxsimilarityratio': ['qmsr$_lab#'], # Promedio
	'questionscorrectness': ['qc$_lab#'] # Promedio



### METODOLOGÍA

Describa brevemente y con claridad la metodología que utilizó para llevar a cabo su proyecto, las acciones y actividades realizadas y la manera en cual evalúo los resultados de obtenidos (máximo 400 palabras).

En este proyecto se analizó la relación existente entre la conducta de los estudiantes en una actividad formativa y su desempeño en una evaluación sumativa.

La principal hipótesis es que existe una relación significativa entre la **conducta del estudiante** y su **desempeño**. Es más, se cree que es posible **predecir el desempeño de un estudiante** analizando su comportamiento en las **actividades formativas del curso**.

Se realizó una investigación de tipo observacional. Su usó un acercamiento cuantitativo, ya que los datos conductuales del estudiante fueron obtenidos de su historial en CodeRunner y transformados en valores numéricos.

Se realizó un estudio correlacional con el objetivo de determinar la relación existente entre los datos conductuales y el desempeño del estudiante en la evaluación sumativa. El estudio fue longitudinal ya que se analizaron varios semestres (alrededor de 6 semestres y 200 alumnos) para la asignatura de Estructura de Datos.

**Recolección de datos**

Los experimentos se realizaron usando la información recolectada durante 6 semestres en el curso de “Estructura de Datos” de la carrera de Ingeniería Civil en Informática. En este curso, los estudiantes aprenden teoría relacionadas a distintas estructuras de datos tales como “listas enlzadas”, “tablas hash” o “árboles binarios”. Además, el curso incluye sesiones (laboratorios) y trabajos prácticos en las cuales se aprende a implementar las diferentes estructuras usando el lenguaje de programación C. Las notas finales de los estudiantes se obtienen de las notas de laboratorios (20%), tareas de programación (20%), controles en clases (20%), 2 pruebas sumativas (20%) y un proyecto grupal (20%).

Para realizar los laboratorios, los estudiantes usan **Code Runner**, un plugin de Moodle que permite implementar, compilar y probar códigos (ejercicios), entregando retroalimentación inmediata. Todos los datos de cada estudiante relacionados a la cantidad de intentos, errores, códigos no terminados, marcas de tiempo, etc., son almacenados en la base de datos MySQL de Moodle.  Por lo tanto, toda la información referente a las **variables predictoras** se obtiene de esta base de datos.

Los laboratorios cuentan con sesiones presenciales de 70 minutos, sin embargo, el tiempo total que tienen los estudiantes para realizarlos fluctúa entre 5 y 7 días. El curso se dicta semestralmente y los datos analizados cubren un periodo de 6 semestres (2017-2019) con un total de 224 estudiantes.

Por cada laboratorio y estudiante se extrajeron los siguientes atributos:

Relacionados principalmente con las habilidades de los estudiantes:

* Número total de intentos. Es de suponer que los “buenos” estudiantes realicen menos intentos en el laboratorio, sin embargo no siempre es así, ya que según lo indican estudios previos, los buenos estudiantes tienden a “probar” más el código y así encontrar errores más rápidamente. Es posible también, que alumnos con dificultades realicen muchos intentos en algunos ejercicios y luego pidan ayuda con los más difíciles reduciendo el promedio.

* Tiempo activo: corresponde tiempo total que el estudiante estuvo trabajando en los ejercicios. Para obtener este dato se analizan las marcas de tiempo de los intentos y se establece un límite máximo para considerar que dos intentos consecutivos fueron realizados durante una misma sesión (y no hubo desconexiones entremedio).

* Tiempo promedio antes de realizar el primer intento de cada ejercicio.  De acuerdo al análisis reportado en [5], este tiempo contribuye negativamente al éxito de los estudiantes. Al parecer es preferible que los estudiantes dediquen más tiempo observando el comportamiento y errores del programa en ejecución que tratando de escribir un primer intento sin errores.

* Proporción de tiempo activo con errores de compilación. Los “buenos” estudiantes dedican más tiempo reparando errores de ejecución que de compilación [7].

* Proporción de intentos con errores de compilación.

* Tasa de reducción de errores: corresponde a la proporción de intentos consecutivos con una reducción en el número de errores de compilación. Esta métrica se deriva de dos métricas propuestas en otros trabajos (Error Quotient y Watmin Score)

Relacionados con la motivación del estudiante:

* Cuartiles de tiempo activo: instantes de tiempo en que el estudiante llevaba un 25%, 50% y 75% del tiempo total dedicado al laboratorio. Se esperaría que en estudiantes “motivados” estos tiempos fueran menores o más cercanos entre sí.

* Número de desconexiones: estimación del número de veces que el estudiante dejó de hacer el laboratorio para “probablemente” dedicarse a hacer otra actividad.

* Tiempo activo: se piensa que una gran cantidad de tiempo activo indicaría (a) que al estudiante le cuesta y (b) que el estudiante se esfuerza, por lo tanto  es una variable que apuntar tanto a las habilidades del estudiante como a su motivación.

Relacionados con la autonomía del estudiante:

* Similitud entre respuestas: Se calcula la máxima similitud entre la respuesta del estudiante y todos sus compañeros que terminaron antes el laboratorio. Una similitud muy alta (cercana a 1) indicaría que al alumno lo ayudaron o incluso que copió la respuesta correcta. El primer alumno en terminar el laboratorio tiene una similitud igual a 0.

Los datos relacionados al desempeño del estudiante en evaluaciones sumativas (**variables de respuesta**) se obtuvieron directamente de las planillas de notas de cada semestre. Se consideraron 3 variables de respuesta: promedio de puntajes en sección de las pruebas con ejercicios similares a los del laboratorio, promedio de notas en las pruebas y promedio final.








<!--stackedit_data:
eyJoaXN0b3J5IjpbODYxMzc1ODAsMTg4NjUzMzQ1NSwyMDU0OT
MyNTE5LDI2NTg4MTY4LDE4NDg3OTY4MzMsLTEwODYxNDQ2NDYs
LTU2NjU0Nzc5MCwtMTA4MjgwODc0NiwxOTU1MDUyMzY0LC0xNz
M3NjU2NTUwLC0yMjExOTMwNjcsNzQyOTU3MTMsMjA0MzYwMDA0
NSwxNDY5Mzc5NTUxLC0xMjQwMTE1MTEyLDE5NzY4ODE0OTEsLT
EwNDU0Mzk4NjUsLTkxMDk5NDI1LC00NDc0NzQ1NTIsLTExNDcw
NjcyODhdfQ==
-->