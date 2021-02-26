CLP con restricciones reales (Adolfo, Sebastián)
==


Redacción paper
---
Link del [paper](https://www.overleaf.com/read/fmrmkpttxsgz)

### TODO (Adolfo y Seba)

- Complementar introducción. Sacar ideas de [este paper](%28https://drive.google.com/file/d/10DjpuIa6jcbinnr6foMSsag67MQvvm_w/view%29)
- Agregar sección en donde se explica como integrar las restricciones (ver sección **Integrando restricciones en solver** más abajo).



### Introducción
Escribir una introducción *inspirada* en papers:
> - [2017 - Mathematical models for Multi Container Loading Problems with practical constraints](http://www.optimization-online.org/DB_FILE/2017/07/6140.pdf)
> - [2020 - Selective Breeding Model for Optimizing Multi Container Loading Problems with Practical Constraints](https://iopscience.iop.org/article/10.1088/1757-899X/912/3/032010/pdf)
> - [202X - A MILP Approach for the Multi-Drop Container Loading Problem](https://drive.google.com/file/d/10DjpuIa6jcbinnr6foMSsag67MQvvm_w/view)
> - [2020 - Practical Constraints in the Container Loading Problem: Comprehensive Formulations and Exact Algorithm](https://drive.google.com/file/d/140Cc5hsvMkzfqlAbjS8LQZFJBCIu1YrL/view)


### CLP con Restricciones Prácticas
Explicar CLP (pueden copiar-pegar del [paper VCS](https://drive.google.com/file/d/1q6AP892-bcuZ1LzkxNJmjHw-HVsfgwG4/view)

**Restricciones prácticas**
Escribir una sección en donde se expliquen en detalle las restricciones duras y blandas.
- ¿En qué consisten? (quizás incluir una figura)
- Referencias (quién la propuso)
- Explicar si se considera alguna variación en relación a la original. Argumentar las razones
- Formulación matemática

### BSG-CLP
Incluir sección explicando BSG (por ahora copiar-pegar del [paper VCS](https://drive.google.com/file/d/1q6AP892-bcuZ1LzkxNJmjHw-HVsfgwG4/view))


### Integrando restricciones en solver
Escribir una sección en donde se explique cómo se integran las restricciones al solver.
- Explicación detallada de integración de restricciones duras en validación de las acciones del greedy. Con pseudocódigo si es necesario.
- Explicación detallada de penalizaciones asociadas a restricciones blandas en la función objetivo.

**Orienting greedy (más adelante lo hago)**
Luego vendría una sección sobre cómo *ayudar* al greedy para que, por un lado, no se *bloquee* debido a las restricciones duras,  y por otro, se enfoque en reducir la penalización relacionada con las blandas.
Esto podríamos conversarlo en más detalle.

**Experiments and results**

**Conclusiones**


-----
**De aquí hacia abajo es de la memoria**

---

Integración de restricciones
-- 
**Restricciones duras**
Se incorporan a momento de evaluar las acciones para un estado. Si la restricción no se cumple para la acción, simplemente no se considera

* **Conflicting items.** Se evalúa que las **cajas del nuevo bloque** mantenga distancia adecuada con los elementos en conflicto. Para una implementación eficiente se puede agregar un mapa `type2simple_aabb` que asocie cada tipo de caja con la lista de cajas de ese tipo ya ubicadas en el contenedor.

* **Load bearing.** Se considera que peso de cajas se distribuye proporcional al **área de contacto** de las cajas que se encuentran justo debajo.
Para evaluar una acción se verifica que las cajas **debajo del bloque** que se agrega respeten la restricción.
Para evitar buscar intersecciones de cajas, cada caja colocada o `simple_aabb` puede mantener la lista de simple_aabbs que se encuentran justo por debajo junto al área de contacto. Esta lista se crea al momento de crear un bloque o agregarlo en el contenedor.

* **Cargo stability.** Para cumplir esta restricción, el área de contacto de las cajas inferiores del nuevo bloque debe ser mayor a un $\alpha$%. Esta area se puede obtener directamente usando la estructura especificada más arriba.

**Restricciones blandas**
Se incorporan directamente al momento de evaluar una solucióna modo de penalización, por lo que la función objetivo quedaría:

$\max V(s) - A*MD(s) - B*CS(s) - C*LB(s)$

donde $V(s)$, corresponde al volumen usado por la solución, $MD$ corresponde al *multidrop*, $CS$ a *complete shipment* y $LB$ al *load balance*.

* **Multidrop**: Tiene que ver con la cantidad de movimientos de cajas *adicionales* que se necesitaría realizar para extraer los items de los clientes. El multidrop para un cliente $i$, se estima considerando el número de cajas que se encuentran arriba, y al frente de todas las cajas del cliente $i$ que correspondan a clientes mayores a $i$. Para un cálculo efectivo, cada `simple_aabb` puede guardar la lista de `simple_aabbs` que la están bloqueando. En la función, el término $MD$ puede ser una sigmoide $(c_1,c_2)$.
![image](https://i.imgur.com/AsVnj6w.png)

* **Complete shipment**: Cada caja en la instancia está asignada a un cliente en particular. Complete shipments es el cuociente entre la *cantidad de entregas completas* correspondientes a la solución vs. la cantidad de entregas totales. Se podría sumar el **máximo porcentaje de pedido no completado** (al cuadrado?).
* **Load balance**: Tiene que ver con lo estable que debería estar el contenedor en vista de un futuro traslado. Como factor determinante se considera el ángulo de volcamiento que se genera con el vector que pasa por el centro de masa y un vértice inferior del contenedor y el eje horizontal. El término LB podría ser una sigmoide $(c_1, c_2)$

¿Cómo *ayudar* al greedy a satisfacer las restricciones?
--
* **Conflicting items:** premiar acciones que coloquen items del mismo tipo cerca. Premiar/castigar proporcional a cantidad de cajas por colocar en conflicto.
* **Load bearing**. Premiar cajas que soportan más peso
* **Cargo stability**. Premiar cajas con mayor área
* **Multidrop**. Premiar cajas de clientes con mayor prioridad
* **Complete shipment**. Premiar pedidos más completos
La estrategia podría asignar configuraciones de pesos de manera aleatoria por simulación a los criterios para así obtener mayor diversidad de soluciones.
También, se podría evaluar un sampling aleatorio de acciones.




Experimentos
---
**Instancias de prueba**.
Agregar a instancias BR8:
	* Peso a soportar
	* Tipos de caja = clientes
	* Gamma --> 0.65
	* ==Considerar el doble de cajas==

**Escenarios**
* ==Sin restricciones adicionales==
* Sin restricciones blandas
* 1 escenario para cada restricción blanda
* 1 escenario para las 3 restricciones blandas

**Sintonización**
* Comparar resultados con y sin criterio de evaluación asociando (para distintos valores)

**Tabla**
Para cada escenario mostrar los resultados del mejor valor del parámetro.
Volumen, MD, CS, LB, Valor de la función objetivo penalizada


Load Bearing
--
*Cajas soportan peso máximo*

**Algoritmo**
Es necesario calcular el peso soportado por la caja actual `c`.
````python
def supported_weight(c): #load beraing
  weight <- 0
  B <- cajas justo arriba de c
  Para cada caja b en B:
	area_total <- área justo abajo de b (soportada)
	# cargo stability
	assert(area_total/area_base(b) > factor_estabilidad_vertical(b))
	weight += (area_contacto(c,b)/area_total) * (weight(b)+supported_weight(b))
return weight
````


Trabajo futuro
---
- ¿Como medir cargo stability horizontal?
Se puede calcular un promedio ponderado con el volumen o peso de los bloques
    


Links
--
 - [doc google](https://docs.google.com/document/d/1xqC2JHcyNHvJhVR-0k1AEQt9-J5tetHlkauml5mZXpk/edit)
 - [carpeta](https://drive.google.com/drive/folders/1KW63uK4i-ZZ9D6PuADDV1sGxv-GFhGHe)
 - [tesis](https://drive.google.com/file/d/15Hz83as3dUzeZaU2c3hhjcY_9ujwsBkG/view?usp=sharing)

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzNDIzNjIzNTFdfQ==
-->