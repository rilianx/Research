# OPTIMIZE: en python 4 esto no es necesario. Tener este import hace que el
#  interprete sea 7 veces mas lento.
from __future__ import annotations
from typing import Tuple, List
from camera import Camera
import pygame
import math
import random


class Node:
    
    # Numero del nodo
    id: int

    # Radio de la representacion del nodo
    radius = 10

    # Posicion del nodo
    pos: List[float, float]
    depth: int  #  Profundidad del nodo en el arbol

    # Posicion objetivo
    speed: float   # Velocidad que tiene el objeto para cambiar de posicion
    pos_objetive: Tuple[float, float]
    box_init: int  # Posicion inicial de la caja del nodo
    box_end: int   # Posicion final de la caja del nodo

    # Color
    color: List[int, int, int]
    color_objetive: Tuple[int, int, int]

    # Estado de seleccion
    selected: bool

    # Nodos conectados
    conected_nodes: List[Node]
    father: Node

    # Data contenida en el nodo
    data: List
    data_string: List

    def __init__(self, pos: List[float, float], color: List[int, int, int],
                 depth: int, id_node: int, father: Node = None,
                 pos_objetive=None):
        self.pos = pos
        if pos_objetive is None:
            self.pos_objetive = (pos[0], pos[1])
        else:
            self.pos_objetive = pos_objetive
        self.color = color
        self.color_objetive = (color[0], color[1], color[2])
        self.conected_nodes = []
        self.id = id_node
        #print("id_node: ", id_node)
        self.radius = 10
        self.selected = False
        self.clicked = False
        self.data = []
        self.data_string = []
        self.depth = depth
        self.father = father
        self.speed = random.random()*0.02 + 0.08

    def __str__(self):
        return "Nodo" + str(self.id)

    def go_to(self, pos_objetive: Tuple[int, int]) -> None:
        """
        Establece una posicion destino para el nodo. Tras iterativas
        actualizaciones el nodo se posicionará en la coordenada indicada en
        pos_objetive
        :param pos_objetive:    Posicion en la que se quiere posicionar el nodo
        :return:
        """
        self.pos_objetive = pos_objetive

    def color_to(self, color_objetive: Tuple[int, int, int]) -> None:
        """
        Establece un color objetivo para el nodo. Tras iterativas
        actualizaciones el nodo cambiara de color poco a poco hasta llegar al
        color objetivo.
        :param color_objetive:  Color del nodo que tendra con el paso del tiempo
        """
        self.color_objetive = color_objetive
    
    def update(self) -> None:
        """
        Actualiza el estado del nodo. Es necesario llamar este metodo cada
        frame, ya que depende de esto para poder moverse y ejecutar las
        animaciones pertinentes
        """
        # Actualizando posicion
        self.pos[0] += (self.pos_objetive[0] - self.pos[0]) * 0.03
        self.pos[1] += (self.pos_objetive[1] - self.pos[1]) * 0.03

        self.color[0] += (self.color_objetive[0] - self.color[0]) * 0.03
        self.color[1] += (self.color_objetive[1] - self.color[1]) * 0.03
        self.color[2] += (self.color_objetive[2] - self.color[2]) * 0.03

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        """
        Dibuja el nodo en la superficie ingresada como parametro
        :param surface:  Superficie donde se va a dibujar el nodo.
        :param camera:   Camara que contiene el desplazamiento de la vista
        """
        # Dibujando lineas de conexiòn
        for son in self.conected_nodes:
            pygame.draw.line(surface, (0,0,0),
                             (self.pos[0] + camera.desp[0],
                              self.pos[1] + camera.desp[1]),
                             (son.pos[0] + camera.desp[0],
                              son.pos[1] + camera.desp[1]))

        # Dibujando nodo
        pos_x = int(self.pos[0] + camera.desp[0])
        pos_y = int(self.pos[1] + camera.desp[1])
        position = (pos_x, pos_y)
        radio = max(int(self.radius*float(min(camera.anchura, camera.altura))/35.0),1)
        pygame.draw.circle(surface, (0, 0, 0), position, int(radio *1.2))
        pygame.draw.circle(surface, self.color, position, radio)
        
        if self.selected:
            pygame.draw.circle(surface, (0, 0, 0), position, radio *2)
            pygame.draw.circle(surface, (217,179,255), position, int(radio*1.8))  # , width=2)
            
            #size = radio*2
            #pygame.draw.circle(surface, (237, 174, 192), position, size, 0)
                


    def generate_son(self, pos: List[float, float],
                     color: List[int, int, int],
                     pos_objetive: Tuple[float, float],
                     id_nodo: int) -> Node:
        """
        Genera un nuevo nodo y lo conecta con el actual (self)
        :param pos:             Posicion inicial del nuevo nodo
        :param color:           Color del nuevo nodo
        :param pos_objetive:    Posicion objetivo del nuevo nodo
        :param id_nodo:         Identificador del nodo
        :return:                Retorna el nuevo nodo
        """
        new_node = Node(pos, color, self.depth + 1, id_nodo, self, pos_objetive)
        self.conected_nodes.append(new_node)
        return new_node

    def in_body(self, px: int, py: int, camera: Camera) -> bool:
        """
        Comprueba si las coordenadas ingresadas como parametro estan dentro
        del circulo que representa al nodo
        :param px:      Posicion en el eje X
        :param py:      Posicion en el eje Y
        :param camera:  Camara que contienen el desplazamiento de la vista
        :return:        Retorna True si es que el punto esta dentro del cuerpo
                        del nodo y False en caso contrario
        """
        dx = px - self.pos[0] - camera.desp[0]
        dy = py - self.pos[1] - camera.desp[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < self.radius

    def add_data(self, new_data) -> None:
        """
        Agrega nuevo objeto a la data. Se recomienda utilizar objetos con la
        funcion __str__ definida. De esta forma se podrá visualizar la data
        al pasar el mouse por arriba del nodo
        :param new_data:    Nuevo data que se quiere agregar a la data
        """
        self.data.append(new_data)
        self.data_string.append(str(new_data))

    def get_n_sons(self):
        n = len(self.conected_nodes)
        for son in self.conected_nodes:
            n += son.get_n_sons()
        return n

    def get_n_leaves(self):
        n = 0
        if len(self.conected_nodes) == 0:
            return 1
        for son in self.conected_nodes:
            n += son.get_n_leaves()
        return n

    def update_pos(self, offset):
        xpos = 50
        xtop = 0
        for son in self.conected_nodes:
            xpos += son.update_pos(xpos)
        self.go_to((xpos, self.depth*50))
        return xpos

    def get_n_leaves_until(self, node):
        n_leaves = 0
        for n in self.conected_nodes:
            if n == node:
                return n_leaves
            n_leaves += n.get_n_leaves()

        return -1
