## TODO

- [Multi-objective optimisation of positively homogeneous functions and
an application in radiation therapy (2014)](https://mail.google.com/mail/u/0/#search/guillermo.cabrera%40pucv.cl+filename%3Apdf+paper/FMfcgxwKjwzcDqHqgpNjHQHVftjCRWpq)
- [Image Augmentation Is All You Need: Regularizing Deep Reinforcement Learning from Pixels](https://arxiv.org/pdf/2004.13649.pdf)
- Reinforcement learning with decision trees?
- Construcción de redes neuronales a partir de reglas heurísticas
- KD-Tree: Revisar como particionan espacio en otros paper (orden alfabético?)
- Paper: Minima distribution for global optimization (2018)
- Computer-aided breast cancer diagnosis based on  **image** segmentation and  **interval analysis**
- [Training robust neural networks using  **Lipschitz bounds**](https://ieeexplore.ieee.org/abstract/document/9319198/)

### [NEAT and Neuroevolution](https://towardsdatascience.com/neat-an-awesome-approach-to-neuroevolution-3eca5cc7930f)

Recent papers have even highlighted ways to use NEAT and NEAT-like algorithms to evolved neural net structure and then use back propagation and gradient descent to optimize these networks, an area that I think is increasingly going to become relevant and important.

**Encoding**
![image](https://i.imgur.com/jZyKXdR.png)

**Mutation**
In NEAT, mutation can either mutate existing connections or can add new structure to a network.
If a new node is added, it is placed between two nodes that are already connected. The previous connection is disabled (though still present in the genome). The previous start node is linked to the new node with the weight of the old connection and the new node is linked to the previous end node with a weight of 1. This was found to help mitigate issues with new structural additions.

![image](https://i.imgur.com/zRGxXDs.png)

**Crossover**
In order to avoid non-functional networks, NEAT marks new evolutions with a historical number. Thus, when it comes time to crossover two individuals, this can be done with much less chance of creating individuals that are non-functional. Each gene can be aligned and (potentially) crossed-over. Each time a new node or new type of connection occurs, a historical marking is assigned, allowing easy alignment when it comes to breed two of our individuals.

![image](https://i.imgur.com/HIovF8O.png)

**Speciation**
Adding new connection without optimizing weight generally leads to low performances. Speciation simply splits up the population into several species based on the similarity of topology and connections by using some criteria. Individuals in a population only have to compete with other individuals within that species.

---

### [A Survey of Evolutionary Algorithms for Decision Tree Induction](https://www.researchgate.net/profile/Rodrigo-Barros-10/publication/224243034_A_Survey_of_Evolutionary_Algorithms_for_Decision-Tree_Induction/links/0fcfd5097f0908a83f000000/A-Survey-of-Evolutionary-Algorithms-for-Decision-Tree-Induction.pdf)

Evolutionary design of components can be divided into:

- Hyperplane evolution, where, at each tree node, an EA evolves a near-optimal (non-) linear combination of attributes for oblique trees;
- Pruning method evolution, where an EA is used to handle pruning over an induced decision tree; 
- Evolution of other methods, such as parameters of the impurity measure used to split nodes

**Encoding**

Axis-Parallel Decision Trees (node representation)
![image](https://i.imgur.com/8EPOuwt.png)
In[35-37] a similar approach is used. $node = \{t, label, P, L, R, id, value, size\}$, where $t$ is the node number ($t = 0$ is the root node), $label$ is the class label of a terminal node (meaningful only for terminal nodes), $P$ is a pointer for the parent node, $L$ and $R$ are pointers to the left and right children, respectively (null for terminal nodes). The decision related to the node is $feature[id] < value$.

**Oblique Decision Trees**
Bot and Langdon [33], [92] propose a GP for evolving oblique decision trees.
A function node has as its children a tuple $({w_i , x_i}, threshold, ifT rue, ifF lse)$, where $w_i$ and $x_i$ are the $i$-th weight constant and attribute pair, respectively.


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

The authors propose in the paper a decomposition method for dealing with large scale global optimization problems. The idea seems to be interesting, however i think the paper is poorly written (need english proofreading) and needs to be restructured.

Methods and concepts are not clearly introduced. For instance, LSGO problems should be introduced with more details in the introduction (are discrete/continuous, convex/nonconvex, differentiable, have constraints?); it is not clear **what decomposition methods actually do**; also is not clear what do you mean with accuracy of the decomposition. 

The paper lacks a background section which explains clearly the problem and the notation that will be used in the rest of the paper. Assume that readers are not expert in your field, thus concept should be explained patient and clearly to them. For instance, Fig. 1 is very difficult to understand, because the notation has not been explained before. Also, I am not familiarized with the concept "variables interaction structure", thus I do not understand what are you talking about in section 2.1. 

If an acronym is used in the abstract, it must be defined again the first time it is used in the body of the paper.

## [Image Augmentation Is All You Need: Regularizing Deep Reinforcement Learning from Pixels](https://arxiv.org/pdf/2004.13649.pdf)

We propose a simple **data augmentation technique** that can be applied to standard **model-free reinforcement learning algorithms**.

Existing model-free approaches, such as Soft Actor-Critic (SAC) [22], **are not able to train deep networks effectively from image pixels**. However, the addition of our augmentation method dramatically improves SAC’s performance, enabling it to reach state-of-the-art performance on the DeepMind control suite, surpassing model-based [23, 38, 24] methods and recently proposed **contrastive learning**.

Simultaneously training a convolutional encoder alongside a policy network is challenging when given **limited environment interaction**, **strong correlation between samples** and a typically sparse reward signal.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTk1MzAxNDQxMSwyMTEyNTIxNTI1LC03MT
Y5NzM0NDcsLTEwMjEzNDE0LDE5NTE3MjczODUsLTU0Mzc4NDgy
NSwtMTY4NDE3MDg0NCwtNjU2MDQ4MTkzLC0xMjAzMTUzMDAsLT
Y1MjYwNDM1MSwtMTQ0MjM3OTUyOCwtMTIxMzI2NDczMiwtMzcx
ODAwNTc1LC0xMzY2NTY4OTcxLDIwODE2MDg3MTUsLTE1NDc5Mj
U2ODIsLTE1ODg3NTMzMjUsLTE3MDA4NjQ2MSwtMTI3OTI1ODM2
NSwxMzQ4Nzg2OTIzXX0=
-->