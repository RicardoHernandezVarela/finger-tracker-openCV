import cv2
import numpy as np
from scipy.spatial import distance as dist

def dibujar_circulos(info, cimg):
    circulos = np.uint16(np.around(info, out=None))

    for i in circulos[0,:]:
        # dibujar circulo exterior
        cv2.circle(cimg,(i[0],i[1]),i[2],(255,255,255),2)
        # dibujar centro
        cv2.circle(cimg,(i[0],i[1]),2,(20,20,20),3)

def ordenar(ar):
    arreglo = ar[0]

    arreglo = sorted(arreglo, key=lambda arreglo_entry: arreglo_entry[0])
    arreglo = np.array(arreglo)
    return arreglo

def guardar_img(nombre, img_counter, res):
    img_name = nombre + "_{}.png".format(img_counter)
    cv2.imwrite(img_name, res)
    print("{} capturada!".format(img_name))
    return img_name

def trazar_lineas(imag, im1, im2):
    frame1 = im1
    frame2 = im2

    for i in range(0, 5):
        fila1 = frame1[i]
        fila2 = frame2[i]

        #Dibujar líneas
        cv2.line(imag, (fila1[0],fila1[1]), (fila2[0],fila2[1]), (0, 215, 255), 2)
        D = dist.euclidean((fila1[0],fila1[1]), (fila2[0],fila2[1]))
        cv2.putText(imag, "{:.1f}px".format(D), (int(fila1[0] - 25), int(fila1[1] - 35)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

        cv2.putText(imag, str(i), (int(fila1[0] - 25), int(fila1[1] + 35)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

        #cv2.putText(img, text, (x, h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 

        #Dibujar circulos
        cv2.circle(imag,(fila1[0],fila1[1]),fila1[2],(255,0,0),2)
        cv2.circle(imag,(fila1[0],fila1[1]),2,(180,180,180),3)

def umbralizar(frame):
        mediana = cv2.medianBlur(frame, 23)

        gris = cv2.cvtColor(mediana, cv2.COLOR_BGR2GRAY)
        _, umbral = cv2.threshold(gris, 165, 255, cv2.THRESH_BINARY)

        res = cv2.bitwise_and(frame, frame, mask=umbral)
        res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        return res

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == trackerTypes[0]:
    tracker = cv2.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]: 
    tracker = cv2.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv2.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv2.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv2.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv2.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv2.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv2.TrackerCSRT_create()
  else:
    tracker = None
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)
    
  return tracker
