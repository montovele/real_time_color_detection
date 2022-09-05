# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import cv2
import imutils
import math

#Comienza la captura de imagen en tiempo real
camera = cv2.VideoCapture(0)

r = g = b = xpos = ypos = 0
#index con los nombres a iterar en conjunto la bd de colores
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
#Aqui se obtiene el conocimiento para para la deteccion en tiempo real
df = pd.read_csv('conocimiento/colores.csv', names = index, header = None)

#Funcion principal para obtener el nombre de cada color iterando en la base de conocimiento colores.cv
def getColorName(R,G,B):
    #Se revisa que no sobrepase la cantidad de datos existentes en colores.cv
	minimum = 10000
	cname =''
	global count
	count =0
 #Iteracion y obtencion de los indices y los nombres obtenidos por cada indice en RGB
	for i in range(len(df)):
		count +=1
		d = abs(R - int(df.loc[i,"R"])) + abs(G - int(df.loc[i,"G"])) + abs(B - int(df.loc[i,"B"]))
		if (d <= minimum):
			minimum = d
			#Nombre de cada color
			colorName=df.loc[i,'color_name']
			#Se valida en tiempo real si es true muestra el menu con los datos del color
   			#Aqui manejamos el color a detectar
			if colorName =="White":
				cname = df.loc[i, 'color_name'] + '   Hex=' + df.loc[i, 'hex']
				if count <1:
					print("Color= ",colorName)
				return cname
			
	return cname

#FUncion para identificar cada color por medio de sus indices en formato RGB y la obtencion de las cordenadas x y
def identify_color(event, x, y, flags, param):
	global b, g, r, xpos, ypos, clicked
	xpos = x
	ypos = y
	b, g, r = frame[y,x]
	b = int(b)
	g = int(g)
	r = int(r)

#Nombre que aparece en la ventana
cv2.namedWindow('Deteccion_color_tiempo_real')
#Al dar click revela el color solo si cumple con la condicion del color especifico if colorName =="White":
cv2.setMouseCallback('Deteccion_color_tiempo_real', identify_color)

while True:
    (grabbed, frame) = camera.read()
    #Tamanio de la ventana
    frame = imutils.resize(frame, width=900)
    kernal = np.ones((5, 5), "uint8")
    ifGetColorName= getColorName(b,g,r)
    #Si es true muestra el menu completo con el color detectado mas su informacion en formato RGB Y HEX
    if ifGetColorName:
        cv2.rectangle(frame, (5,5), (800, 60),(b,g,r), -1)
        text = getColorName(b,g,r) + '   R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(frame,text, (30,30),2, 0.8, (255,255,255),2,cv2.LINE_AA)
        if count ==0:
         print('ifGetColorName',ifGetColorName)
        if(r+g+b >= 600):
            #Cordenadas del recudro de informacion
            cv2.putText(frame,text,(50,50), 2, 0.8, (0,0,0),2,cv2.LINE_AA)
            #Renderiza la ventana
    cv2.imshow('Deteccion_color_tiempo_real',frame)
    #Valida el onclick de la tecla C
    if cv2.waitKey(20) & 0xFF == 27:
        break
    #Cierra el programa
camera.release()
#Destrulle toda ventana
cv2.destroyAllWindows()










