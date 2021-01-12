import numpy as np

def menorVol(y1,y2):
    i = 2
    A_menor = float(0)
    punto = 1
    

    for x in y1:
      if i == np.size(y1):
        break

      while 1:
        h1 = y1[i-2:i+1]
        h2 = y2[i-2:i+1]
    
        area = abs((h1[0]*(h2[1]-h2[2]) + h1[1]*(h2[2]-h2[0]) + h1[2]*(h2[0]-h2[1]))/2)
        
        if area < A_menor or i == 2:
            A_menor = area
            punto = i-1
           
        i+=1
        break

    print("El menor area es: ", A_menor,"y corresponde al punto",punto+1,"\n")
    return punto,A_menor


def Calcula_HV(h1,h2):

    HVTotal = 0

    #se designa un punto que sobrepasa a los valores maximos de X e Y en la grafica
    puntoX = h1[np.size(h2)-1]+2
    puntoY = h2[0]+2

    for i in range(1,len(h1)):

      #si los puntos a evaluar estan en la misma coordenada X se salta
      if h1[i] == h1[i-1]:
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
      

      

    return HVTotal


def pos_punto(h1,h2):
    a = 1

    m = (h2[2]-h2[0])/(h1[2]-h1[0])
    b = h2[2] - (m*h1[2])
    valor = (m*h1[1]) + b

    if valor>h2[1]:
      a = -1
    else:
      a = 1
  
    return  a 


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

      if h1[i+1]-h1[i] == 0 and h2[i+1]-h2[i] == 0:

        h1 = np.delete(h1,i+1)
        h2 = np.delete(h2,i+1)

        i = 0
        cont_ptosIguales+=1
        
      i+=1
    
    return h1,h2


def pos_punto(h1,h2):
    a = 1

    m = (h2[2]-h2[0])/(h1[2]-h1[0])
    b = h2[2] - (m*h1[2])
    valor = (m*h1[1]) + b

    if valor>h2[1]:
      a = -1
    else:
      a = 1
  
    return  a 


def puntos_iguales(h1,h2):

    i = 0
    cont_ptosIguales = 0

    #le quita los decimales a todas las coordenadas
    #for x in h1:
    #  h1[i] = round(h1[i], 0)
    #  h2[i] = round(h2[i], 0)
    #  i+=1

    i = 0

    while 1:
      if i == np.size(h1)-1:
        break

      if h1[i+1]-h1[i] == 0 and h2[i+1]-h2[i] == 0:

        h1 = np.delete(h1,i+1)
        h2 = np.delete(h2,i+1)

        i = 0
        cont_ptosIguales+=1
        
      i+=1
    
    return h1,h2


def elim_punto(h1,h2,pto,pos):

    if pos == -1:#si esta por debajo el punto entra aqui   
    
      h1 = np.delete(h1,pto)
      h2 = np.delete(h2,pto)

      return h1,h2
    else:
      
      if pto+2 == np.size(h1):#se revisa si el punto que se eliminara es el penultimo
    
        m1 = (h2[pto-1]-h2[pto-2])/(h1[pto-1]-h1[pto-2])
        m2 = (h2[pto+1]-h2[pto])/(h1[pto+1]-h1[pto])

        if m2 == float('inf') or m2 == float('-inf'):#si la recta del final es vertical entra acá
        
          x = h1[pto]
          b1 = h2[pto-1] - (m1*h1[pto-1])

          y = (m1*x) + b1

          h1[pto-1] = x
          h2[pto-1] = y

          h1 = np.delete(h1,pto)
          h2 = np.delete(h2,pto)
 
          return h1,h2

        if m1 == 0:#si la pendiente del antepenultimo segmento es 0 entra aca 
          
          y = h2[pto-1]
          b2 = h2[pto] - (m2*h1[pto])

          x = (y-b2)/m2

          h1[pto-1] = x
          h2[pto-1] = y

          h1 = np.delete(h1,pto)
          h2 = np.delete(h2,pto)

          return h1,h2

        #si no es ninguno de los 2 casos calcula normalemnte la interseccion entre los 2 segmentos
        b1 = h2[pto-1] - (m1*h1[pto-1])
        b2 = h2[pto+1] - (m2*h1[pto+1])

        A = np.array([[-m1,1],[-m2,1]])
        B = np.array([b1,b2])
      
        if np.linalg.det(A) == 0:
          x,y,z,w = np.linalg.lstsq(A,B)
        else:
          x = np.linalg.solve(A,B)

        h1[pto-1] = x[0]
        h2[pto-1] = x[1]

        h1 = np.delete(h1,pto)
        h2 = np.delete(h2,pto)
          
        return h1,h2

      #si es un punto cualquiera de la recta sigue normalmente
            
      m1 = (h2[pto]-h2[pto-1])/(h1[pto]-h1[pto-1])
      m2 = (h2[pto+2]-h2[pto+1])/(h1[pto+2]-h1[pto+1])

      l1 = h1[pto:pto+3]
      l2 = h2[pto:pto+3]

      #se revisa si el siguiente punto esta por debajo del segmento
      posicion = pos_punto(l1,l2)

      if posicion == -1:#si es asi, elimina el punto siguiente

        h1 = np.delete(h1,pto+1)
        h2 = np.delete(h2,pto+2)

        return h1,h2

      if m2 == float('inf') or m2 == float('-inf'):#si el segundo segmento es vertical(pendiente tiende al infinito) entra aca
  
        x = h1[pto+1]
        b1 = h2[pto] - (m1*h1[pto])

        y = (m1*x) + b1

        h1[pto+1] = x
        h2[pto+1] = y

        h1 = np.delete(h1,pto)
        h2 = np.delete(h2,pto)
 
        return h1,h2
      
      if m1 == 0:#si el segundo segmento es horizontal(pendiente igual a 0) entra aca
          y = h2[pto-1]
          b2 = h2[pto+1] - (m2*h1[pto+1])

          x = (y-b2)/m2

          h1[pto+1] = x
          h2[pto+1] = y

          h1 = np.delete(h1,pto)
          h2 = np.delete(h2,pto)

          return h1,h2
      
      #si no es ninguno de los casos anteriores calcula normamente la interseccion entre los 2 segmentos      
      b1 = h2[pto] - (m1*h1[pto])
      b2 = h2[pto+1] - (m2*h1[pto+1])

      A = np.array([[-m1,1],[-m2,1]])
      B = np.array([b1,b2])
      
      if np.linalg.det(A) == 0:
        x,y,z,q = np.linalg.lstsq(A,B)
      else:
        x = np.linalg.solve(A,B)

      h1[pto+1] = x[0]
      h2[pto+1] = x[1]

      h1 = np.delete(h1,pto)
      h2 = np.delete(h2,pto)

    return h1,h2