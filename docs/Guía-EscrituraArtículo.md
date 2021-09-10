[Escritura Papers](https://docs.google.com/file/d/15zz-n1lxaeyiZhJYtRrL0X-gYwOn6I41/edit)

---
### Sistema de Recomendación (Luciano)

[Sistema de recomendación](https://docs.google.com/file/d/1-IDaFVlcMcUOo11KTW5NSwaQE5_Sc-VV/edit) - [overleaf](https://www.overleaf.com/project/6053a175fa465c69f71acdd6)
[paper (drive)](https://docs.google.com/document/d/18yYwocuxqfC1oZmKnqSBSCcSGXyDairlFC80RaVGtWw/edit)
[github](https://github.com/LucianoSm20/SistemaRecomencion/tree/RamaA/Jupyter)

**TODO**

- Escritura de paper:
	- Agregar muchas citas en la intro (bibtex)
- Repetir experimentos
	- Optimizar vector de pesos con PSO --> Ignacio
	- Usar atributos normales, +director-likeness, +emotion, +both


###  Collaborative.Window

**TODO**
- Recolección de datos :ok:
	- Historial usuarios: fecha, peli, nota
	- Listas
- Calcular proporción de conexiones entre pares de películas para ventana en historial de usuarios:
````python
def movie_links(user, S, window=100):
	links = []
    window_m=user.movies[0:window]
    for m in user.movies[window::]:
       window_m.pop(0)
       window_m.append(m)
       W=window_m.intersect(S)
	   if window_m[0] in S:
	       mF=window_m[0]
		   links.append([(mF,m) for m in W if m!=mF])
	   if window_m[-1] in S:
	       mL=window_m[-1]
		   links.append([(mL,m) for m in W if m!=mF])
````


---

Identificar (o generar) listas que puedan servir para identificar gustos de usuarios. Por ejemlo, anime-gibli, amsr, accion-marvel, festivales-independientes, cannes, sundance, f-rated, etc.

En vez de encontrar usuario cercanos, encontrar tuplas cercanas (usuario, lista, periodo) y recomendar de estas tuplas. Esto, ya que asumimos que el interés de los usuarios va evolucionando. Por ejemplo, si un usuario a visto durante el último tiempo películas de disney, se le podría recomendar películas de disney que otro usuario, con gustos parecidos en este tipo de pelis, se puso a ver el 2015.

Para validar el modelo, habría que ver que tanto acierta en películas que los usuarios vieron durante el periodo de tiempo considerado.






<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExMDAwNDExMzksMTUyNTI5NTk0OSwxND
c3MDMwNjIsMTY3MDI2MzY0OCwxMzMyODM2OSwtNjcyNTM5NTc5
LC0xMTk1MTQwNjY2LC0xODk2ODgzMzU1LC0xNzUzNDA2NzE4LD
E3ODYxMjk3MDksNDc1NjM4NDI5LC0xODI5NjcwODYsODYzNTk0
MzMxLC04OTM5NDA2NDUsMjA5OTAyMjAxNiwtODkzOTQwNjQ1LD
EzNTE2OTU0MTksLTExNDcwMDYyNDksMjA2MjkxNDU0NCwtMTA3
NTU5MDYyMF19
-->