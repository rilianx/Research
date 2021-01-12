import paramiko
import getpass
import numpy as np
import math
import funcion as F
import matplotlib.pyplot as plt

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


def reduc_puntos(y1, y2, cant_elim):

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    #se grafica la serie inicial de puntos
    plt.plot(y1, y2, 'ro',y1, y2, 'b-')

    print("Coordenadas X del conjunto: ",y1)
    print("Coordenadas y del conjunto: ",y2)

    i = 1  
    punto = 0

    Hvolumen = F.Calcula_HV(y1,y2)
    print("El hipervolumen inicial es de",Hvolumen)

    while(1):

      print("----------------------Iteracion",i,"--------------------------------------")

      punto = F.menorVol(y1,y2)

      Hvolumen-=punto[1]

      h1 = y1[punto[0]-1:punto[0]+2]
      h2 = y2[punto[0]-1:punto[0]+2]

      pos = F.pos_punto(h1,h2)

      y1,y2 = F.elim_punto(y1,y2,punto[0],pos)

      print("Coordenadas X tras la",i,"iteracion: ",y1,"\n")
      print("Coordenadas Y tras la",i,"iteracion: ",y2,"\n")

      if i >= cant_elim:
        break 
      i+=1
    print("El hipervolumen final tiene un valor de",Hvolumen)
        
    return y1, y2


def menorArea(y1,y2):

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    print("Se calcula la menor area")

    datos = F.menorVol(y1,y2)


def posicion_punto(y1,y2,punto):

    punto-=1

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    h1 = y1[punto-1:punto+2]
    h2 = y2[punto-1:punto+2]

    print("Con el punto anteriormente señalado se obtiene un subconjunto de puntos pertenecientes al punto anterior, el que se selecciono y el siguiente\n")
    print("Coordenadas X de los puntos",h1)
    print("Coordenadas Y de los puntos",h2)

    print("Luego con los 3 puntos se calcula si el punto esta sobre o debajo el segmento formado entre los puntos de los extremos, arrojando 2 posibles casos:\n")
    print("~ El punto esta sobre el segmento")
    print("~ El punto esta por debajo del segmento\n")

    posicion = F.pos_punto(h1,h2)

    if posicion == 1:
      print("El punto",punto+1,"se encuentra sobre el segmento")
    else:
      print("El punto",punto+1,"se encuentra debajo el segmento")

    return h1,h2


def elimina_punto(y1,y2,punto):

    punto-=1

    y1 = y1[2:-2]
    y2 = y2[2:-2]

    y1,y2 = F.puntos_iguales(y1,y2)

    print("El punto a eliminar será el",y1[punto],y2[punto])

    h1 = y1[punto-1:punto+2]
    h2 = y2[punto-1:punto+2]

    posicion = F.pos_punto(h1,h2)

    print("Se muestra graficamente el punto que se ira a eliminar")

    fig1 = plt.figure("grafica 1")
    plt.plot(y1[punto], y2[punto], 'ro',y1, y2, 'g-')
    plt.show

    y1,y2 = F.elim_punto(y1,y2,punto,posicion)

    print("Luego de eliminarse se vuelve a graficar la serie de puntos ")

    return y1,y2

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