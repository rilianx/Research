## TODO



---

### [2018 - A hybrid LP/NLP paradigm for global optimization relaxations](http://mpc.zib.de/archive/2018/3/Khajavirad-Sahinidis2018_Article_AHybridLPNLPParadigmForGlobalO.pdf)

**Autores: Aida Khajavirad · Nikolaos V. Sahinidis**

In this paper, we introduce a new relaxation paradigm for global optimization. The main components of the implementation are:

(i) an efficient **convexity detection tool** that is embedded at every node in the branch and-bound tree, 
(ii) a dynamic local solver selection strategy that can switch among various local solvers in the search tree **based on their performance,** 
(iii) a verification routine that examines the optimality of the solution returned by a local solver, and 
(iv) a hybrid relaxation constructor that alternates between polyhedral and nonlinear relaxations at every node based on their **relative quality and numerical stability.**

### Highlights

En sección 2.2 aparecen una serie de reglas para detectar *subexpresiones convexas*

**Cut generation** 

If $f_j(x)$ is a convex function (resp. concave function) that is not recognized as such by the conventional factorable scheme and $y_j^∗ < f_j(x^∗)$, then a cut of the form

![image](https://i.imgur.com/hODcDxL.png)
 
is added to the current relaxation.

**Exploiting convexity for domain reduction**

Hacen algo similar a AF2, nodos intermedios corresponden a relajaciones (no necesariamente lineales) de nodos inferiores. Cuando detectan convexidades de nodos, contractan intervalos usando convexidad.

**Convex problems**

Various cutting plane-based algorithms have been proposed for solving convex NLPs by solving a sequence of LPs [8,32]. These methods are used mostly for solving non-smooth convex problems or large-scale structured convex problems such as nonlinear network flows. For general *smooth convex problems*, however, methods based on active sets or **interior point algorithms** are often significantly faster, even though they are more prone to numerical difficulties. It is well-known that for differentiable convex problems, *every primal-dual pair that satisfies the KKT conditions is optimal*. Therefore, a practical approach to solve convex problems could first utilize local NLP solvers and, if these solvers fail due to numerical issues, then the algorithm could utilize the more stable but slower polyhedral-based techniques.

**Selección dinámica de local solvers**

If a solver fails η consecutive times, then we decrease the frequency at which the solver is called by downgrading its rank: rs = min(2rs,r¯). Similarly, if a solver wins η consecutive times, we upgrade its rank using the relation rs = max(1,rs/2). Prior to each local search, we employ the above learning procedure to select a local solver as follows. If all local solvers have failed too often, i.e., rs = ¯r for all solvers, then the solver with the largest total number of wins (Nwins) is selected; otherwise, a solver with the best rank is utilized for local search.

**Combining polyedral and NL relaxations**

Suppose that the convexity detector verifies that a sub-problem in the branch-andbound tree is convex. We select a local solver from the list of available solvers using the dynamic scheme outlined in the previous section. It is well known that even for convex problems, a good starting point can highly affect the performance of local solvers. Indeed, providing a near-optimal starting point often expedites the convergence rate of Newton-type methods significantly. We construct a crude polyhedral relaxation of the convex NLP using BARON’s polyhedral relaxation constructor and utilize its solution as the starting point for the local solver. If the solution reported by the local solver satisfies the KKT conditions, then the optimal value of the convex NLP is used as the lower bound in this node; otherwise, the local solver’s solution is discarded and BARON continues with the conventional polyhedral relaxation scheme as detailed in [47]. In addition, to avoid the extra cost of solving many NLPs for which the local solver fails to find an optimal solution, we adjust the frequency at which the NLP lower bounding scheme is used based on the performance of local solvers.


### Ideas 

**Generalización del árbol de expresión.** Algo como la aritmética afín pero mejorada.  Cada nodo se asocia a una a varias restricciones o relajaciones (en vez de una sola como lo hace la aritmética afín). Luego se pueden extraer sistemas lineales o convexos para explotar. 

Otros papers relacionados:
- [Linearization of McCormick Relaxations and Hybridization with the Auxiliary Variable Method](http://www.optimization-online.org/DB_FILE/2020/11/8122.pdf)
- [A review and comparison of solvers for convex MINLP](https://link.springer.com/content/pdf/10.1007/s11081-018-9411-8.pdf)
- [On the complexity of detecting convexity over a box](https://link.springer.com/content/pdf/10.1007/s10107-019-01396-x.pdf)

---

### [Linearization of McCormick Relaxations and Hybridization with the Auxiliary Variable Method](http://www.optimization-online.org/DB_FILE/2020/11/8122.pdf) (2021)

**Jaromił Najman · Dominik Bongartz · Alexander Mitsos**

The **difficulty** of determining a good set of linearization points for the McCormick technique lies in the fact that **no auxiliary variables are introduced** and thus, the **linearization points have to be determined in the space of original optimization variables**. The selection of points for linearization affects the tightness of the linear relaxation and consequently the lower bound obtained through the solution of the resulting linear program

We propose algorithms for the **computation of linearization points** for convex relaxations constructed via the (multivariate) McCormick theorems.




**The auxiliary variable method (AVM)**

The AVM is a general method  [33, 35, 36] for the **construction of convex and concave relaxations of factorable functions**. The AVM introduces an auxiliary variable together with a corresponding auxiliary equality constraint for every intermediate nonlinear factor of a given function. Then, the convex and concave envelopes of each factor are constructed providing a convex relaxation and a concave relaxation of the original function. To linearize the convex and concave envelopes of each factor provided by the AVM, the so-called sandwich algorithm has been developed. The resulting linear program suffers from an **increased dimensionality** and a **large number of constraints because** of the auxiliary variables and equality constraints added.

**The method of McCormick [26]**

In contrast to the AVM, the McCormick technique **does not introduce any auxiliary variables** when constructing convex and concave relaxations of a given function, thus always preserving the original dimension of the underlying function. Since the resulting McCormick relaxations may be **nonsmooth**, we use subgradient propagation [28] in order to construct valid affine under- and overestimators for the convex and concave McCormick relaxations.

>Creo que el método de McCormick construye una serie de inecuaciones sin agregar variables auxiliares, pero que podría ser exponencial. Ya que cada vez cada relajación generada para un nodo (factor) debe usarse para seguir construyendo las relajaciones de la función completa.

When propagating **all combinations with the McCormick** method, we have to compute all facets explicitly and thus, also all vertices of the underlying polytope. In contrast to the computation of vertices in the linear programming simplex algorithm, this propagation thus inevitably results in exponential computational runtime.

AVM and the McCormick (with all combinations) relaxations provide **equally tight relaxations if common factors occurring at least twice are recognized**.

In order to achieve a similar tightness without the necessity of propagating all combinations of the affine functions and avoiding the combinatorial complexity, the following possibility can be considered. We choose only a **limited number of what we think are promising linearizations in each factor** and **propagate only a small part of all possible combinations**.

> Para linearizar un factor, me imagino que se usan puntos de expansión, entonces se deben escoger un pequeño conjunto de *buenos puntos*.

**Método de Kelley (para agregar puntos de linearización)**

Agregar relajaciones iterativamente al sistema lineal L. Cada relajación usa como punto de linearización el LB del L previo.

**Otro método para encontrar estos puntos (n-simplex)**

First, we need to clarify what we denote as a promising set of linearization points. A promising set of linearization points consists of points, that are well-distributed among the n-dimensional interval domain of the optimization variables and at the same time is not too large.

We propose an approach based on the computation of all vertices of an n-simplex. An n-simplex is defined as an n-dimensional polytope which also is the convex hull of its n + 1 vertices. The idea is to compute all n + 1 vertices of an n-simplex, with all vertices lying on an n-dimensional Ball centered at 0 in [−1,1] n with radius r ∈ (0,1]. These points can then be rescaled to the original interval domains of the optimization variables and then used for the computation of subgradients and McCormick relaxations.

![image](https://i.imgur.com/ZCid3q9.png)


### Decision Focused Learning [link](https://ojs.aaai.org/index.php/AAAI/article/view/3982/3860)

**Idea:** to train a predictive model using the quality of the decisions which it induces via the optimization algorithm.

The starting point is to relax the combinatorial problem to a continuous one. Then, we analytically differentiate the optimal solution to the continuous problem as a function of the model’s predictions. This allows us to train using a continuous proxy for the discrete problem. At test time, we round the continuous solution to a discrete point.

El objetivo es que la solución óptima usando parámetros  predichos por el modelo m, maximice el valor de la función f.

![image](https://i.imgur.com/xybgXlV.png)
.
El gradiente de una muestra:
![image](https://i.imgur.com/jZm68aM.png)
The first term is just the gradient of the objective with respect to the decision variable x, and the last term is the gradient of the model’s predictions with respect to its own internal parameterization. The key is computing the middle term, which measures how the optimal decision changes with respect to the prediction $\hat{\theta}$.
For continuous problems, the optimal continuous decision x must satisfy the KKT conditions (which are sufficient for convex problems). By solving this system of linear equations, we can obtain the desired term. However, the above approach is a general framework; our main technical contribution is to instantiate it for specific classes of combinatorial problems. Specifically, we need 
(1) an appropriate continuous relaxation, along with a means of solving the continuous optimization problem and 
(2) efficient access to the terms in Equation 2 which are needed for the backward pass (i.e., gradient computation).


## [Review] An Improved Decomposition Method for Large-Scale Global Optimization: Bidirection-Detection Differential Grouping

**Differential grouping** (DG) is an efficient decomposition method, which
is used to solve large scale global optimization (LSGO) problems.




LSGO problems generally refer to optimization problems with dimension greater than or equal to 1000.


To reduce the computational cost of DG and to improve the decomposition accuracy of DG-based improved methods for certain problems, a bidirection-detection differential 
grouping (BDDG) method is proposed in this paper, which uses the bidirectional detection structure (BDS) proposed in this paper to detect the relationships between variables in two directions in a one-to-many manner. 

--> rewrite the paragraph for clarity (my attempt):
In this paper we propose a bidirection-detection differential grouping (BDDG) method to reduce the computational cost of DG and to improve the decomposition accuracy of DG-based methods. BSSG uses a bidirectional detection structure (BDS) to detect the relationships between variables in two directions in a one-to-many manner.

English proofreading is required

Avoid **acronyms** in the **abstract** unless the **acronym** is commonly understood and used multiple times in the **abstract**. If an **acronym** is used in the **abstract**, it must be spelled out (defined) in the **abstract**, and then spelled out again the first time it is used in the body of the paper.

LSGO problems are not clearly defined in the introduction. Are discrete/continuous, convex/nonconvex, differentiable, have constraints?

From introduction I do not fully understand what decomposition methods actually do. It should be explained in a more detailed way.



<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA5NzQ4MTI2OCwtMTcwMDg2NDYxLC0xMj
c5MjU4MzY1LDEzNDg3ODY5MjMsMTQyMTI4NzExLC0xMTMzNDYy
NzIxLDE4NzU4NjI2MzYsLTE5MTAzNDQ0NDMsLTI4MjM5ODg5Ny
wtMjAzODAzODkzMiwyNTUzMTQwMDUsLTc4ODcxNjY2LDE2ODI1
NTMyOTEsLTE2MTE3MTIyMDUsLTIwODQ3MTkxMDhdfQ==
-->