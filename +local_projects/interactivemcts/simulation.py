
# ---------------------------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import state 
import subprocess
import random
from scipy.stats import truncnorm
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Se inicializa el mapa y se crea la primera casilla (nodo raiz)
StateMap = {}
StateMap[0] = state.State(0, None, 0, 0) 

def BestState(heuristic):
    bestEval = -100000000
    bestState = None
    for (key,state) in StateMap.items():
        ev = state.eval(heuristic)
        if bestEval < ev:
            bestEval = ev
            bestState = key
    return bestState

# Con la misma clave utilizada para agregar un nodo al grafo, se agrega un elemento de la clase Nodo, de modo que se cree un diccionario de referencias entre el grafo y el mapa
def CreateState(key, parent, eval):
    # La key que se ocupa para el grafo, es la misma que se ocupa para el mapa
    # Se hace una instancia de la clase Nodo (vacio)
    NewState = state.State(key, parent, 0, eval)

    
    # Se guarda el nodo inicializado en la misma posicion del grafo
    StateMap[key] = NewState

    # Como ya esta creado el nuevo nodo, se mete a la lista de "hijos visibles" del nodo
    (StateMap[parent].ChildList).append(key) 
    
    StateMap[parent].AddSimulation(eval) 
    StateMap[parent].set_selected()
              
    # Se llama a simular el nodo para inicializarlo (Ver clase Nodo)
    StateMap[key].AddSimulation(eval)


#---------------------Esta funcion escribe en un archivo la informacion de los nodos antes de ser simulados---------------------
def writeFile(selectedNodes, file_):

    #Total de nodos de todo el arbol
    length = len(StateMap)

    if length >= 1 and selectedNodes != 0:
        #Se recorre el mapa y se escribe la información del archivo
        #file_.write("Selected Node: ")
        #file_.write(";")
        for i in range(len(selectedNodes)):
            file_.write(str(selectedNodes[i])+",")
        file_.write(";\n")
        for i in range (1, length):
            node = StateMap[i]
            file_.write(str(node.id))
            file_.write(",")
            file_.write(str(node.Parent.id))
            file_.write(",")
            len_ = len(node.ChildList)
            file_.write(str(len_)) 
            file_.write(",") 
            file_.write(str(node.CurrentEv))
            file_.write("\n")
        file_.write("-")
        file_.write("\n")
           
    else:
        print("Selected node: ", selectedNodes)
        print("Length: ", length)
        print("ERROR. No hay suficientes datos")
    


def compute_parameters(parentEv, mu_parent, sigma_parent, V, id_child):
    if V<0.05: 
        v = V
    else:
        v =  random.uniform (0.05,0.1)

    sigma_child = ((V-v)/V) * sigma_parent
    if id_child==1:
        firstEv = parentEv
        mu_child = ((V-v)*mu_parent + v*firstEv)/V
    else:
        #if (random.uniform(0,100) <= np.power(0.99,(id_child-2)) * 20):
        mu_child = mu_parent + random.uniform(-0.05,0.05)*(V-v)
        #else:
        #    mu_child = mu_parent - random.uniform(0,0.05)*(V-v)
            
        if sigma_child>0:
            firstEv = truncnorm.rvs((0 - mu_child) / sigma_child, 
               (1 - mu_child) / sigma_child, loc=mu_child, scale=sigma_child, size=1)[0]
        else:
            firstEv = mu_child
    return firstEv, mu_child, sigma_child, v

# --- Fake simulations ------- #
def Simulation(ParentKey, key, NOS):

    id_child = len(StateMap[ParentKey].ChildList)+1
    parentEv = StateMap[ParentKey].fakeEv
    V = StateMap[ParentKey].V
    sigma = StateMap[ParentKey].sigma
    mu = StateMap[ParentKey].mu
    
    for i in range(0,NOS):
        #fake eval
        firstEv, mu_child, sigma_child, v = compute_parameters(parentEv, mu, sigma, V, id_child)  
        
        CreateState(key, ParentKey, firstEv)
        
        StateMap[key].mu = mu_child
        StateMap[key].sigma = sigma_child
        StateMap[key].V = V-v
        StateMap[key].fakeEv = firstEv
        id_child = id_child+1

        key=key+1

# --------------------------------------------------------- SIMULACION DE UN NODO ----------------------------------------------------
StateSimulations = 0
# Se recibe una evaluacion y un numero de acciones a partir del simulador. A partir de ello, se rellena el nodo del mapa y se agregan hijos a un nodo del grafo
def RealSimulation(ParentKey, ChildKey, NOS):

    global StateSimulations
    
    if StateSimulations == 0:
        # StateSimulations almacena una cantidad inicial minima de simulaciones que deben aparecer al apretar un nodo
        StateSimulations = NOS #NOS = number of simulations   
    
    # Se crea un arreglo que guardara el camino desde la raiz al nodo actual
    pathStack = [] 
    
    # Se crea una copia auxiliar que guarde la  informacion del nodo actual
    AuxState = StateMap[ParentKey] 
    pathStack.insert(0,len(StateMap[ParentKey].ChildList)+1)
    
    while AuxState.IdLastChild != None: 
    
        # Se mete a la pila el nuevo hijo
        pathStack.insert(0,AuxState.IdLastChild) 
        
        # Se obtiene el padre de nodo (con toda su informacion para crear el camino hacia arriba) 
        AuxState = AuxState.Parent 
        # Se vuelve a iterar siempre y cuando su IdChild no None, que es el caso del nodo raiz
   
    
    # El lector lee la cantidad de simulaciones por cada nodo y las ordena separadas por comas
    reader="" 
    
    # Se inicializa la variable   que recibira el numero que se esta leyendo de la cadena. Representa la cantidad de simulaciones que se hicieron para llegar     al nodo actual
    number=0
    
    # Se recorre pathStack para dejarlo en formato "simulaciones1, simulaciones2, ... , simulaciones3"
    for e in range(len(pathStack)):
    
        number = str(pathStack[e])
        reader+= number
        reader += ','   
   
   # Se inicializa la profundidad del nodo actual
    depth = 0 
    
    # Se calcula la profundidad del grafo segun la cantidad de simulaciones por nodos registradas en el lector anterior
    for f in range(len(reader)):
    
      # Se lee el reader, si es un numero, entonces aumenta la profundidad (entre largo el reader, m�s grande la profundidad)
        if reader[f].isnumeric():
            depth = depth+1  
     
    # Se hace una copia del lector para
    simulations = reader
      
    for i in range(StateSimulations-1):
       simulations = simulations + "\;" + reader.replace(reader[len(reader)-2], str(int(number)+i+1))
       
    print("Simulations=", simulations)
    
    # Se llama al simulador para obtener la evaluacion y numero de acciones de un caso
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    #ssh.connect("158.251.88.197", username = "tifa", password = "ScHrOdL223")
    #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("./BSG_SIMULATOR BR/BR10.txt -i 1 --min_fr=0.98 -t 10 -f BR --actions="+simulations)
    output = str(subprocess.check_output("ssh tifa@158.251.88.197 ./BSG_SIMULATOR BR/BR10.txt -i 1 --min_fr=0.98 -t 10 -f BR --actions="+simulations, shell=True))
    #output = str(subprocess.check_output("echo %PATH%" , shell=True))
    print(output)

    # Se separa el output por salto de linea 
    output = output.split('\\n')
    
    # Recorre toda la cadena del output para poder encontrar el inicio de la simulacion
    for i in range(len(output)): 
             
          # La variable position almacena la posicion del inicio de esta cadena, en caso de que no se encuentre, devuelve -1
          position = output[i].find("##start simulation") 
          
          if position != -1: 

              # Se avanza un espacio para guardar las acciones
              path = output[i+1] 
              
              # Se separa el numero de simulaciones del nodo
              path = path.split(';')
            
              # Se separa el numero de acciones del nodo
              Actions = int(path[depth-1].split('/')[1])
              
              # Se obtiene la evaluacion a traves del simulador
              # Luego se avanza dos espacios para guardar la evaluacion del nodo 
              Evaluation = float(output[i+2])
                
              # Crea un nodo para luego insertarlo en el mapa y el grafo
              NewState = CreateState(ChildKey, ParentKey, Actions, Evaluation) 
                        
              ChildKey=ChildKey+1
                            
    print("La evaluacion del nodo ", ParentKey, "es ", Evaluation)
          
    return ParentKey, StateSimulations