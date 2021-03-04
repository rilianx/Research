IpOPT para IbexOpt
==

Upper bounding is a very important component of branch & bound solvers for global optimization. Finding good quality solutions early in the search may improve the performance of the solver by means of the addition of the auxiliary constraint $f(x)<ub$, where $ub$ is the cost of the best found solution so far.

IpOPT is a well know local optimizer that can be used for finding solutions in B&B global optimizers, however it is too expensive to be called in each node of the search tree.

In this work, we propose a mechanism for applying IpOPT only in some nodes of the search tree in order to avoid a large time overhead but keeping the effectiveness of the method.

> [TODO](https://docs.google.com/document/d/1P0yYlNuIu-I2taOfEJMDzq-FMiMf7y_uyqXVvFZ8ssE/edit#) ∙ [PaperBaron](http://mpc.zib.de/archive/2018/3/Khajavirad-Sahinidis2018_Article_AHybridLPNLPParadigmForGlobalO.pdf) ∙  [Resultados](https://drive.google.com/file/d/1-EYDoR6nBFgXzq4WG_mMaLD3YkfAv1Fe/view?usp=sharing)
> 
Actualmente tenemos 3 variantes:
* Ipopt sólo
* Ipopt para encontrar solución inicial, luego IbexOpt
* IbexOpt con Ipopt para buscar soluciones

**TODO**

- Avanzar con mecanismo para decidir cuando aplicamos IpOPT.
- Mostrar la tablita
- In

Mecanismo:
- [ ] Seguir diseñando mecanismo para seleccionar cuándo aplicar Ipopt (T>1).
- [ ] ¿Qué atributos del nodo influyen en la efectividad de IpOpt?
- [ ] Tiempo ipopt



---
**Mecanismo para decidir cuando aplicar Ipopt**
Tomar en cuenta tiempo y mejora (en %) de intervalo objetivo
Vale la pena aplicar Ipopt cuando:
>- mejora considerablemente la calidad de la mejor solución
> - la mejora implica una reducción considerable en el tamaño del árbol de búsqueda (impacto de Y?)


**Comando para compilar**

	g++ -I/home/erick/ibex-lib/include/ibex/ -I/home/erick/ibex-lib/include/ibex/3rd -L/home/erick/ibex-lib/_build_/3rd/lib -std=c++11 -g -DNDEBUG -L/home/erick/ibex-lib/lib/ibex/3rd -L/home/erick/ibex-lib/lib /home/erick/ibex-lib/plugins/optim/main/ibexopt.cpp -Wl,--start-group -libex -lamplsolvers -lipopt -lgaol -lgdtoa -lultim -lsoplex -lz -ldl -Wl,--end-group -Wall -Wno-deprecated -Wno-unknown-pragmas -Wno-unused-variable -Wno-unused-function -Warray-bounds -v -o ibexopt -Wl,--rpath -Wl,/home/erick/CoinIpopt/lib -L/home/erick/CoinIpopt/lib -L/usr/lib/gcc/x86_64-linux-gnu/7 -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib -L/lib/../lib -L/usr/lib/../lib -L/usr/lib/gcc/x86_64-linux-gnu/7/../../.. -llapack

Selección dinámica del solucionador local (BARON)
---
  

1.  Se asocia una tasa de éxito
    
	1.  Para el límite superior (upper bounding), el solucionador local gana, si devuelve una solución que pasa la prueba de viabilidad y mejora el valor del límite superior conocido
    
	2.  Para el límite inferior, el solucionador local gana, si devuelve solución que satisface las [condiciones KKT](http://apmonitor.com/me575/index.php/Main/KuhnTucker)
    

2. Para cada solucionador local, se guarda el número total de victorias en la rama, para (a) se denota $N_{wins}$  y para (b) el número de ganancias o pérdidas consecutivas  denotado por $N_{consecutivas}$ donde el número positivo indica número de victorias consecutivas, mientras que un número negativo denota derrotas consecutivas

Además, si m victorias consecutivas , son seguidas por una pérdida , luego Nganancias se reestablece a cero.

Finalmente, definimos un rango rs ∈ [1 ,  r ] para cada solucionador s . En un nodo dado, los solucionadores se seleccionan para la búsqueda local en función de este rango. Un valor menor para el rango implica un mayor probabilidad de éxito. Inicializamos el rango de cada solucionador en función de nuestro conocimiento sobre el rendimiento promedio del solucionador en una gran cantidad de problemas de prueba, y se actualizará rs durante la búsqueda global . Si un solucionador falla η veces consecutivas, se disminuirá la frecuencia con que se llama al solucionador al degradar su rango -> rs = min( 2rs ,  r) . Del mismo modo, si un solucionador gana η veces consecutivas, mejoramos su rango usando la relación rs = max ( 1 , rs/2 ) .

Antes de cada búsqueda local, empleamos el procedimiento de aprendizaje para seleccionar un solucionador local de la siguiente manera. Si todos los solucionadores locales han fallado muy a menudo, es decir, rs = r para todos los solucionadores, entonces el solucionador con el mayor número total de gana ( Nganados) está seleccionado; de lo contrario, se utiliza un solucionador con el mejor rango para buscar

Algoritmo (Idea)
---
````python
#factor (double) se setea en el main
int T=1; iter=0
def upper_bounding(box x, loup):
    iter += 1
	x = default_finder(x) #midpoint + inHC4 + InnerTaylor
	if f(x) < loup: loup = f(x)
	if iter % T == 0:
 	    #calcular tiempo para obtener tiempo usado por IpOPt
		x = IpOpt(x) 
		if f(x) < loup: 
		`  wins +=1
	   	   succesives += 1; T/= (minimo T=1)
		   loup = f(x)
		else:
		   loses +=1
		   succesives = 0; T*=
	if max_succesives<succesives:
		max_succesives = succesives
	#con T=1: en main imprimir max_succesives y wins/(wins+loses)
````



<!--stackedit_data:
eyJoaXN0b3J5IjpbLTU0OTIyMzcxNCwtMTM4NzAzNTg4OF19
-->