
Idea
==

Inspirado en:
[Iterated two-phase local search for the Set-Union Knapsack Problem](https://sci-hub.se/10.1016/j.future.2019.07.062)

Algoritmo que mantiene la "esencia" del paper.

````python
def solve()
   s = random_greedy() #construcción de solución inicial
   sb = s #mejor solución
   while time < time_limit
      s = local_search(s) # e.g., hill climbing o Simmulated Annealing para mejorar resultados
      if f(s) > f(sb): sb = s
      s = perturbation(sb) # or random_greedy()
````

````python
def local_search(s): # hill_climbing
    #moves: (item a sacar, item a colocar, mejora)
    no_improvements = 0
    while no_improvements < 50:
       m = generar movimiento aletaroio (considerandos swaps) 
       si m mejora: 
	       s = s.apply(m)
	       no_improvements = 0
	   sino: no_improvements+=1
       
````


El `random_greedy` básicamente coloca los items uno a uno en la mochila. En el paper usan un greedy determinista. Yo lo haría aleatorio (e.g, escoger uno de los mejores en vez del mejor).

![image](https://i.imgur.com/ZCPDunx.png)

Para la `local search` se podría implementar un algoritmo que vaya haciendo swaps aleatorios y vaya aceptando sólo aquellos que mejoran la función objetivo (hill climbing). En el paper proponen estos movimientos. Yo me quedaría sólo con el primero. Generalmente, el algoritmo debería detenerse luego de un número consecutivo de swap fallidos (50?)

![image](https://i.imgur.com/B5CNEqK.png)

Para la `perturbation`, en el paper sacan algunos elementos de la mochila y colocan otros aleatoriamente hasta que la capacidad lo permita. El objetivo de esto es "comenzar" a buscar de nuevo con una solución *parecida* a la mejor encontrada previamente.

Otra opción es comenzar de cero haciendo un `random_greedy`.

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTY2NDQxNzc4NSw1MzM3MTQ0ODEsNzE0NT
c4MjQzLC0yMDE0NDEwMTIyLC0xODE3MzU0NTA2LDUyMjYzNDc5
OSwzNzk5Mjc3MzEsLTUwOTcyOTIxMSwzNzI2NTE0NTIsLTkxNT
I0NzA0MywtMjA1NzE1NTExOSwtMTc3MjYwODI1NywxNTgyNTg2
MzM4LC0xNjIwMjUxNSwtNjYyMDg2NDU4LC0zNTMxNzc5OTUsMT
c5NzkwNzcyMCw4NDEzMDMyMzgsODYxMjk2MTE4LC02MDM4NDIz
NTBdfQ==
-->