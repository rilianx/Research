# ------------------------ LIBRERIAS -------------------------
import state
import numpy as np
import random
import math as mt
import scipy.stats as st
#import training as t
#import simulation as sm

### Específicos para FakeEvaluation
# self.mu 
# self.sigma 
# self.V 
# self.fakeEv 
#-----------------------------FUNCIONES DE EVALUACION---------------------------------------
############# Heuristic Functions ###############

#Búsqueda en profundidad (nodo más profundo)
def DFS(self):
  
    return self.Level

#Búsqueda en achura (nodo menos profundo)
def BFS(self):

    return -self.Level

#Búsqueda en profundidad (informada)
def informed_DFS (self):

    return self.Level*100 + self.FirstEv

#Búsqueda en achura (informada)
def informed_BFS (self):

    return -self.Level*100 + self.FirstEv
#Criterio bajo la mejor primera evaluacion
def bestFirstEv(self):

    return self.FirstEv

#Criterio bajo la mejor primera evaluacion
def bestMeanEv(self):
    return self.MeanEv

#En caso de requerir usar Beam Search con un determinado W, solo basta con cambiar el parametro W
def BeamSearchW (self): 
    W=3
    return BeamSearch_CurrentEv (self, W)

def BeamSearch_CurrentEv (self, W): 
    SN=0
    if self.Level in state.State.level2selected:
        SN = state.State.level2selected[self.Level] 
        
    depth = self.Level
    b=10000; e=1
    children = len(self.ChildList)

    if self.id==0: #root node
        if children >= W*W: return -np.inf
        return -b*depth
    else:
        if children >= W: return (-b*depth + e*self.FirstEv) - (self.NumSimulations*b)


        if not self.Selected and SN>=W: return -np.inf
        return (-b*depth + e*self.FirstEv) 

#BeamSearch like evaluation
def BSearch2(self):
    
    if self.V==0.0:
        return -np.inf
    
    N1=0; SN=0; N=1
    if self.Level in state.State.level2nodes:
        N = state.State.level2nodes[self.Level] #nodos en nivel actual
    if self.Level+1 in state.State.level2nodes:
        N1 = state.State.level2nodes[self.Level+1] #nodos del siguiente nivel
    if self.Level in state.State.level2selected:
        SN = state.State.level2selected[self.Level]
        
    depth = self.Level
    children = len(self.ChildList)

    a=100000; b=10000; c=1000; d=100; e=1
    S=0
    if self.Selected: S=1
    if self.id==0: #root node
        return -a*N1/2 - b*depth
    else:
        return -a*N1 - b*depth -c*np.max(np.sqrt(N)-SN,0)*S - d*children + e*self.FirstEv


def CurrentEv_NumSimulations(self):
    return self.CurrentEv/self.NumSimulations

def mcts(self):
    
    if self.Parent != None:
        Ni = self.Parent.NumChild+2
    else:
        Ni = 2
    Np = self.NumChild+2
    UTC = self.MeanEv + random.randint(1,50) * mt.sqrt(mt.log(Np)/Ni)
    return UTC
'''def tifa(self):

    SN=0 #numero de nodos seleccionados en el nivel actual

    SN2 = 0 #numero de nodos seleccionados en el siguiente nivel

    TSN = 0 #numero de nodos totales en el nivel actual

    #se verifica que el nivel seleccionado esté en el mapa
    if self.Level in state.State.level2selected: 
        SN = state.State.level2selected[self.Level] 
    
    #se define el siguiente nivel
    nextLevel = int(self.Level) + 1 
    
    #se verifica que el nivel seleccionado esté en el mapa
    if nextLevel in state.State.level2selected: 
        SN2 = state.State.level2selected[nextLevel] 

    #se verifica que el nivel 
    if self.Level in state.State.level2nodes:
        TSN = state.State.level2nodes[self.Level]

    #la profundidad del nodo es el nivel en el que se encuentra
    depth = self.Level 

    #se definen las constantes 
    a=1000000
    b=10000
    c=1000
    d=100
    e=10 

    #se obtiene la cantidad de hijos del nodo
    children = len(self.ChildList)

    #se obtienen la cantidad de nodo/estados en todos los niveles
    totalNodes = len(sm.StateMap)
   
    #W varía segun la cantidad de nodos totales y nodos seleccionados 
    W = totalNodes - SN

    #si es el nodo raiz
    if self.id==0: 

        #si la cantidad de hijos es mayor a W^2 (es decir, la cantidad de hijos es W veces mas grande que W)
        if children > W*W: 
            #se castiga la evaluacion del nodo pero no se descarta 
            return (-a*children)-(b*SN2)-(c*max(mt.sqrt(totalNodes-TSN), 0))-d*depth

        return -(b*SN2)-(c*max(mt.sqrt(totalNodes-TSN), 0))-d*depth

    else:
        if children >= (totalNodes - TSN)*W: 
            return -(b*SN2)-(c*max(mt.sqrt(TSN/totalNodes)), 0)-d*depth+e*self.MeanEv #cambie el totalNodes-TSN por TSN/totalNodes

        if TSN >= (totalNodes - TSN)*W: 
            return -(b*SN2)-(c*max(mt.sqrt(TSN/totalNodes), 0))-d*depth+e*self.MeanEv-TSN #cambie el totalNodes-TSN por TSN/totalNodes

        #if not self.Selected and SN>=W: 
            #return (-a*children)-(b*SN2)-(c*max(1/(mt.log(totalNodes-TSN +0.0001)), 0))
        
        return (-b*depth + e*self.MeanEv) '''
def h2(self):
    TSN = 0
    minDev = 0.001
    ev = 0.0
    #datos para calcular la probabilidad 
    mean = self.MeanEv
    print("Mean= ", mean)
    dev = self.StdDev
    if dev == 0:
        dev = minDev
    print("Std Dev= ", dev)
    data = state.State.bestEv
    print("Data= ", data)
    child = len(self.ChildList)
    print("Num Child= ", child)

    #se verifica que el nivel 
    if self.Level in state.State.level2nodes:
        #numero de nodos totales en el nivel actual
        TSN = state.State.level2nodes[self.Level]
    
    #se definen las constantes para dar prioridad
    a=1000000
    b=10000
    #se obtiene la probabilidad de que el nodo sea mayor a la mejor evaluacion encontrada hasta el momento
    #multiplicar esta desv por una constante
    prob = st.norm.sf(data,mean,dev)

    #se genera la evaluacion
    #ev = a*prob 
    #probar distintos valores de "b" (despues de 1000 nodos aprox) / comparar con el BeamSearch
    ev = a*mean*prob - b*child*TSN
    #ev = a*prob - b*pow(child,TSN)

    #si el promedio es menor al promedio del árbol
    #if mean < state.State.totalMean:

        #pero su desviación estándar es más alta que la desviación promedio, entonces varía más sus evaluaciones y podría haber un buen resultado
        #solo se premia al nodo por su desviacion std. 
        #if dev >= state.State.totalDev:
            #ev = a*prob*dev - b*child*TSN*mean
        #sino, si su desviación estándar es más baja que la desviación promedio, quiere decir que ha tenido malas evaluaciones que no han variado mucho
        #se castiga al nodo por su promedio y desviación std. (le resté importancia a la probabilidad)
        #if dev < state.State.totalDev:
            #ev = prob - b*b*child*TSN*mean*dev

    #Si el prmedio es mayor al promedio del arbol
    #if mean >= state.State.totalMean:

        #pero su desviación estándar es menor a la del árbol, tiene buenas evaluaciones pero no varian mucho
        #entonces se premia al nodo por su promedio
        #if dev < state.State.totalDev:
            #ev = a*pow(mean,-1)*prob - b*child*TSN*dev

        #si la desviacion estándar y el promedio del nodo es más alto que los del árbol, entonces sus evaluaciones podrían variar mucho con resultados prometedores
        #entonces, se le premia por su promedio y desviación estándar (le quité la constante b)
        #if dev >= state.State.totalDev:
            #ev = a*pow(mean,-1)*pow(dev,-1)*prob - child*TSN

    return ev

# v es vector de parámetros: por ejemplo (A,B,C,D,E)
def paramaterized_heuristic(self, v):
    # A*pow(mean,-1)*prob - B*child*TSN*dev
    return 0
    


def hill_climbing(self):
    TSN = 0
    minDev = 0.001
    ev = 0.0
    ln = 0
    x3 = 0
    vValue = 0
    lastEv = 0
    bestEv = 0
    variable = 0
    a = 1
    b = 1
    random = 1
    rankingValue = 0
    no_improvements = 0
    #datos para calcular la probabilidad 
    mean = self.MeanEv
    
    dev = self.StdDev
    if dev == 0:
        dev = minDev
    #se normaliza la desviación estándar para valores entre 0 y 1
    dev = abs(mt.sin(dev))
    data = state.State.bestEv
    
    child = len(self.ChildList)

    #se verifica que el nivel 
    if self.Level in state.State.level2nodes:
        #numero de nodos totales en el nivel actual
        TSN = state.State.level2nodes[self.Level]
    
    #se obtiene la probabilidad de que el nodo sea mayor a la mejor evaluacion encontrada hasta el momento
    #multiplicar esta desv por una constante

    prob = st.norm.sf(data,mean,dev)
    x3 =  pow(mean,3)
    ln = mt.log(dev)
 
    '''while no_improvements<50:   
        #se obtienen valores aleatorios (dentro de un rango) que determina que variable se ajustará
         #ademas,
        variable, vValue = t.values(random)
        #se determina la calidad de la heuristica mediante el ranking
        rankingValue = t.ranking(self.id)
############################ REVISAR #########################
        if lastEv < rankingValue:
            #dependiendo la variable que haya sido seleccionada, se asignará un nuevo valor random
            if variable == 1:
                a = vValue
            if variable == 2:
                b = vValue
            #se actualiza el mejor ranking
            bestEv = lastEv
            #se resetea el contador
            no_improvements = 0
        else:
            no_improvements = no_improvements + 1'''

    ev = (x3 + prob * a) + (ln + (child*TSN*b))

    return ev
    
#---------------------------DEFINICION DEL MAPA DE HEURISTICAS--------------------------------

evalMap={}
evalMap["BFS"] = BFS
evalMap["DFS"] = DFS
evalMap["informed_DFS"] = informed_DFS 
evalMap["informed_BFS"] = informed_BFS
evalMap["bestFirstEv"] = bestFirstEv
evalMap["bestMeanEv"] = bestMeanEv
evalMap["BeamSearchW"] = BeamSearchW
evalMap["BeamSearch_CurrentEv"] = BeamSearch_CurrentEv
evalMap["BSearch2"] = BSearch2
evalMap["CurrentEv_NumSimulations"] = CurrentEv_NumSimulations
evalMap["mcts"] = mcts
#evalMap["tifa"] = tifa
evalMap["h2"] = h2
evalMap["hill_climbing"] = hill_climbing



def eval(self, heuristic):
    if self.V <=0.0:  #nodo sin hijos
        return -np.inf
    
    #Change by your prefered heuristic
    #return BeamSearch(self, 3)
    return evalMap[heuristic](self)

