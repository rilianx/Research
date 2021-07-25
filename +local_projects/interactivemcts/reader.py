import node_manipulator as n_manipulator
import simulation as sm
import graphics as gp

def reader ():
    # abre un archivo de prueba txt
    archive = open('tree-example.txt', 'r')
    # define el token para seprar los datos
    token = ","
    # se crea una lista que almacena muchos estados 
    stateList = []
    # se crea una lista que almacena un estado (childKey, parentKey, Actions, evaluation)
    dataList = []
    # se crean las variables para almacenar valores 
    childKey = 0
    parentKey = 0
    Actions = 0
    Evaluation = 0

    # recorre el archivo linea a linea
    for line in archive.readlines():
        # obtiene el largo de la linea
        lineSize = len(line)-1
        # quita el ultimo caracter de la linea (\n)
        line = line[0 : lineSize]
        # se guarda la nueva linea sin "\n"
        newLine = line.split(token)
        # se agrega la linea o estado a la lista de estados
        stateList.append(newLine)

    # se obtiene el largo de la lista de estados
    lenght = len(stateList)

    # se recorre la lista de estados para imprimir cada uno de ellos

       
    
    # se cierra el archivo
    archive.close()

    return stateList


