from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
from random import random
from typing import Tuple


class Box:

    x: Tuple[float, float]
    y: Tuple[float, float]
    z: Tuple[float, float]

    i: float
    j: float
    k: float
        
    def __init__(self, text_dimensions: str):
        text_dimensions = text_dimensions.replace("(", "")
        text_dimensions = text_dimensions.replace(")", "")
        dim = text_dimensions.strip().split(",")
        dim = [[float(dim[0]), float(dim[1]), float(dim[2])],
               [float(dim[3]), float(dim[4]), float(dim[5])]]
        
        self.init(dim)
    
    def __init__(self, dim):
        dim.shape = (2,3);
        self.init(dim)

    def init(self, dim):
        # Agregando puntos
        points = []
        points.append((dim[0][0], dim[0][1], dim[0][2]))
        points.append((dim[0][0], dim[1][1], dim[0][2]))
        points.append((dim[1][0], dim[1][1], dim[0][2]))
        points.append((dim[1][0], dim[0][1], dim[0][2]))
        points.append((dim[0][0], dim[0][1], dim[1][2]))
        points.append((dim[0][0], dim[1][1], dim[1][2]))
        points.append((dim[1][0], dim[1][1], dim[1][2]))
        points.append((dim[1][0], dim[0][1], dim[1][2]))

        self.x = []
        self.y = []
        self.z = []

        for p in points:
            self.x.append(p[0])
            self.y.append(p[1])
            self.z.append(p[2])

        self.i = [7, 0, 0, 0, 4, 4, 2, 6, 4, 0, 3, 7]
        self.j = [3, 4, 1, 2, 5, 6, 5, 5, 0, 1, 2, 2]
        self.k = [0, 7, 2, 3, 6, 7, 1, 2, 5, 5, 7, 6]

def save_container(cont_dim, box_dims, filename):
    boxes = []
    for box_dim in box_dims:
        boxes.append(Box(box_dim))

    data = []
    for box in boxes:
        tracel = go.Mesh3d(x=box.x, y=box.y, z=box.z, i=box.i,
                               j=box.j, k=box.k, opacity=1,
                               color='rgb({},{},{})'.format(random()*255,
                                                            random()*255,
                                                            random()*255))
        data.append(tracel)

    # Configurando layout del grafico
    layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0))
    fig = go.Figure(data=data, layout=layout)

    # Configurando grafico
    fig.update_layout(scene=dict(
        xaxis=dict(nticks=14, range=[0, cont_dim[0]], ),
        yaxis=dict(nticks=14, range=[0, cont_dim[1]], ),
        zaxis=dict(nticks=14, range=[0, cont_dim[2]], ),
        xaxis_showspikes=False,
        yaxis_showspikes=False,
        ),
    )

    # Renderizando grafico
    fig.write_image(filename)
    #iplot(fig, filename="holo")
    #fig.show()