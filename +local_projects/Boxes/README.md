# Graficador de contenedores
Este graficador permite ver tangiblemente las instancias de los 
contenedores.

## Requerimientos
Los unicos requerimientos de este programa son:
- Python 3
- plotly (Instalar usando pip3 install plotly)

## Formato de las instancias
La primera linea debe contener la dimension del contenedor en forma y
las siguientes lineas deben corresponder a las las coordenadas de los
limites de las cajas. Por ejemplo:

```
(100,100,100)
(0,0,0),(97,40,77)
(0,40,0),(98,90,78)
(0,90,0),(93,92,77)
(0,0,78),(99,91,100)
(0,92,0),(97,97,99)
(0,97,0),(95,100,100)
```

# Como utilizarlo
Corra el programa utilizando python 3. Además, debe especificar el
archivo que contiene la instancia utilizando el argumento -f y a
continuación escribir el nombre del archivo. Ejemplo:
`python3 main.py -f instancia.txt`
