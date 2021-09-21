## TODO

- A Generalized Reinforcement Learning Algorithm for Online 3D Bin-Packing
- [Multi-Agent Deep Reinforcement Learning in a Three-Species Predator-Prey Ecosystem](https://odr.chalmers.se/handle/20.500.12380/302922)
- [Multi-objective optimisation of positively homogeneous functions and an application in radiation therapy (2014)](https://mail.google.com/mail/u/0/#search/guillermo.cabrera%40pucv.cl+filename%3Apdf+paper/FMfcgxwKjwzcDqHqgpNjHQHVftjCRWpq)
- Interval based NN, dependence problem?
- Neural Networks frames-oriented? Finding data in frames? (example: objects, acceleration)
- Interval gradient descent?
- Semidefinite Programming
- [Rainbow (Deep reinforcement learning with double q-learning)](https://ojs.aaai.org/index.php/AAAI/article/download/10295/10154)

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

---

I think the paper has improved significantly. The introduction is more structured now.

I think that a formal definition of the problem should be given in the introduction or at the beginning of the related work. At least, objective function, variables and variable domains should be properly defined.

Some simple concepts, like Variable interaction, should be explained more clearly. It was very difficult for me to understand such a simple concept. Maybe you can start with: "We say that two variables interacts when...".
What is the idea behind differential grouping? I think it should be explained briefly in the Section 2.2 or in the Introduction.
What is the essence of your proposal? I think that a summary should be presented at the beginning of Section 3. Otherwise the paper is difficult to follow.

Try to start explanations showing a general picture of the problem or method, then focus on the details.

English was improved, but I think that proofreading is still required.



## [Image Augmentation Is All You Need: Regularizing Deep Reinforcement Learning from Pixels](https://arxiv.org/pdf/2004.13649.pdf)

We propose a simple **data augmentation technique** that can be applied to standard **model-free reinforcement learning algorithms**.

Existing model-free approaches, such as Soft Actor-Critic (SAC) [22], **are not able to train deep networks effectively from image pixels**. However, the addition of our augmentation method dramatically improves SAC’s performance, enabling it to reach state-of-the-art performance on the DeepMind control suite, surpassing model-based [23, 38, 24] methods and recently proposed **contrastive learning**.

Simultaneously training a convolutional encoder alongside a policy network is challenging when given **limited environment interaction**, **strong correlation between samples** and a typically **sparse reward signal**.

The key idea is **to use standard image transformations to peturb input observations**, as well as **regularizing the Q-function** learned by the critic so that different transformations of the same input image have similar Q-function values. No further modifications to standard actor-critic algorithms are required, obviating the need for additional losses, e.g. based on auto-encoders [60], dynamics models [24, 23], or contrastive loss terms [50].

![image](https://i.imgur.com/Mf60ZZY.png)

![image](https://i.imgur.com/fWFZXTz.png)

![image](https://i.imgur.com/eMk6UL3.png)

## [Computer-aided breast cancer diagnosis based on image segmentation and interval analysis](https://sci-hub.se/10.1080/00051144.2020.1785784)

**Image segmentation** is a technique for dividing an image into its principal components in some areas which are actually different objects in the image that are uniform in terms of texture or colour.
Image segmentation is used in cases such as image processing, machine vision, medical image processing, digital libraries, content-based information retrieval in pictures and videos, data transfer through the Internet and image compression [17–20].

A primary move before image segmentation is **quantizing and sampling the range of input image in computer memory** for discretization of the image from the spatial domain. Doing discretization has always a bad effect on the input image, i.e. missing of the information in the input image. This problem makes uncertain intensity information for the image pixels.

Several methods are performed on considering uncertainties, for example, fuzzy methods [22–26], statistical methods [27] and interval methods [28].

![image](https://i.imgur.com/DUKwMON.png)

Apply two preprocessing methods:
- **Histogram Equalization**: for increasing contrast in low contrast images
- **Median Filtering**: For removing noise
- **Image thresholding (Kapur method)**: The objective maximizing is the image entropy and describing the compactness and separability in the classes.

### Interval Edge Detection

One of the proper methods in **edge detection** is Laplacian of Gaussian (LoG). It combines the Gaussian filtering with the Laplacian. 

Laplacian, indeed, is the **image second-order derivative**. Since performing derivative into an image, enhances its high-frequency edges, the Laplacian filter is utilized to edges detection of an image. LOG applies Laplacian operator following the smoothing it on an image by Gaussian filter to reduce the noise.

![image](https://i.imgur.com/cJpVMhX.png)
*Kernel for approximating Laplacian filter*

A most important drawback of LOG is that **doesn’t work properly where the image tone (intensity level) is varying and has uncertainties**. 

Proposal: Interval extension of Laplacian to improve the performance of LOG



## [Actor-Critic](https://theaisummer.com/Actor_critics/)

The principal idea is to split the model in two: one for computing an action based on a state and another one to produce the Q values of the action.

The actor takes as input the state and outputs the **best action**. It essentially controls how the agent behaves by **learning the optimal policy**

The critic, on the other hand, **evaluates the action by computing the value function**

The **actor** can be a function approximator like a neural network and its task is to **produce the best action for a given state**. Of course, it can be a fully connected neural network or a convolutional or anything else. The **critic** is another function approximator, which receives as input **the environment and the action by the actor**, concatenates them and output the **action value** (Q-value) for the given pair. Let me remind you for a sec that the Q value is essentially the **maximum future reward**.

### A2C

Advantage function captures **how better an action is compared to the others at a given state**, while as we know the value function captures how good it is to be at this state.

**Instead of having the critic to learn the Q values, we make him learn the Advantage values**. The advantage of the advantage function (see what I did here?) is that it **reduces the high variance** of policy networks and stabilize the model.

### Asynchronous Advantage Actor-Critic

The key difference from A2C is the Asynchronous part. A3C consists of **multiple independent agents**(networks) with their own weights, who interact with a different copy of the environment in parallel. Thus, they can explore a bigger part of the state-action space in much less time.

![image](https://i.imgur.com/Fa8Jq4i.png)

The agents (or workers) are trained in parallel and update periodically a global network, which holds shared parameters. The updates are not happening simultaneously and that’s where the asynchronous comes from. After each update, the agents resets their parameters to those of the global network and continue their independent exploration and training for n steps until they update themselves again.

We see that the information flows not only from the agents to the global network but also between agents as each agent resets his weights by the global network, which has the information of all the other agents. Smart right?

### Improved A2C

There is no need to have many agents if they are synchronous, as they essentially are not different at all. In fact, what we do, is to create **multiple versions of the environment** and just two networks.

The first network (usually referred to as step model) interacts with all the environments for n time steps in parallel and outputs a batch of experiences. With those experience, we train the second network (train model) and we update the step model with the new weights. And we repeat the process.

### Trust Region and Proximal policy optimization

Remember that in **policy gradients techniques**, we try to optimize a policy objective function (the expected accumulative reward) using gradient descent. Policy gradients are great for continuous and large spaces but suffer from some problems.

-   High variance (which we address with  [Actor-critic](https://theaisummer.com/Actor_critics/)  models)
-   Delayed reward problem
-   Sample inefficiency
-   Learning rate highly affects training

Especially the last one troubled researchers for quite a long, because it is very hard to find a suitable learning rate for the whole optimization process. Small learning rate may cause vanishing gradients while large rate may cause exploding gradient. In general, we need a method to change the policy not too much but also not too little and even better to always improve our policy.

### Trust region policy optimization (TRPO) 

To ensure that the policy won’t move too far, we add a **constraint** to our **optimization problem** in terms of making sure that the updated policy lies within a trust region. Trust regions are defined as the region in which the **local approximations of the function are accurate**.

We have to use the**Conjugate Gradient method** instead of gradient descent. 

Generally speaking, trust regions are considered pretty standard methods to approach optimization problems. The tricky part is to apply them in a reinforcement learning context in a way that provides an advantage over simple policy gradients.

Although TRPO is a very powerful algorithm, it suffers from a significant problem: that bloody constraint, which adds additional overhead to our optimization problem. I mean it forces us to use the conjugate gradient method and baffled us with linear and quadratic approximations. Wouldn’t it be nice if the could somehow **include the constraint directly into our optimization objective**? As you might have guessed that is exactly what Proximal policy optimization does.

### Proximal policy optimization (PPO)

So instead of adding a constraint separately, we incorporate it inside the objective function as a penalty

![image](https://i.imgur.com/vwrbVpE.png)

The algorithm is transformed as follows:

-   We run a set of trajectories and collect the policies
-   Estimate the advantages using an advantage estimation algorithm
-   Perform stochastic gradient descent on the objective function for a certain number of epochs
-   Repeat

We update the coefficient C based on how big or small the KL divergence is. If KL is too high, we increase it, or if it is too low, we decrease it.

The authors found a way to improve this penalized version into a new, more robust objective function.

![image](https://i.imgur.com/eBQdBzO.png)

Using this ratio, we can construct a new objective function to **clip the estimated advantage if the new policy is far away from the old one**.

[Hiperparámetos PPO](https://medium.com/aureliantactics/ppo-hyperparameters-and-ranges-6fc2d29bccbe)

### Gamma

Typically, gamma is viewed as part of the  _problem_, not of the  _algorithm_. A reinforcement learning algorithm tries for each state to optimise the cumulative discounted reward:

`r1 + gamma*r2 + gamma^2*r3 + gamma^3*r4 ...`

where  `rn`  is the reward received at time step  `n`  from the current state. So, for one choice of gamma the algorithm may optimise one thing, and for another choice it will optimise something else.

However, when you have defined a certain high-level goal, there still often remains a modelling choice, as many different gamma's might satisfy the requirements of the goal. For instance, in the cart pole the goal is to balance the pole indefinitely. If you give a reward of +1 for every step that it is balanced, the same policies (the ones that always balances the pole) are optimal for all gamma > 0. However, the ranking of suboptimal policies - that determine the learning properties towards this goal - will be different for different values of gamma.

In general, most algorithms learn faster when they don't have to look too far into the future. So, it sometimes helps the performance to set gamma relatively low. A general rule of thumb might be: determine the lowest gamma  `min_gamma`  that still satisfies your high-level goal, and then set the gamma to  `gamma = (min_gamma + 1)/2`. (You don't want to use  `gamma = min_gamma`  itself, since then some suboptimal goal will be deemed virtually as good as the desired goal.) Another useful rule of thumb: for many problems a gamma of 0.9 or 0.95 is fine. However, always think about what such a gamma means for the goal you are optimising when combined with your reward function.

### Lambda

The lambda parameter determines how much you bootstrap on earlier learned value versus using the current Monte Carlo roll-out. This implies a trade-off between more bias (low lambda) and more variance (high lambda). In many cases, setting lambda equal to zero is already a fine algorithm, but setting lambda somewhat higher helps speed up things. Here, you do not have to worry about what you are optimising: the goal is unrelated to lambda and this parameter only helps to speed up learning. In other words, lambda is completely part of the  _algorithm_  and not of the  _problem_.

A general rule of thumb is to use a lambda equal to 0.9. However, it might be good just to try a few settings (e.g., 0, 0.5, 0.8, 0.9, 0.95 and 1.0) and plot the learning curves. Then, you can pick whichever seems to be learning the fastest.


## [Training robust neural networks using Lipschitz bounds](https://arxiv.org/pdf/2005.02929.pdf)

La idea del paper es hacer una red que minimice Loss y su constante Lipschitz. Es decir el menor valor L que satisface para cualquier par de inputs x,y:
![image](https://i.imgur.com/YkvStWa.png)

Llegan a esta propiedad:
![image](https://i.imgur.com/iQwHJfm.png)
Donde $l$ son las capas de la red y $W$ los peso obviamente.
Entonces hay que resolver este problemilla para encontrar un upperbound $L$.
![image](https://i.imgur.com/EAX0CEf.png)


##   [A Generalized Reinforcement Learning Algorithm for Online 3D Bin-Packing](https://arxiv.org/pdf/2007.00463.pdf)

### The problem

Unlike *offline* packing, we assume that the entire set of objects to be packed is **not known a priori**. Instead, a fixed number of upcoming objects is visible to the loading system, and they must be loaded in the order of arrival. 

Simulation results show that the RLbased method **outperforms state-of-the-art online bin packing heuristics** in terms of empirical competitive ratio and volume efficiency.

**Robot-implementability**: The loading of parcels is subject to some physical constraints. First, the gripper of the robot requires all boxes to be non-deformable cuboids. Second, the robot is capable of rotating the boxes only along the zaxis (vertical axis), in steps of 90o . This is more restrictive than the generic RT-3D-BPP with six canonical orientations and partial rotations. Third, the robot placement has an accuracy of 1 centimetre, with any partial dimensions rounded up to the next highest centimetre. Fourth, the placement of sensors dictates that only the upcoming n boxes (where n is a parameter) are known to the RL agent, in terms of physical dimensions. Finally, parcels cannot be reshuffled once placed inside the container, cannot be placed below an existing parcel, the corners of the parcel must be level, and the base must be flat (Fig. 2).

### Contributions

The claimed contributions of this paper are, 
(1) a novel heuristic (called WallE) for solving RT-3D-BPP which is shown to outperform existing bin-packing heuristics, 
(2) a Deep RL methodology (called PackMan) for **online computation of object location and orientation**, combined with
 (3) a generalised approach that allows the algorithm to work with arbitrary bin sizes, making it more suitable for real world deployment.

### Baseline heuristics from literature

**First Fit:** places boxes in the first found feasible location (defined by the robot-implementability constraints), scanning row-by-row from the top left of the container from the perspective of Fig. 3. If no feasible locations are found in the currently available containers, the orientation of the box is changed and the search is executed again. If this check also fails, a new container is opened and the box is placed there. First Fit is the fastest and simplest of the search-based algorithms as it does not have to explore the whole space to find the placement position. 

**Floor building:** attempts to pack the container layer-bylayer, from the floor up. In effect, the heuristic places boxes at the lowest (in terms of coordinate h) feasible location in the container. Rules for changing the orientation and opening new containers remain the same as for First Fit. Floor building performs very well when boxes in the incoming stream are of similar height, because the newly created surface is as smooth as the base. When the parcels are of varying heights, the solution quality deteriorates because it creates rough surfaces. The algorithm also requires searching through all possible locations and orientations before placing each parcel, leading to slow decision-making.

**Column building:** is the vertical complement of floor building, where the algorithm attempts to build towers of boxes with the highest feasible h coordinate in the container. Column building performs very well when the incoming boxes are sorted in decreasing order of their volume. Broadly, column building performs empirically as well as first fit but the overall structure which is created after packing can be unstable, especially for a robot to build.

### WallE (proposed heuristic)
WallE takes the box dimension as input and maintains the state space representation for each container. When a new box arrives, it computes a stability score S for each feasible location using the following relationship.

![image](https://i.imgur.com/tlSSt1O.png)
We use α1 = 0.75, α2 = 1, α3 = 1, α4 = 0.01, α5 =1.
Gvar, is defined as the sum of absolute values of differences in cell heights with neighbouring cells around the box, after the box is placed in the proposed location.  Second, we count the number of bordering cells that are higher than the height of the proposed location after loading. Denoted by Ghigh, this count indicates how snugly the current location packs an existing hole in the container. 
Finally, we count the number Gflush of bordering cells that would be exactly level with the top surface of the box, if placed in the proposed location. This indicates how smooth the resulting surface will be.
The structure of (1) includes characteristics of floor building (penalty on height hi,j), first fit (penalty on location i+j), as well as an emphasis on smooth surfaces (first three terms), which infuses some wall building tendencies if the resulting placement is tall but smooth on top.

### Deep Reinforcement Learning - PackMan

The obvious approach using reinforcement learning for this problem is to train a policy-based method that computes the optimal location and orientation for the next box, given the current state of the container and (optionally) information about other upcoming boxes.


### References
*A reinforcement learning framework for container selection and ship load sequencing in ports*. Verma, et al. (2019)





<!--stackedit_data:
eyJoaXN0b3J5IjpbMTg1Mjg2ODEzNywxNDA2NDUxMDQ5LC0xOT
g5MjQ3ODg2LDEzMDA2NDE4MDAsLTIwODczMTQxNDksLTUxMTY5
MDg3NywtMTQwNzU2NTcxMSwxNzM3NTEwNDE4LDEyNDk5NzA5Nz
csODQ3Nzg2NDk5LDEwOTE2MTQ1ODgsLTc0MTQwODEyNiwxNDg5
MjcyMjM5LDIxMDY1Nzc0MjgsLTEwNjI3MTYzODgsMTk3OTYxMz
kxMywtMTYzNjI3ODg5MCwtMTk0NTM3NTI0NiwxNzczMzI5MDMw
LC03MDY3NDY3NzhdfQ==
-->