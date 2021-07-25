from box import Box
import plotly.graph_objs as go
from random import random
from sys import argv, exit


def mostrar_man():
    print("""
Graficador de contenedores:
===========================

Para graficar una instancia se debe especificar el archivo que la contiene
utilizando el parametro -f. A continuación se muestra una lista de los
argumentos que utiliza el programa

-f [file_name]      Especifica el nombre del archivo que contiene la
                    instancia que se quiere graficar
-h --help           Muestra este dialogo de ayuda
    """)


def leer_instancia(nombre_archivo: str):
    f = open(nombre_archivo, "r")
    boxes = []
    dim_cont = []

    for line in f.readlines():
        if len(dim_cont) == 0:
            line = line.replace("(", "")
            line = line.replace(")", "")
            dim_cont = line.strip().split(",")

            continue

        box = Box(line)
        boxes.append(box)
    f.close()

    return dim_cont, boxes


def main():
    file_name = None

    # Obteniendo nombre del archivo en los p
    if '-f' in argv:
        index = argv.index('-f')
        try:
            file_name = argv[index + 1]
        except IndexError:
            exit("Error: Debe especificar el nombre del archivo a " +
                 "continuacion del argumento -f (-h para ayuda)")
    elif '-h' in argv or '-help' in argv:
        mostrar_man()
        exit()
    else:
        print("No se ha ingresado un parametro o no es valido.")
        mostrar_man()
        exit()

    # Leyendo instancia y creando data
    data = []
    dim_cont, boxes = leer_instancia(file_name)
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
        xaxis=dict(nticks=14, range=[0, dim_cont[0]], ),
        yaxis=dict(nticks=14, range=[0, dim_cont[1]], ),
        zaxis=dict(nticks=14, range=[0, dim_cont[2]], ),
        xaxis_showspikes=False,
        yaxis_showspikes=False,
        ),
    )

    # Renderizando grafico
    fig.show()


if __name__ == "__main__":
    main()
