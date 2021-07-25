# ------------------------ LIBRERIAS -------------------------
import math as mt
from scipy.stats import truncnorm
import heuristics as h
import simulation as sm
# ------------------------ DEFINICION DE CLASE NODO Y SUS METODOS -------------------------
# Esta clase define la informacion que se guarda en el nodo (cada nodo se guarda en el mapa StateMap)

#Parameters of the Fake Simulator
max_child = 100  # max number of children per node
mean_depth = 20 # profundidad media
init_sigma = 0.05 # std deviation of the children simulations
factor_sigma = 3 # init_sigma/factor_sigma is the std deviation of mu
init_mu = 0.8
init_V = 1.0

class State:

    id_ = 0
    bestEv = -1000.0
    worstEv = 1000.0
    level2selected = {} #Number of nodes selected by level of the tree
    level2nodes = {} #Number of nodes by level
    totalMean = 0.0 # Promedio de todas las evaluaciones
    totalSimulations = 0
    totalDev = 0.0 
    totalSquareMean = 0.0

    def __repr__(self):
        return "("+str(self.id)+","+str(self.FirstEv)+","+str(self.MeanEv)+","+str(len(self.ChildList))+")"
    
    def __init__(self, id, Parent, actions, currentEv):  # Constructor del nodo
        self.id = id # Clave o identificador del nodo. Esta es la que se asocia con StateMap
        self.SelectedNode = Parent #Nodo que se selecciono para que se creara este nodo actual
        self.FirstEv = 0 #Primera evaluacion del nodo, una vez asignada no se puede cambiar
        self.CurrentEv = currentEv # Almacena la evaluacion actual, cambia cada vez que se simula el nodo
        self.lastPosition = 0 #ultima posicion registrada del nodo en la lista ordenada
        self.heuristic_ev = 0 #evaluacion generada por la heuristica  
        self.MeanEv = currentEv
        self.SquareMeanEv = 0  # Promedio de todas las evaluaciones obtenidas
        self.actions = actions
        self.StdDev  = 0  # Desviacion estandar de todas las evaluaciones obtenidas
        self.BestEv = 0  # La mayor evaluacion obtenida
        self.WorstEv = 0 # mt.inf #Pero evaluacion de                                           nodo
        self.ChildList = []  # Esto representa una  lista dinamica, para apregar datos se utiliza el metodo append()
        self.Path = [] #Pila de nodos (desde la raiz) para llegar al nodo actual. Utiliza el metodo extend()
        self.NumSimulations = 0 # Numero de veces que el nodo ha sido simulado
        self.Selected = False # Mark if the node has been selected
        self.NumChild = len(self.ChildList)
        self.IdLastChild = None
        self.Parent = Parent
        self.StateEv = 0
        self.mu = 1
        self.sigma = 1
        self.V = 1

        self.fakeEv = truncnorm.rvs(
                (- self.mu) / self.sigma, (1 - self.mu) / self.sigma, loc=self.mu, scale=self.sigma, size=1)[0] 
        if Parent != None:
            if sm.StateMap[Parent] != None:
                self.Parent = sm.StateMap[Parent]
            
            self.IdLastChild = len(self.Parent.ChildList)+1
            
        if id==0:
            self.Level = 0 # nivel del nodo
            self.mu = init_mu
            self.sigma = init_sigma
            self.V = init_V
            self.Parent = None
            #print("V= ", self.V)
            self.fakeEv = truncnorm.rvs(
                (- self.mu) / self.sigma, (1 - self.mu) / self.sigma, loc=self.mu, scale=self.sigma, size=1)[0] 
        else:
            if self.Parent != None:
                self.V = 0.1
                self.Level = self.Parent.Level + 1  # nivel del nodo
                if self.Level in State.level2nodes:
                    State.level2nodes[self.Level] += 1
                else:
                    State.level2nodes[self.Level] = 1
                
# ------------------------ Evaluación de un estado ---------------------- #
    def eval(self, heuristic):
        return h.eval(self, heuristic)
        #return 1
# ------------------------- Mark selected ---------------------------- #
    def set_selected(self):
        if self.Selected == False:
            if self.Level in State.level2selected:
                State.level2selected[self.Level] += 1
            else:
                State.level2selected[self.Level] = 1
            self.Selected = True
# ------------------------ PROMEDIO DE LAS EVALUACIONES -------------------------

    # Calcula el promedio cada vez que se hace una simulacion con el nuevo dato (nueva evaluacion)
    def Mean(self, Evaluation):

        Data = self.MeanEv * (self.NumSimulations-1)
        Sum = Data + Evaluation
        NewMean= Sum / (self.NumSimulations)
        return NewMean

    def globalMean(self, Evaluation):
        Data = State.totalMean * (State.totalSimulations-1)
        Sum = Data + Evaluation
        totalMean= Sum / (State.totalSimulations)
        return totalMean

# ------------------------ PROMEDIO DE LAS EVALUACIONES AL CUADRADO-------------------------

    # Calcula el promedio de los cuadrados cada vez que se hace una simulacion con el nuevo dato (nueva evaluacion)
    def SquareMean(self, Evaluation):

        Data = self.SquareMeanEv * (self.NumSimulations-1)
        Sum = Data + (Evaluation**2)
        NewSquareMean = Sum / (self.NumSimulations)
        return NewSquareMean
    def globalSquareMean(self, Evaluation):

        Data = State.totalSquareMean * (State.totalSimulations-1)
        Sum = Data + (Evaluation**2)
        NewSquareMean = Sum / (State.totalSimulations)
        return NewSquareMean

# ------------------------ DESVIACION ESTANDAR DE LAS EVALUACIONES -------------------------

    # Se calcula la desviacion estandar en funcion del promedio
    def StandardDev(self, Evaluation):

        SquareMean = self.SquareMeanEv
        Mean = self.MeanEv
        Diff = SquareMean - (Mean**2)
        StdDev = float(mt.sqrt(Diff))

        return StdDev

    def globalDev(self, Evaluation):

        SquareMean = State.totalSquareMean
        Mean = State.totalMean
        Diff = SquareMean - (Mean**2)
        StdDev = float(mt.sqrt(Diff))
        return StdDev

# ------------------------  EVALUACIONES -------------------------

    # Cuando se apreta un nodo para que despliegue un hijo, se llama al simulador pata guardar las informacion que retorna en los atributos de la clase
    def AddSimulation(self, Evaluation):

        # Cuando se apreta un nodo para que despliegue un hijo, se llama al simulador pata guardar las informacion que retorna en los atributos de la clase
        # Cada vez que se llama este metodo se agrega una simulacion
        self.NumSimulations = self.NumSimulations + 1

        #Solo si no hay una primera evaluacion se asigna, sino no
        if self.FirstEv == 0:
            self.FirstEv = Evaluation

        # Se calcula la peor o mejor evaluacion
        if Evaluation > self.BestEv:
            self.BestEv = Evaluation

        if Evaluation < self.WorstEv:
            self.WorstEv = Evaluation

        ## update of global variables
        if Evaluation > State.bestEv:
            State.bestEv = Evaluation

        if Evaluation < State.worstEv:
            State.worstEv = Evaluation

        State.totalSimulations = State.totalSimulations + 1
        State.totalMean = self.globalMean(Evaluation)
        State.totalSquareMean = self.globalSquareMean(Evaluation)
        self.CurrentEv = Evaluation
        self.MeanEv = self.Mean(Evaluation)
        self.SquareMeanEv = self.SquareMean(Evaluation)
        #self.retropropagation( Evaluation)

