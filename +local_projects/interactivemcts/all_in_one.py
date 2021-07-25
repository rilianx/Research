import sys
import argparse
import pygame
from nodeProp import Node 
import random 
import numpy
import simulation as sm
import state as st
import heuristics
import graphics as gp
import node_manipulator as nd
import nodeProp as np
import properties as pr

from cpmp import Greedy
from cpmp import Layout
import copy

layout0 = Layout.read_file("cpmp/Instancias/BF//BF32/cpmp_20_8_128_52_96_1.bay", 8)

def simulation(p_key):

    path = [] 
    
    # Se crea una copia auxiliar que guarde la  informacion del nodo actual
    aux = sm.StateMap[p_key] 
    path.insert(0,len(sm.StateMap[p_key].ChildList)+1)
    
    while aux.IdLastChild != None: 
    
        # Se mete a la pila el nuevo hijo
        path.insert(0,aux.IdLastChild) 
        
        # Se obtiene el padre de nodo (con toda su informacion para crear el camino hacia arriba) 
        aux = aux.Parent 
        # Se vuelve a iterar siempre y cuando su IdChild no None, que es el caso del nodo raiz
        
    #simulation
    layout = copy.deepcopy(layout0)
     
    eval, actions = Greedy.simulation(layout, path, min_action=1)
    #print(p_key,path)
    #print(eval, actions)
    return -eval, actions

def click_node(NOS,id,n_manipulator):
    
    for i in range(NOS):
        if len(n_manipulator.nodes[id].conected_nodes) >= sm.StateMap[id].NumActions: break 
        st.lastSelected = id

               
        eval, actions = simulation(id)
        sm.StateMap[id].NumActions=actions
        if actions==0: continue
        
        id_child = n_manipulator.generate_son(id)  
        sm.CreateState(id_child, id, -1, eval)             
        
        
    #more graphic staff
    for node in n_manipulator.nodes:
        newColor = pr.StateColor(node.id, len(n_manipulator.nodes)) 
        node.color_to(newColor)

def eval(state):
    if len(state.ChildList) >= state.NumActions: return -20000
    return 10*state.FirstEv + state.Level

def diving(state):
    if len(state.ChildList) >= state.NumActions: return -20000
    return 1000*(state.Parent!=None and state.Parent.id == st.lastSelected) + state.FirstEv

def bfs(state):
    if state.Level >20 or len(state.ChildList) >= state.NumActions: return -20000
    if state.Level+1 not in st.State.level2nodes: sat = 0.0     
    else: sat = st.State.level2nodes[state.Level+1]/st.State.max_level_nodes
    return -10000*sat - 10*state.Level + state.FirstEv + 5*numpy.sqrt(1/(len(state.ChildList)+1))
        
sm.StateMap = {}
sm.StateMap[0] = st.State(None, 0)
raiz = Node([27, 27], [200, 200, 200], 1, 0) 
n_manipulator = nd.NodeManipulator(raiz) 

pygame.init()
screen = pygame.display.set_mode((900, 500), pygame.SRCALPHA, 32)
pygame.display.set_caption("Node Plotter")

#visualización (fase recopilación de información)
done=False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            done=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            id = n_manipulator.get_node_id(x,y)

            #ningun nodo seleccionado (seleccion automatica)
            if id == -1 or len(sm.StateMap[id].ChildList) >= sm.StateMap[id].NumActions:
                best_eval=-20000
                for i in sm.StateMap:
                    ev = bfs(sm.StateMap[i])
                    if ev > best_eval: 
                        best_eval=ev; id=i
                        
            click_node(2,id,n_manipulator)
                
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: n_manipulator.camera.drag(0, 45)
                elif event.key == pygame.K_s: n_manipulator.camera.drag(0, -45)
                elif event.key == pygame.K_d: n_manipulator.camera.drag(-45, 0)
                elif event.key == pygame.K_a: n_manipulator.camera.drag(45, 0)
                elif event.key == pygame.K_z: n_manipulator.camera.anchura -= 2
                elif event.key == pygame.K_x: n_manipulator.camera.anchura += 2
                elif event.key == pygame.K_r: n_manipulator.camera.altura -= 2
                elif event.key == pygame.K_f: n_manipulator.camera.altura += 2
                
                n_manipulator.update_position()
            
    if not done:
        n_manipulator.update()

        screen.fill((33, 33, 33))
        n_manipulator.draw(screen)
        pygame.display.update()
        pygame.time.wait(10)