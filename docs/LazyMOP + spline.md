MOP Explorer
==
> [TODO](https://docs.google.com/document/d/177XZFPXJYG7MEU--YZT8tfaSQeFfg0WoROwZz-OhjIc/edit) 
> Paper: [On continuation methods](https://drive.google.com/file/d/0B9JSHx01XN1rTWJSRGEtRU9VOFE/view)... [Resumen-Análisis](https://stackedit.io/app#providerId=googleDrive&state=%7B%22ids%22:%5B%221H4AH2GGK0xA39AnJsDP9Wk1o1R4xD614%22%5D,%22action%22:%22open%22,%22userId%22:%22102610549431282508675%22%7D)


Actualmente se tiene un solver que:

1) Encuentra puntos “eficientes” usando *SearchEfficient*
2) Trata de encontrar un nuevo punto (y1,?) entre los dos más distantes.
3) Genera una caja alrededor del punto (y1,y2), donde y2 es generado usando interpolador spline

ToDo
--
### Trabajar en paper

Los objetivos de trabajar en la redacción del paper son:
1. Por un lado, tener algo más concreto, detallado y mejor explicado. Aunque sólo se tengan resultados preliminares, es posible enviarlo a alguna conferencia o revista para obtenre feedback.
2. Trabajar en la redacción de un paper nos permitirá mejorar el entendimiento del algoritmo pudiendo vislumbrar maneras de mejorarlo u otras oportunidades.

### Pasos
- Descripción del algoritmo en formato paper. 
- Buscar algoritmos estado del arte para comparar.
- Diseñar experimentos.

Ideas:
--
* Preprocesamiento (reducción inicial de espacio de búsqueda)
* Moverse por zonas contiguas (estilo continuation methods)

**Continuation-method-based idea**
La idea es usar soluciones eficientes para explorar zonas cercanas en busca de más soluciones eficientes.

Algo como esto:
![image](https://i.ibb.co/P5h7PG4/image.png)
[ParCont](https://drive.google.com/file/d/1yEgXwBqa9__NUrrBkkkOhavjhndZPpkG/view?usp=sharing) 

Algoritmo preliminar:
1. Se genera un punto cercano a la solución eficiente
2. Se genera una cajita *proyectando* valores de x e y
3. Se busca una solución eficiente dentro de la caja

![image](https://i.ibb.co/9qKsSPv/image.png)

Otra Alternativa
---

Usara **AbsTaylor** para navegar
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTYwNzk3MDkxNF19
-->