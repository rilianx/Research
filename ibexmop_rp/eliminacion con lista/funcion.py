import numpy as np
from estructura import *

#se cacula el volumen mediante 3 coordenadas y se retorna
def volPuntos(x,y,z):

    area = abs((x[0]*(y[1]-z[1]) + y[0]*(z[1]-x[1]) + z[0]*(x[1]-y[1]))/2)
    return area

#se calcula un punto mediente 4 coordenadas y se retorna
def calcula_Punto(x,w,y,z):

    #se calcula las pendientes formado por los puntos
    m1 = (w[1]-x[1])/(w[0]-x[0])
    m2 = (z[1]-y[1])/(z[0]-y[0])

    #si la segunda pendiente es vertical entra acá
    if m2 == float('inf') or m2 == float('-inf'):
        
      k = y[0]
      b1 = w[1] - (m1*w[0])

      l = (m1*k) + b1

      a = [k,l]

      return a

    #si no es vertical sigue por aca calculando sus 
    b1 = w[1] - (m1*w[0])
    b2 = y[1] - (m2*y[0])

    #se meten en 2 arrays lo anteriormente calculado
    A = np.array([[-m1,1],[-m2,1]])
    B = np.array([b1,b2])
      
    #si su determinante es 0 entra aca, sino entra en el else y se calculan 
    if np.linalg.det(A) == 0:
      k,y,z,w = np.linalg.lstsq(A,B)
    else:
      k = np.linalg.solve(A,B)

    return k

#funcion que calcula el hipervolumen que se perdera de un punto especifico y se retorna
def volParticular(y1,y2,pos,pto):

      #si el punto queda por debajo del segmento entra aca
      if pos == -1:

        area = abs((y1[pto-1]*(y2[pto]-y2[pto+1]) + y1[pto]*(y2[pto+1]-y2[pto-1]) + y1[pto+1]*(y2[pto-1]-y2[pto]))/2)
        return area
      else:#si el punto queda por arriba entra aca

        if pto+2 == np.size(y1):#si el punto es el penultimo entra aca

          m1 = (y2[pto-1]-y2[pto-2])/(y1[pto-1]-y1[pto-2])
          m2 = (y2[pto+1]-y2[pto])/(y1[pto+1]-y1[pto])

          if m2 == float('inf') or m2 == float('-inf'):#si la recta del final es vertical entra acá
        
            x = y1[pto]
            b1 = y2[pto-1] - (m1*y1[pto-1])

            y = (m1*x) + b1

            area = abs((y1[pto-1]*(y-y2[pto]) + x*(y2[pto]-y2[pto-1]) + y1[pto]*(y2[pto-1]-y))/2)
            return area

          if m1 == 0:#si la pendiente del antepenultimo segmento es 0 entra aca 
          
            y = y2[pto-1]
            b2 = y2[pto] - (m2*y1[pto])

            x = (y-b2)/m2

            area = abs((y1[pto-1]*(y-y2[pto]) + x*(y2[pto]-y2[pto-1]) + y1[pto]*(y2[pto-1]-y))/2)
            return area

          #si no es ninguno de los 2 casos calcula normalmente la interseccion entre los 2 segmentos
          b1 = y2[pto-1] - (m1*y1[pto-1])
          b2 = y2[pto+1] - (m2*y1[pto+1])

          A = np.array([[-m1,1],[-m2,1]])
          B = np.array([b1,b2])
      
          if np.linalg.det(A) == 0:
            x,y,z,w = np.linalg.lstsq(A,B)
          else:
            x = np.linalg.solve(A,B)

          area = abs((y1[pto-1]*(x[1]-y2[pto]) + x[0]*(y2[pto]-y2[pto-1]) + y1[pto]*(y2[pto-1]-x[1]))/2)
          return area

        #se obtienen las coordenadas de x e y del punto actual
        x = y1[pto:pto+1]
        y = y2[pto:pto+1]

        #se obtienen las coordenadas de x e y del punto siguiente
        a = y1[pto+1:pto+2]
        b = y2[pto+1:pto+2]

        #se obtienen las coordenadas de x e y del punto subsiguiente
        i = y1[pto+2:pto+3]
        j = y2[pto+2:pto+3]

        xy = np.concatenate((x,y),axis = 0)#se concatenan las coordenadas del punto actual
        ab = np.concatenate((a,b),axis = 0)#se concatenan las coordenadas del punto siguiente
        ij = np.concatenate((i,j),axis = 0)#se concatenan las coordenadas del punto subsiguiente

        if pos_punto(xy,ab,ij) == -1:#si el punto siguiente queda por debajo simplemente se calcula el hipervolumen de ese y se retorna
          area = abs((y1[pto]*(y2[pto+1]-y2[pto+2]) + y1[pto+1]*(y2[pto+2]-y2[pto]) + y1[pto+2]*(y2[pto]-y2[pto+1]))/2)
          return area

        #si no se cumple lo anterior continua por aca calculando las 2 pendientes
        m1 = (y2[pto]-y2[pto-1])/(y1[pto]-y1[pto-1])
        m2 = (y2[pto+2]-y2[pto+1])/(y1[pto+2]-y1[pto+1])

        #si la segunda pendiente es vertical entra aca
        if m2 == float("inf") or m2 == float("-inf"):

          x1 = y1[pto+1]
          b1 = y2[pto] - (m1*y1[pto])

          y = (m1*x1) + b1

          area = abs((y1[pto]*(y-y2[pto+1]) + x1*(y2[pto+1]-y2[pto]) + y1[pto+1]*(y2[pto]-y))/2)
          return area

        #si la primera pendiente es horizontal entra aca
        if m1 == 0:

          y = y2[pto]
          b2 = y2[pto+1] - (m2*y1[pto+1])
        
          x1 = (y-b2)/m2
      
          area = abs((y1[pto]*(y-y2[pto+1]) + x1*(y2[pto+1]-y2[pto]) + y1[pto+1]*(y2[pto]-y))/2)
          return area

        #si no se cumplen las 2 anteriores continua por aca
        b1 = y2[pto] - (m1*y1[pto])
        b2 = y2[pto+1] - (m2*y1[pto+1])

        matrix1 = np.array([[-m1,1],[-m2,1]])
        matrix2 = np.array([b1,b2])
      
        if np.linalg.det(matrix1) == 0:
          v,y,z,w = np.linalg.lstsq(matrix1,matrix2)
        else:
          v = np.linalg.solve(matrix1,matrix2)

        area = abs((y1[pto]*(v[1]-y2[pto+1]) + v[0]*(y2[pto+1]-y2[pto]) + y1[pto+1]*(y2[pto]-v[1]))/2)
        return area

#verifica el menor volumen y a que punto pertenece, los muestra por pantalla y lo retorna
def menorVol2(list_puntos):

    area = 0
    i = 0

    for x in list_puntos:

      if i == 0:
        area = x.Hv
        punto = i

      if x.Hv< area:
        area = x.Hv
        punto = i

      i+=1

    print("El menor area es: ", area,"y corresponde al punto",punto+2,"\n")

    return punto

#funcion que calcula el hipervolumen total inicial del area dominada
def Calcula_HV(h1,h2):

    HVTotal = 0
    i = 1

    #se designa un punto que sobrepasa a los valores maximos de X e Y en la grafica
    puntoX = h1[np.size(h2)-1]+2
    puntoY = h2[0]+2

    for x in h1:

      #si los puntos a evaluar estan en la misma coordenada X se salta
      if h1[i] == h1[i-1]:
        if i == np.size(h1)-1:

          distanciaX = puntoX-h1[i]
          distanciaY = puntoY-h2[i]

          areaRectangulo = distanciaX*distanciaY
          HVTotal = HVTotal+areaRectangulo     

          break  
        i+=1
        continue

      #se saca las coordenadas para formar el triangulo
      Xtriangulo = h1[i]
      Ytriangulo = h2[i-1]

      #se saca la base y la altura del rectangulo que se forma
      distanciaX = h1[i]-h1[i-1]
      distanciaY = puntoY-h2[i-1]

      #se calcula las areas de cada uno
      areaRectangulo = distanciaX*distanciaY     
      areaTriangulo = abs((h1[i-1]*(h2[i]-Ytriangulo) + h1[i]*(Ytriangulo-h2[i-1]) + Xtriangulo*(h2[i-1]-h2[i]))/2)

      HVTotal = HVTotal+areaRectangulo+areaTriangulo

      #si se llega al par de puntos finales se entra en este if     
      if i == np.size(h1)-1:

        distanciaX = puntoX-h1[i]
        distanciaY = puntoY-h2[i]

        areaRectangulo = distanciaX*distanciaY
        HVTotal = HVTotal+areaRectangulo     

        break    

      i+=1

    return HVTotal

#funcion que calcula si el punto esta por debajo o arriba del segmento pediante 3 coordenadas
def pos_punto(x,y,z):
  
    a = 1

    m = (z[1]-x[1])/(z[0]-x[0])
    b = x[1] - (m*x[0])
    valor = (m*y[0]) + b

    #si valor es mayor, quiere decir que el punto que se evalua queda por debajo
    if valor>y[1]:
      a = -1
    else:#por el contrario, si es menor quiere decir que el punto queda por arriba
      a = 1
  
    return  a 

#funcion que elimina los puntos que tengan un valor bien similar, de manera que solo queden los puntos que tengan los valores mas diferentes posibles
def puntos_iguales(h1,h2):

    i = 0
    cont_ptosIguales = 0

    #le quita los decimales a todas las coordenadas
    for x in h1:
      h1[i] = round(h1[i], 0)
      h2[i] = round(h2[i], 0)
      i+=1

    i = 0

    while 1:
      if i == np.size(h1)-1:
        break

      #si la resta entre los 2 puntos da 0 significa q tienen el mismo valor y uno debe ser borrado
      if h1[i+1]-h1[i] == 0 and h2[i+1]-h2[i] == 0:

        h1 = np.delete(h1,i+1)
        h2 = np.delete(h2,i+1)

        i = 0
        cont_ptosIguales+=1
        
      i+=1
    
    return h1,h2

#funcion que se encarga de eliminar el punto seleccionado, actualizar los hipervolumenes de los puntos cercanos al eliminado y retorna el hipervolumen perdido y la lista de puntos actualizada
def elim_punto(list_puntos,pto):
    
    a = []
    i = 0

    x = list_puntos[pto].ptoAnterior
    y = list_puntos[pto].ptoActual
    z = list_puntos[pto].ptoSiguiente

    #se llama a funcion que calcula si el punto que se eliminara queda situado por debajo o arriba
    pos = pos_punto(x,y,z)

    if pos == -1:#si el punto esta por debajo entra aqui

      #si el punto a eliminar es el primero entra aca
      if pto == 0:
    
        list_puntos[pto+1].ptoAnterior = list_puntos[pto].ptoAnterior
        HvPerdido = list_puntos[pto].Hv

        list_puntos.pop(pto)
        #si el punto siguiente al que es eliminado queda por debajo entra aca
        if pos_punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente) == -1:

          list_puntos[pto].Hv = volPuntos(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)
          return list_puntos,HvPerdido
        else:
          #si el subsiguiente punto queda por debajo se copia el mismo hipervolumen que tiene en el anterior
          if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:

            list_puntos[pto].Hv = list_puntos[pto+1].Hv
            return list_puntos,HvPerdido

          x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

          list_puntos[pto].Hv = volPuntos(list_puntos[pto].ptoActual,x,list_puntos[pto].ptoSiguiente)
          return list_puntos,HvPerdido

      #si el punto que se eliminara va a ser el penultimo entra aca
      if pto == len(list_puntos)-1:

        list_puntos[pto-1].ptoSiguiente = list_puntos[pto].ptoSiguiente
        HvPerdido = list_puntos[pto].Hv

        list_puntos.pop(pto)

        #si el punto anterior al que es eliminado queda por debajo entra aca
        if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == -1:

          volNuevo = volPuntos(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

          list_puntos[pto-1].Hv = volNuevo

          #si el punto anterior al anterior esta por arriba entra aca actualizando su hipervolumen
          if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == 1:
            list_puntos[pto-2].Hv = volNuevo

          return list_puntos,HvPerdido

        #si el punto anterior queda por arriba sigue por aca

        #si el punto anterior al anterior queda por abajo entra aca
        if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == -1:
          list_puntos[pto-1].Hv = list_puntos[pto-2].Hv

          return list_puntos,HvPerdido
        
        #si el punto anterior al anterior queda por arriba continua por aca
        x = calcula_Punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

        volNuevo = volPuntos(list_puntos[pto-2].ptoAnterior,x,list_puntos[pto-2].ptoActual)

        list_puntos[pto-1].Hv = volNuevo
        list_puntos[pto-2].Hv = volNuevo

        return list_puntos,HvPerdido

      #si es un punto cualquiera sigue normalmente
      list_puntos[pto-1].ptoSiguiente = list_puntos[pto+1].ptoActual
      list_puntos[pto+1].ptoAnterior = list_puntos[pto-1].ptoActual
      HvPerdido = list_puntos[pto].Hv

      list_puntos.pop(pto)

      #si al eliminar el punto el siguiente queda por debajo y el anterior tambien entra aca
      if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == -1 and pos_punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente) == -1:

        vol1 = volPuntos(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)
        vol2 = volPuntos(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)

        #se actualizan los hipervolumenes a perder del punto anterior y siguiente  
        list_puntos[pto-1].Hv = vol1
        list_puntos[pto].Hv = vol2

        #si el punto que esta antes al anterior esta arriba se actualiza tambien su hipervolumen
        if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == 1:

          list_puntos[pto-2].Hv = vol1
    
        return list_puntos,HvPerdido

      #si al eliminar el punto el siguiente queda por debajo y el anterior por arriba entra aca
      if pos_punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente) == -1 and pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == 1:

        vol = volPuntos(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)

        list_puntos[pto].Hv = vol
        list_puntos[pto-1].Hv = vol

        #si el punto que esta antes al anterior se encuentra por arriba entra aca
        if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == 1:

          x = calcula_Punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

          list_puntos[pto-2].Hv = volPuntos(list_puntos[pto-1].ptoAnterior,x,list_puntos[pto-1].ptoActual)

        return list_puntos,HvPerdido

      #si el punto anterior y el siguiente al eliminado quedan situados por arriba entra aca
      if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == 1 and pos_punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente) == 1:

        x = calcula_Punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)

        list_puntos[pto-1].Hv = volPuntos(list_puntos[pto-1].ptoActual,x,list_puntos[pto-1].ptoSiguiente)

        #si el punto anterior al anterior queda por arriba entra aca
        if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == 1:

          x = calcula_Punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

          list_puntos[pto-2].Hv = volPuntos(list_puntos[pto-2].ptoActual,x,list_puntos[pto-2].ptoSiguiente)

        #si el punto siguiente al siguiente queda por abajo entra aca
        if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:

          list_puntos[pto].Hv = list_puntos[pto+1].Hv

          return list_puntos,HvPerdido

        #si el punto siguiente se encuentra por arriba siguen por aca
        x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

        list_puntos[pto].Hv = volPuntos(list_puntos[pto].ptoActual,x,list_puntos[pto].ptoSiguiente)

        return list_puntos,HvPerdido

      #si el punto anterior queda por debajo y el siguiente por arriba entra aca
      if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == -1 and pos_punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente) == 1:

        vol = volPuntos(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

        list_puntos[pto-1].Hv = vol

        #si el anterior al anterior queda por arriba entra aca
        if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == 1:
          list_puntos[pto-2].Hv = list_puntos[pto-1].Hv

        #si el punto siguiente al siguiente esta por debajo entra aca
        if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:
          list_puntos[pto].Hv = list_puntos[pto+1].Hv
        else:
          x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

          list_puntos[pto].Hv = volPuntos(list_puntos[pto].ptoActual,x,list_puntos[pto].ptoSiguiente)

        return list_puntos,HvPerdido

    else:#si el punto a eliminar esta por arriba del segmento continua por aca
      #si es el primer punto entra aca
      if pto == 0:    

        #si el siguiente punto queda por debajo entra aqui
        if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:

          list_puntos[pto].ptoSiguiente = list_puntos[pto+1].ptoSiguiente
          list_puntos[pto+2].ptoAnterior = list_puntos[pto].ptoActual
          HvPerdido = list_puntos[pto+1].Hv

          list_puntos.pop(pto+1)

          #si el punto siguiente queda por debajo entra aca
          if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:

            vol = volPuntos(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)
            
            list_puntos[pto].Hv = vol
            list_puntos[pto+1].Hv = vol
          else:#si el punto queda por abajo entra aca
            x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

            list_puntos[pto].Hv = volPuntos(list_puntos[pto].ptoActual,x,list_puntos[pto].ptoSiguiente)

            #si el punto siguiente al siguiente queda por arriba entra aca
            if pos_punto(list_puntos[pto+2].ptoAnterior,list_puntos[pto+2].ptoActual,list_puntos[pto+2].ptoSiguiente) == 1:

              x = calcula_Punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+2].ptoActual,list_puntos[pto+2].ptoSiguiente)

              list_puntos[pto+1].Hv = volPuntos(list_puntos[pto+2].ptoActual,x,list_puntos[pto+2].ptoSiguiente)
            else:#si el punto siguiente al siguiente queda por abajo entra aca copiando su hipervolumen al anterior
              list_puntos[pto+1].Hv = list_puntos[pto+2].Hv

          return list_puntos,HvPerdido

        #si el siguiente punto queda por arriba sigue aca
        x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

        list_puntos[pto].ptoActual = x
        list_puntos[pto].ptoSiguiente = list_puntos[pto+1].ptoSiguiente
        list_puntos[pto+2].ptoAnterior = x
        HvPerdido = list_puntos[pto+1].Hv

        list_puntos.pop(pto+1)

        #si el punto siguiente al nuevo queda por debajo entra aca
        if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:

          vol = volPuntos(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

          list_puntos[pto+1].Hv = vol
          list_puntos[pto].Hv = vol
        else:#si el punto siguiente al nuevo queda por arriba entra aca

          x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

          list_puntos[pto].Hv = volPuntos(list_puntos[pto].ptoActual,x,list_puntos[pto].ptoSiguiente)

          #si el siguiente punto al siguiente queda por abajo entra aca copiando su hipervolumen en el anterior
          if pos_punto(list_puntos[pto+2].ptoAnterior,list_puntos[pto+2].ptoActual,list_puntos[pto+2].ptoSiguiente) == -1:
            list_puntos[pto+1].Hv = list_puntos[pto+2].Hv
          else:#si el siguiente punto al siguiente queda por arriba entra aca
            x = calcula_Punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

            list_puntos[pto+1].Hv = volPuntos(list_puntos[pto+1].ptoActual,x,list_puntos[pto+1].ptoSiguiente)

        return list_puntos,HvPerdido

      #si es el penultimo punto entra aca
      if pto == len(list_puntos)-2:
        #si el punto siguiente esta por debajo entra aca
        if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:

          list_puntos[pto].ptoSiguiente = list_puntos[pto+1].ptoSiguiente
          HvPerdido = list_puntos[pto+1].Hv

          list_puntos.pop(pto+1)

          #si el punto anterior queda por debajo entra aca
          if pos_punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente) == -1:
            vol = volPuntos(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)

            list_puntos[pto].Hv = vol

            #si el punto anterior al anterior queda por arriba se copia su hipervolumen al que esta arriba
            if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == 1:
              list_puntos[pto-1].Hv = vol

            return list_puntos,HvPerdido

          #si el anterior queda por arriba sigue por aca
          list_puntos[pto].Hv = list_puntos[pto-1].Hv

          return list_puntos,HvPerdido

        #si el punto siguiente esta por arriba sigue por aca
        x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

        list_puntos[pto].ptoActual = x
        list_puntos[pto].ptoSiguiente = list_puntos[pto+1].ptoSiguiente
        HvPerdido = list_puntos[pto+1].Hv

        list_puntos.pop(pto+1)

        #si el punto anterior queda por abajo entra aca actualizando su hipervolumen
        if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == -1:
          vol = volPuntos(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

          list_puntos[pto-1].Hv = vol

          #si el punto anterior al anterior queda arriba entra aca
          if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == 1:
            list_puntos[pto-2].Hv = vol          
        else:#si el punto queda por arriba entra aca
          x = calcula_Punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)

          list_puntos[pto-1].Hv = volPuntos(list_puntos[pto-1].ptoAnterior,x,list_puntos[pto-1].ptoSiguiente)

        list_puntos[pto].Hv = list_puntos[pto-1].Hv

        return list_puntos,HvPerdido

      #si es el ultimo entra aca
      if pto == len(list_puntos)-1:

        #si el punto anterior al que se eliminara queda por debajo entra aca
        if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == -1:

          list_puntos[pto].ptoAnterior = list_puntos[pto-1].ptoAnterior
          list_puntos[pto-2].ptoSiguiente = list_puntos[pto].ptoActual
          HvPerdido = list_puntos[pto-1].Hv

          list_puntos.pop(pto-1)

          #al eliminar el punto si el que tenia antes queda por abajo entra aca
          if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual.list_puntos[pto-2].ptoSiguiente) == -1:

            vol = volPuntos(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual.list_puntos[pto-2].ptoSiguiente)

            list_puntos[pto-2].Hv = vol

            #si el punto que esta antes que el anterior esta por arriba entra aca
            if pos_punto(list_puntos[pto-3].ptoAnterior,list_puntos[pto-3].ptoActual.list_puntos[pto-3].ptoSiguiente) == 1:

              list_puntos[pto-3].Hv = vol

            list_puntos[pto-1].Hv = list_puntos[pto-2].Hv

            return list_puntos,HvPerdido

          #si queda por arriba el punto anterior al eliminado entra aca
          x = calcula_Punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

          vol = volPuntos(list_puntos[pto-2].ptoActual,x,list_puntos[pto-2].ptoSiguiente)
          list_puntos[pto-1].Hv = vol
          list_puntos[pto-2].Hv = vol

          #si el punto que esta antes que el anterior esta por arriba entra aca
          if pos_punto(list_puntos[pto-3].ptoAnterior,list_puntos[pto-3].ptoActual,list_puntos[pto-3].ptoSiguiente) == 1:

            x = calcula_Punto(list_puntos[pto-3].ptoAnterior,list_puntos[pto-3].ptoActual,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente)

            list_puntos[pto-3].Hv = volPuntos(list_puntos[pto-3].ptoActual,x,list_puntos[pto-3].ptoSiguiente)

          return list_puntos,HvPerdido

        #si el punto anterior al que se eliminara queda por arriba sigue por aca

        x = calcula_Punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)

        list_puntos[pto-1].ptoActual = x
        list_puntos[pto-1].ptoSiguiente = list_puntos[pto].ptoSiguiente
        HvPerdido = list_puntos[pto].Hv
        
        list_puntos.pop(pto)

        #si el punto anterior queda por debajo entra aca
        if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == -1:

          vol = volPuntos(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente)

          list_puntos[pto-2].Hv = vol

          #si el anterior al anterior queda por arriba entra aca
          if pos_punto(list_puntos[pto-3].ptoAnterior,list_puntos[pto-3].ptoActual,list_puntos[pto-3].ptoSiguiente) == 1:
            list_puntos[pto-3].Hv = vol
        else:
          x = calcula_Punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

          list_puntos[pto-2].Hv = volPuntos(list_puntos[pto-2].ptoActual,x,list_puntos[pto-2].ptoSiguiente)

        list_puntos[pto-1].Hv = list_puntos[pto-2].Hv

        return list_puntos,HvPerdido

      #si es un punto cualquiera sigue por aca

      #si el punto siguiente esta por debajo entra aca
      if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:

        list_puntos[pto].ptoSiguiente = list_puntos[pto+1].ptoSiguiente
        list_puntos[pto+2].ptoAnterior = list_puntos[pto+1].ptoAnterior
        HvPerdido = list_puntos[pto+1].Hv

        list_puntos.pop(pto+1)

        #si el punto actual queda por debajo entra aca
        if pos_punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente) == -1:
          vol = volPuntos(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)

          list_puntos[pto].Hv = vol

          #si el punto anterior al anterior queda por arriba
          if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == 1:
            list_puntos[pto-1].Hv = vol

          #si el siguiente punto es el penultimo entra aca
          if pto+1 == len(list_puntos)-1:
            list_puntos[pto+1].Hv = list_puntos[pto].Hv
            return list_puntos,HvPerdido

          #si el siguiente punto al siguiente queda por debajo entra aca
          if pos_punto(list_puntos[pto+2].ptoAnterior,list_puntos[pto+2].ptoActual,list_puntos[pto+2].ptoSiguiente) == -1:
            list_puntos[pto+1].Hv = list_puntos[pto+2].Hv
          else:
            x = calcula_Punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+2].ptoActual,list_puntos[pto+2].ptoSiguiente)

            list_puntos[pto+1].Hv = volPuntos(list_puntos[pto+1].ptoActual,x,list_puntos[pto+1].ptoSiguiente)

          return list_puntos,HvPerdido

        #si el anterior queda por arriba sigue por aca
        x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

        list_puntos[pto].Hv = volPuntos(list_puntos[pto].ptoActual,x,list_puntos[pto].ptoSiguiente)

        #si el siguiente punto al siguiente queda por debajo entra aca
        if pos_punto(list_puntos[pto+2].ptoAnterior,list_puntos[pto+2].ptoActual,list_puntos[pto+2].ptoSiguiente) == -1:
          list_puntos[pto+1].Hv = list_puntos[pto+2].Hv
        else:
          x = calcula_Punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+2].ptoActual,list_puntos[pto+2].ptoSiguiente)

          list_puntos[pto+1].Hv = volPuntos(list_puntos[pto+1].ptoActual,x,list_puntos[pto+1].ptoSiguiente)

        return list_puntos,HvPerdido

      #si el punto que se eliminara esta por arriba sigue por aca
      x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

      list_puntos[pto].ptoActual = x
      list_puntos[pto].ptoSiguiente = list_puntos[pto+1].ptoSiguiente
      list_puntos[pto+2].ptoAnterior = x
      HvPerdido = list_puntos[pto+1].Hv

      list_puntos.pop(pto+1)

      #si el punto anterior queda por abajo entra aca
      if pos_punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente) == -1:
        vol = volPuntos(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto-1].ptoSiguiente)

        list_puntos[pto-1].Hv = vol

        #si el punto anterior al anterior queda arriba entra aca
        if pos_punto(list_puntos[pto-2].ptoAnterior,list_puntos[pto-2].ptoActual,list_puntos[pto-2].ptoSiguiente) == 1:
          list_puntos[pto-2].Hv = vol      
      else:#si queda por arriba entra aca
        x = calcula_Punto(list_puntos[pto-1].ptoAnterior,list_puntos[pto-1].ptoActual,list_puntos[pto].ptoActual,list_puntos[pto].ptoSiguiente)

        list_puntos[pto-1].Hv = volPuntos(list_puntos[pto-1].ptoAnterior,x,list_puntos[pto-1].ptoSiguiente)
        
      #si el punto siguiente al siguiente queda por debajo entra aca
      if pos_punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente) == -1:
        vol = volPuntos(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

        list_puntos[pto+1].Hv = vol
        list_puntos[pto].Hv = vol
      else:#si el punto siguiente al siguiente queda arriba entra aca
        x = calcula_Punto(list_puntos[pto].ptoAnterior,list_puntos[pto].ptoActual,list_puntos[pto+1].ptoActual,list_puntos[pto+1].ptoSiguiente)

        list_puntos[pto].Hv = volPuntos(list_puntos[pto].ptoActual,x,list_puntos[pto].ptoSiguiente)

        x = calcula_Punto(list_puntos[pto+1].ptoAnterior,list_puntos[pto+1].ptoActual,list_puntos[pto+2].ptoActual,list_puntos[pto+2].ptoSiguiente)

        list_puntos[pto+1].Hv = volPuntos(list_puntos[pto+1].ptoActual,x,list_puntos[pto+1].ptoSiguiente)

      return list_puntos,HvPerdido