import paramiko
import getpass
import numpy as np
import math
import funcion as F
import matplotlib.pyplot as plt
from estructura import *


print("Cargando ibex...")

home = "/home/iaraya/ibex/ibex-lib"

def connect(host):
    port = 22
    username = input("login:")
    password = getpass.getpass("pass:")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    return ssh


#llama al solver para encontrar frontera de pareto
def solve(ssh, instance, prec=1e-1):
    cmd = home+"/__build__/plugins/optim-mop/ibexmop "+ home + \
                "/plugins/optim-mop/benchs/" + instance + " --eps=" + str(prec) + \
                " --eps-contract --cy-contract-full --ub=ub1 --verbose"

    #print(cmd) 
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    flag = False; y1 = None; y2 = None
    i = 0
    
    for line in stdout.readlines():
        if "number of solutions:" in line:
            aux, n = line.strip().split(':')
            sols = int(n)
            y1 = np.zeros(sols); y2 = np.zeros(sols)
            
        if line==" solutions:\n":
            flag=True; continue
        if flag:
            #print(line.strip())
            a,b = line.strip().split()
            y1[i] = float(a); y2[i] = float(b)
            i += 1
    
    return y1, y2

#funcion que se llama al querer eliminar un punto
def elimina_punto(y1,y2,point):

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    print(y1,y2)
    fig1 = plt.figure("grafica 1")
    plt.plot(y1[point-1], y2[point-1], 'ro',y1, y2, 'g-')
    plt.show

    print("El punto a eliminar será el",y1[point-1],y2[point-1])

    point-=2
    k = 1
    lista_puntos = []
    volume = float(0.0)

    HVtotal = F.Calcula_HV(y1,y2)
    print("el hipervolumen total inicial es de",HVtotal)


    #se rellena la lista con los datos:
    #el punto anterior y siguiente al punto en donde se encuentra situado, y su hipervolumen perdido si es eliminado

    while 1:

        if k == np.size(y1)-1:
            break

        #x = y1[k-1:k+2]
        #y = y2[k-1:k+2]
        #print(x,y)

        #se obtienen las coordenadas de x e y del punto anterior
        x = y1[k-1:k]
        y = y2[k-1:k]

        #se obtienen las coordenadas de x e y del punto actual
        a = y1[k:k+1]
        b = y2[k:k+1]

        #se obtienen las coordenadas de x e y del punto siguiente
        i = y1[k+1:k+2]
        j = y2[k+1:k+2]

        xy = np.concatenate((x,y),axis = 0)#se concatenan las coordenadas del punto anterior
        ab = np.concatenate((a,b),axis = 0)#se concatenan las coordenadas del punto actual
        ij = np.concatenate((i,j),axis = 0)#se concatenan las coordenadas del punto siguiente
    
        pos = F.pos_punto(xy,ab,ij)
        
        vol = F.volParticular(y1,y2,pos,k)

        Pun = punto(ab,xy,ij,vol)
    
        lista_puntos.append(Pun)
        
        k+=1

    lista_puntos,volume = F.elim_punto(lista_puntos,point)

    HVtotal-=volume

    print("el hipervolumen final es de",HVtotal)

    a = np.array([])
    b = np.array([])

    k = 0

    while 1:
        a = np.append(a,lista_puntos[k].ptoAnterior[0])
        b = np.append(b,lista_puntos[k].ptoAnterior[1])

        if k == len(lista_puntos)-1:
            a = np.append(a,lista_puntos[k].ptoActual[0])
            a = np.append(a,lista_puntos[k].ptoSiguiente[0])

            b = np.append(b,lista_puntos[k].ptoActual[1])
            b = np.append(b,lista_puntos[k].ptoSiguiente[1])

            break

        k+=1

    return a,b

#funcion que se llama al querer eliminar una serie de puntos y volviendose a graficar, teniendo los 2 resultados:
#la grafica roja corresponde al conjunto inicial de puntos
#la grafica azul corresponde al conjunto de puntos con los puntos ya eliminados
def reduc_puntos(y1,y2,puntos):

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    #se grafica la serie inicial de puntos
    plt.plot(y1, y2, 'yo',y1, y2, 'r-')

    k = 1
    lista_puntos = []
    volume = float(0.0)

    HVtotal = F.Calcula_HV(y1,y2)
    print("el hipervolumen inicial es de",HVtotal)

    #se rellena la lista con los datos:
    #el punto anterior ,actual y siguiente al punto en donde se encuentra situado, y su hipervolumen perdido si es eliminado

    while 1:

        if k == np.size(y1)-1:
            break

        #x = y1[k-1:k+2]
        #y = y2[k-1:k+2]
        #print(x,y)

        #se obtienen las coordenadas de x e y del punto anterior
        x = y1[k-1:k]
        y = y2[k-1:k]

        #se obtienen las coordenadas de x e y del punto actual
        a = y1[k:k+1]
        b = y2[k:k+1]

        #se obtienen las coordenadas de x e y del punto siguiente
        i = y1[k+1:k+2]
        j = y2[k+1:k+2]

        xy = np.concatenate((x,y),axis = 0)#se concatenan las coordenadas del punto anterior
        ab = np.concatenate((a,b),axis = 0)#se concatenan las coordenadas del punto actual
        ij = np.concatenate((i,j),axis = 0)#se concatenan las coordenadas del punto siguiente
    
        pos = F.pos_punto(xy,ab,ij)

        vol = F.volParticular(y1,y2,pos,k)

        Pun = punto(ab,xy,ij,vol)
    
        lista_puntos.append(Pun)
        
        k+=1

    k = 0

    #se recorre la lista buscando los puntos que tengan el menor hipervolumen para luego eliminarlos
    while 1:

        if k == puntos:
            break

        point = F.menorVol2(lista_puntos)

        lista_puntos,volume = F.elim_punto(lista_puntos,point)
        HVtotal-=volume

        k+=1

    print("el hipervolumen final es de",HVtotal)

    a = np.array([])
    b = np.array([])

    k = 0

    #se vuelven a poner los puntos en un array para luego ser retornados
    while 1:
        a = np.append(a,lista_puntos[k].ptoAnterior[0])
        b = np.append(b,lista_puntos[k].ptoAnterior[1])

        if k == len(lista_puntos)-1:
            a = np.append(a,lista_puntos[k].ptoActual[0])
            a = np.append(a,lista_puntos[k].ptoSiguiente[0])

            b = np.append(b,lista_puntos[k].ptoActual[1])
            b = np.append(b,lista_puntos[k].ptoSiguiente[1])

            break

        k+=1

    return a,b

#funcion que se llama al querer saber cual punto es el que tiene el menor hipervolumen
def menorArea(y1,y2):

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    k = 1
    lista_puntos = []
    volume = float(0.0)

    #se rellena la lista con los datos:
    #el punto anterior y siguiente al punto en donde se encuentra situado, y su hipervolumen perdido si es eliminado

    while 1:

        if k == np.size(y1)-1:
            break

        #se obtienen las coordenadas de x e y del punto anterior
        x = y1[k-1:k]
        y = y2[k-1:k]

        #se obtienen las coordenadas de x e y del punto actual
        a = y1[k:k+1]
        b = y2[k:k+1]

        #se obtienen las coordenadas de x e y del punto siguiente
        i = y1[k+1:k+2]
        j = y2[k+1:k+2]

        xy = np.concatenate((x,y),axis = 0)#se concatenan las coordenadas del punto anterior
        ab = np.concatenate((a,b),axis = 0)#se concatenan las coordenadas del punto actual
        ij = np.concatenate((i,j),axis = 0)#se concatenan las coordenadas del punto siguiente
    
        pos = F.pos_punto(xy,ab,ij)
        
        vol = F.volParticular(y1,y2,pos,k)

        Pun = punto(ab,xy,ij,vol)
    
        lista_puntos.append(Pun)
        
        k+=1

    print("Se calcula la menor area")

    datos = F.menorVol2(lista_puntos)

#funcion que se llama al querer saber la posicion de un punto en especifico
def posicion_punto(y1,y2,punto):

    punto-=1

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    print("Con el punto anteriormente señalado se obtiene un subconjunto de puntos pertenecientes al punto anterior, el que se selecciono y el siguiente\n")

    print("Luego con los 3 puntos se calcula si el punto esta sobre o debajo el segmento formado entre los puntos de los extremos, arrojando 2 posibles casos:\n")
    print("~ El punto esta sobre el segmento")
    print("~ El punto esta por debajo del segmento\n")

    #se obtienen las coordenadas de x e y del punto anterior
    x = y1[punto-1:punto]
    y = y2[punto-1:punto]

    #se obtienen las coordenadas de x e y del punto actual
    a = y1[punto:punto+1]
    b = y2[punto:punto+1]

    #se obtienen las coordenadas de x e y del punto siguiente
    i = y1[punto+1:punto+2]
    j = y2[punto+1:punto+2]

    xy = np.concatenate((x,y),axis = 0)#se concatenan las coordenadas del punto anterior
    ab = np.concatenate((a,b),axis = 0)#se concatenan las coordenadas del punto actual
    ij = np.concatenate((i,j),axis = 0)#se concatenan las coordenadas del punto siguiente

    posicion = F.pos_punto(xy,ab,ij)

    if posicion == 1:
      print("El punto",punto+1,"se encuentra sobre el segmento")
    else:
      print("El punto",punto+1,"se encuentra debajo el segmento")

    h1 = [x,a,i]
    h2 = [y,b,j]

    return h1,h2

#funcion que se llama al querer saber cuantos puntos se eliminaran en el filtrado de puntos, el cual consiste en eliminar los puntos que se encuentren muy juntos y entorpezcan la eliminacion
def filtrado_puntos(y1,y2):

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    tamaño1 = np.size(y1)

    print(y1,y2)

    fig1 = plt.figure("grafica 1")
    plt.plot(y1, y2, 'ro',y1, y2, 'g-')
    plt.show

    y1,y2 = F.puntos_iguales(y1,y2)

    tamaño2 = np.size(y1)

    print("Se filtraron",tamaño1-tamaño2,"puntos")

    print(y1,y2)

#funcion que se llama al querer saber cual es el hipervolumen de la region dominada
def hipervolumen(y1,y2):

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    volumen = F.Calcula_HV(y1,y2)

    print("El hipervolumen de la grafica es de",volumen)


def get_instances(ssh):
    cmd = "ls "+home+"/plugins/optim-mop/benchs/*.txt  | xargs -n 1 basename"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    for line in stdout.readlines():
        print(line.strip(), end=' ')