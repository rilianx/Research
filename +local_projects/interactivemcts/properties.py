

# ------------------------ LIBRERÍAS -------------------------

import math as mt
import numpy as np
import simulation as sm
import state

#---------------------------------MEJOR EVALUACION DEL GRAFO---------------------------------------
    
def BestMapEv():

    bestEv = 0
    length = len(sm.StateMap)
    # Recorre todos los nodos que existen, los busca en el mapa para obtener la informacion y luego obtiene la mejor evaluacion de todo los nodos del grafo
    if length == 1:
        bestEv = sm.StateMap[0].CurrentEv
    else:
        for i in range(1, length): 
        
            if bestEv < sm.StateMap[i].BestEv:
                bestEv = sm.StateMap[i].BestEv
                
    return bestEv
    
#----------------------------------MEJOR EVALUACION DEL GRAFO---------------------------------------
    
def WorstMapEv():
    
    length = len(sm.StateMap)
    worstEv = mt.inf
    
    # Recorre todos los nodos que existen, los busca en el mapa para obtener la informacion y luego obtiene la peor evaluacion de todo los nodos del grafo
    for i in range(0, length): 
    
         if worstEv > sm.StateMap[i].WorstEv:
             worstEv = sm.StateMap[i].WorstEv
             
    return worstEv

 
#----------------------------------COLOR DEL NODO-----------------------------------------
    
def StateColor(key):

    # Se crea la lista que almacera todos los colores que deban tomar los nodos
    color_array = []

    R = 0
    G = 0
    B = 0
   
    if state.State.bestEv == sm.StateMap[key].FirstEv:
        color_array = [255,255,255]
    
   
    # Sino, se calcula el color de forma gradual segun su porcentaje en funcion de su mejor y peor evaluacion    
    else:
        Percentage = 1.0-((sm.StateMap[key].FirstEv - state.State.worstEv) / (state.State.bestEv - state.State.worstEv))
        

        R = 255-int(Percentage*255) 
        G= 255-int(Percentage*255) 
        B= 255-int(Percentage*255) 
     
        
        color_array = [R,G,B]
     
    # Se retorna un arreglo que contiene todos los colores de los nodos      
    return color_array
    

    
#-------------------------INFORMACION GENERAL DEL GRAFO Y EL NODO----------------------------------
     
def PrintInformation(ParentKey):

    # Se imprime informacion general de todo el grafo y del nodo actual (el que se esta clickeando)

    MeanEv = str(round(sm.StateMap[ParentKey].MeanEv,4))
    numSimulations = str(round(sm.StateMap[ParentKey].NumSimulations, 4))
    numActions = str(round(sm.StateMap[ParentKey].NumActions, 4))
    firstEv = str(round(sm.StateMap[ParentKey].FirstEv, 4))
    bestEvGraf = str(round(BestMapEv(), 4))
    stateNumber = str(ParentKey)
    
    information = str("INFORMACION\n"+ 
    "Mejor evaluacion del grafo: "+
    bestEvGraf+ "\n"+
    "Primera evaluacion del nodo "+ stateNumber+ ":"+
    firstEv+ "\n"+
    "Evaluacion promedio del nodo "+ stateNumber+ ":"+ 
    MeanEv+  "\n"+
    "Numero de simulaciones: "+
    numSimulations+  "\n"+
    "Numero de acciones: "+
    numActions)
    
    return information
    

    
    

                