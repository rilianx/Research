import random as r
import simulation as sm
import state
import numpy as np
import scipy.stats as stats
import simulation as sm

CollectedData = []
Position = {}
class Data:   
    #-------------------------------CONSTRUCTOR-------------------------------
    def __init__(self, bestEv_, worstEv_, level2selected_, level2nodes_): 
        self.selectedNodes = []
        self.candidates = []  #Lista de candidatos en una determinada instancia
        self.bestEv= bestEv_
        self.worstEv = worstEv_
        self.level2selected = level2selected_ #Numero de nodos seleccionados por nivel
        self.level2nodes= level2nodes_ #Numero de nodos por nivel        
    #-------------------------------------------------------------

def loadData(samples_file="results.txt"):
    sm.StateMap = {}
    sm.StateMap[0] = state.State(0, None, 0, 0) 
    CollectedData = []
    selectedNodes = []

    file_=open(samples_file,"r") 
    linea = file_.readlines()
   
    j= 0
    for i in range (0, len(linea)):
        
        candidates = []
        #print("for")
        if not linea: 
            break
        else:
        
            while j < len(linea):
               
                #print("while")
                #print("j: ", j)
                data = linea[j].rstrip().split(',')
                
                semicolon_pos = len(data) - 1
                #Si es la lista de nodos seleccionados
                if data[semicolon_pos] == ";":
                    #print("semicolon")
                    x = 0
                    while x < len(data):
                        if data[x] != ";":
                            node = str(data[x])
                            #print(node)
                            #print(data[semicolon_pos])
                            selectedNodes.append(node)
                        x = x + 1

                    
                if len(data) == 4:
                    if data[3] != ";":
                        id = 0
                        parent = 0
                        actions = 0
                        currentEvaluation = 0
                        id = int(data[0])
                        parent = int(data[1])
                        actions = int(data [2])
                        currentEvaluation = float(data[3])
                        #print("Simulated node: ", id, " ", parent, " ", actions, " ", currentEvaluation)
                        sm.CreateState(id, parent, currentEvaluation)
                        newNode=sm.StateMap[id]
                        #newNode = state.State(id, parent, actions, currentEvaluation)
                        #sm.StateMap[id] = newNode
                        candidates.append(newNode)

                if data[0] == '-':
                    newData = Data(state.State.bestEv, state.State.worstEv, state.State.level2selected, state.State.level2nodes)
                    newData.candidates = candidates
                    #print("Mean: ", candidates[0].MeanEv)
                    newData.selectedNodes = selectedNodes

                    #print("Selected nodes: ", newData.selectedNodes)
                    #print("Candidate nodes: ", len(newData.candidates))  
                    CollectedData.append(newData)
                    sm.StateMap.clear()
                    sm.StateMap = {}
                    sm.StateMap[0] = state.State(0, None, 0, 0) 
                    state.State.bestEv = 0
                    state.State.worstEv = 0
                    state.State.level2selected = {}
                    state.State.level2nodes = {}
                    selectedNodes = []
                    candidates = []
                    #print("---Next---")
                j = j+1
 

    file_.close()
    return CollectedData
 
## HEURISTICS

def best_first(tree_data, node, v): #best_first
    if len(node.ChildList) >= node.actions: 
        node.heuristic_ev = -20000

    node.heuristic_ev =  v[0]*node.FirstEv + v[1]*np.log(node.Level)
    return node.heuristic_ev

def beam_search(tree_data, node, v): #beam search
    if node.Level > 20 or len(node.ChildList) >= node.actions:  node.heuristic_ev = -20000
    if node.Level+1 not in tree_data.level2nodes: sat = 0.0     
    else: 
        max_level_nodes=max(tree_data.level2nodes.values())
        sat = tree_data.level2nodes[node.Level+1]/max_level_nodes
    node.heuristic_ev = v[0]*sat + v[1]*np.log(node.Level+1) + v[2]*node.FirstEv + v[3]*np.log(len(node.ChildList)+1)
    return  node.heuristic_ev


#Actualiza el promedios de los ranbkings por cada simulacion hecha
def rankingMean(currentRanking):
    sum_ = 0
    #Se incrementa una simulacion evaluada
    Data.totalSimulations = Data.totalSimulations + 1
    #Se recalcula el ranking promedio
    sum_ = sum_ + currentRanking
    Data.totalRankingMean = sum_ / Data.totalSimulations



def eval_heuristic_vector(vv, data):
    ret = []
    for v in vv:
        ret.append(eval_heuristic(v, data))
    return np.array(ret)

def eval_heuristic(v, data):
    quality = 0
    sum_ = 0
    rankingValue = 0
    iterations = 0
    #print("samples:", len(data))
    #se recorren todas las simulaciones hechas
    for i in range (0, len(data)):
        tree = data[i]
        candidates = tree.candidates
        selectedNodes = tree.selectedNodes

        for j in range(0, len(candidates)):
            paramaterized_heuristic(tree, candidates[j], v) #evaluar nodos usando heurística con el vector de parámetros "v"

        candidates.sort(key=lambda x: x.heuristic_ev, reverse=True)

        #La lista contiene nodos que tienen un mismo nodo seleccionado
        rankingValue, n = ranking(selectedNodes, candidates)#calcular ranking
        sum_ = rankingValue + sum_
        
        iterations = n + iterations

   
    quality = 1.0-sum_ / iterations

    
    return quality



def position(candidates):
    
    #Largo de la lista de candidatos
    length = len(candidates)
    
    for i in range(length):
        #Se recorre la lista para asignar la ultima posición registrada del nodo en los nodos candidatos
        node = candidates [i]
        Position[node.id] = i


def ranking(selectedNodes, candidates):
    #Se le asigna una posición a cada nodo de la lista (en orden decreciente, según su evaluación)
    position(candidates)
    totalSum = 0
    n = 0
    #Imprimir contenido del mapa
    #print("POSITION: ",Position)

    #print("Selected nodes: ",selectedNodes)
    #print("Len candidates list: ", len(candidates))
    for i in range(len(selectedNodes)):
        sum = 0
        result = 0
        selectedNode = int(selectedNodes[i])

        result = max(Position[selectedNode]-len(selectedNodes),0)/len(candidates)
        #print(selectedNode,":",result)
        sum = sum + result
        n = n + 1
        totalSum = totalSum + sum

    return totalSum, n 


import pyswarms as ps

##evaluacion usando modelo rf
def paramaterized_heuristic_model(s, n, rf):
    if n.Level+1 not in s.level2nodes: sat = 0.0     
    else: 
        max_level_nodes=max(s.level2nodes.values())
        sat = s.level2nodes[n.Level+1]/float(max_level_nodes)

    x = np.array([n.FirstEv,n.MeanEv,n.BestEv,n.StdDev,sat,len(n.ChildList),n.Level])
    return rf.predict([x])[0]

def f(v):
    return -eval_heuristic_vector(v, global_data)




import random
import pickle
from sklearn.metrics import r2_score

def compute_R2(model, X_test, y_test):
    # Use the forest's predict method on the test data
    y_pred = model.predict(X_test)
    return r2_score(y_test,y_pred)


def generate_predictor_model(data, model_file="model_output.sav"):

    sample = random.choices( data, k=200 )
    X = []
    y = []
    for s in sample:
        if random.random()>0.5:
            id = int(random.sample(s.selectedNodes,1)[0])-1
            n = s.candidates[id]
            y.append(1.0)
        else:
            id=s.selectedNodes[0]
            while id in s.selectedNodes:
                n = random.sample(s.candidates,1)[0]
                id = n.id
            y.append(0.0)

        if n.Level+1 not in s.level2nodes: sat = 0.0     
        else: 
            max_level_nodes=max(s.level2nodes.values())
            sat = s.level2nodes[n.Level+1]/float(max_level_nodes)

        x = np.array([n.FirstEv,n.MeanEv,n.BestEv,n.StdDev,sat,len(n.ChildList),n.Level])
        X.append(x)
        
    X=np.array(X)
    #print(X.shape)

    # Using Skicit-learn to split data into training and testing sets
    from sklearn.model_selection import train_test_split
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)

    # The baseline predictions are the historical averages
    baseline_preds = np.mean(y_test)
    # Baseline errors, and display average baseline error
    baseline_errors = abs(baseline_preds - y_test)
    #print('Average baseline error: ', np.mean(baseline_errors))

    # Import the model we are using
    from sklearn.ensemble import RandomForestRegressor
    # Instantiate model with 1000 decision trees
    rf = RandomForestRegressor(n_estimators = 1000, random_state = 42, max_depth = 5)
    # Train the model on training data
    rf.fit(X_train, y_train);
    rf_r2= compute_R2(rf,X_train,y_train)
    #print("R2(rf):", rf_r2)

    from sklearn.neural_network import MLPClassifier
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,  hidden_layer_sizes=(5, 5), random_state=1, max_iter=1000)
    clf.fit(X, y)
    # Print out the mean absolute error (mae)
    clf_r2 =  compute_R2(clf,X_train,y_train)
    #print("R2(clf):", clf_r2)

    if rf_r2 > clf_r2 : 
        pickle.dump(rf, open(model_file, 'wb'))
        return rf_r2 
    else: 
        pickle.dump(clf, open(model_file, 'wb'))
        return clf_r2

paramaterized_heuristic = None 
def adjust_parameterized_heuristic(heur, dim):
    global paramaterized_heuristic
    # Set-up de parameterized heuristic
    paramaterized_heuristic = heur
    dim=4 #size of the vector

    # Set-up hyperparameters of PSO
    options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
    #dimensions -> cantidad de dimensiones del vector v
    optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=dim, options=options)
    return optimizer.optimize(f, iters=100, verbose=False)


global_data = None
def training(samples_file, model_file, heur1_file, heur2_file):
    global global_data
    global_data = loadData(samples_file)

    r2s = []
    for i in range(1,11):
        r2=generate_predictor_model(global_data, model_file+str(i))
        r2s.append(r2)
    print("average_r2:",np.mean(r2s))
    print("max_r2:",np.max(r2s))
    
    costs = []
    f = open(heur1_file, "w")
    for i in range(10):
        best_cost, best_pos = adjust_parameterized_heuristic(best_first, 2)
        costs.append(best_cost,)
        f.write(str(best_pos)+"\n")
    print("average_costs (bf):",-np.mean(costs))
    print("max_cost (bf):",-np.min(costs))

    costs = []
    f = open(heur2_file, "w")
    for i in range(10):
        best_cost, best_pos = adjust_parameterized_heuristic(beam_search, 4)
        costs.append(best_cost)
        f.write(str(best_pos)+"\n")
    print("average_costs (bs):",-np.mean(costs))
    print("max_cost (bs):",-np.min(costs))

#training()