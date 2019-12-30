import cv2
import numpy as np
from scipy.spatial import distance as dist

from tools import *

cap = cv2.VideoCapture(0) #Seleccionar la camara, 0 camara del equipo, 1 para camera conectada.

im_1 = 0 #Mano extendida
im_2 = 0 #Mano contraida
img_counter = 0
sujeto = 0

while True:
    _, frame = cap.read() #tomar frames 

    res = umbralizar(frame)
    
    circulo = cv2.HoughCircles(res,cv2.HOUGH_GRADIENT,2,50,
                                param1=150,param2=36,minRadius=0,maxRadius=30)

    if circulo is not None:
        dibujar_circulos(circulo, res)

    cv2.imshow('frame', frame)
    #cv2.imshow('mediana', mediana)
    #cv2.imshow('gris', gris)

    #cv2.imshow('umbral', umbral)
    #cv2.imshow('res', res)
    cv2.imshow('circulos detectados',res)

    k = cv2.waitKey(1)

    if k%256 == 27:
        # Salir
        print("Cerrando...")
        break

    elif k%256 == 120:
        # Capturar primera imagen con x
        if circulo is not None:
            if circulo.size == 15:
                im_1 = ordenar(circulo)
                for line in im_1:
                    print(line)

                nombre = "opencv_frame"
                img_name = guardar_img(nombre, img_counter, res)
                img_counter += 1

            else:
                print('Presiona x de nuevo...')

    elif k%256 == 110:
        # Capturar segunda imagen con n
        if circulo is not None:
            if circulo.size == 15:
                im_2 = ordenar(circulo)
                print(im_2)

                nombre = "opencv_frame"
                img_name = guardar_img(nombre, img_counter, res)

                img_counter += 1

                imag = cv2.imread(img_name)
                trazar_lineas(imag, im_1, im_2)

                nombre = "sujeto"
                _ = guardar_img(nombre, sujeto, imag)

                cv2.imshow('Trazos', imag)
                sujeto += 1

                
            else:
                print('Presiona n de nuevo')

cv2. destroyAllWindows()

