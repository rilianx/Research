import pygame
from nodeProp import Node
import node_manipulator
import simulation as sm
import properties as pr
from camera import Camera


file_=open("results.txt","a") 
def click_node(NOS,selectedNodes,n_manipulator):
    len_ = len(selectedNodes)
    for i in range(len_):
        parent_key = selectedNodes[i]
        child_key = n_manipulator.generate_son(parent_key)
        for i in range(1,NOS):
            n_manipulator.generate_son(parent_key)

        sm.Simulation(parent_key, child_key, NOS)
        
        for node in n_manipulator.nodes:
            newColor = pr.StateColor(node.id)
            node.color_to(newColor)

def main(NOS,heuristic):
    raiz = Node([27, 27], [200, 200, 200], 1, 0) 
    selectedNodes = []
    n_manipulator = node_manipulator.NodeManipulator(raiz)   
    pygame.init()
    screen = pygame.display.set_mode((1800, 900), pygame.SRCALPHA, 32)
    pygame.display.set_caption("Node Plotter")
    done = False
    
    while not done:
        
        for event in pygame.event.get():
         
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("CLICK")
                
                x, y = event.pos
                current_id = n_manipulator.get_node_id(x,y)
                if current_id != -1:
                    selectedNodes.append(current_id)

                #sm.writeFile(current_id, file_)
                

                if current_id == -1: #ningun nodo seleccionado (seleccion automatica)
                    current_id = sm.BestState(heuristic)
                    pos_x, pos_y = n_manipulator.nodes[current_id].pos
                    
                #click_node(NOS,current_id,n_manipulator)
                #n_manipulator.nodes[id_child].color_to(pr.StateColor(id_child))

            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        n_manipulator.camera.drag(0, 45)
                    elif event.key == pygame.K_s:
                        n_manipulator.camera.drag(0, -45)
                    elif event.key == pygame.K_d:
                        n_manipulator.camera.drag(-45, 0)
                    elif event.key == pygame.K_a:
                        n_manipulator.camera.drag(45, 0)
                    elif event.key == pygame.K_z:
                        n_manipulator.camera.anchura -= 1
                        n_manipulator.update_position()
                    elif event.key == pygame.K_x:
                        n_manipulator.camera.anchura += 1
                        n_manipulator.update_position()
                    elif event.key == pygame.K_r:
                        n_manipulator.camera.altura -= 1
                        n_manipulator.update_position()
                    elif event.key == pygame.K_f:
                        n_manipulator.camera.altura += 1
                        n_manipulator.update_position()
                    elif event.key == pygame.K_RETURN:
                        print("selected nodes: ", selectedNodes)
                        if current_id > 0:
                            sm.writeFile(selectedNodes, file_)
                        click_node(NOS,selectedNodes,n_manipulator)

                        if selectedNodes != None:
                            selectedNodes = []
                        
                    

        n_manipulator.update()
   
        screen.fill((255, 255, 255))
        n_manipulator.draw(screen)
        pygame.display.update()
        pygame.time.wait(10)
    file_.write(";\n")
    file_.close()
