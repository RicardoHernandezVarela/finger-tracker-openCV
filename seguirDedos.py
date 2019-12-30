import cv2
import numpy as np

from tools import *

cap = cv2.VideoCapture(0) #Seleccionar la camara, 0 camara del equipo, 1 para camera conectada.
circulos_arr = []
circulos = []
trackerType = 'CSRT'

while True:
    _, frame = cap.read() #tomar frames 

    res = umbralizar(frame)
    
    circulo = cv2.HoughCircles(res,cv2.HOUGH_GRADIENT,2,50,
                                param1=150,param2=36,minRadius=0,maxRadius=30)

    if circulo is not None:
        dibujar_circulos(circulo, res)
        if circulo.size == 15:
            circulo = np.uint16(np.around(circulo, out=None))
            circulos_arr = ordenar(circulo)
            for vect in circulos_arr:
                vect = np.insert(vect, 3, vect[2]+1)
                print(vect)
                circulos.append(tuple(vect))
            print(circulos)
            break
       
    cv2.imshow('frame', frame)
    cv2.imshow('circulos detectados',res)

    k = cv2.waitKey(1)

    if k%256 == 113:
        # Salir
        print("Cerrando...")
        break


# Crear objeto MultiTracker 
multiTracker = cv2.MultiTracker_create()

# Inicializar MultiTracker 
for circ in circulos:
    multiTracker.add(createTrackerByName(trackerType), frame, circ)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
      break
    
    res = umbralizar(frame)

    success, circs = multiTracker.update(res)

    # dibujar circulos
    for i, newbox in enumerate(circs):
        centroide = (int(newbox[0]), int(newbox[1]))
        cv2.circle(frame,centroide,int(newbox[2]),(120,120,120),2)
        cv2.circle(res,centroide,int(newbox[2]),(0,0,0),2)

    # Mostrar frame
    cv2.imshow('MultiTracker', frame)
    cv2.imshow('circulos detectados',res)

    # salir con botón ESC
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
      break