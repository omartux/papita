import cv2 as cv
import numpy as np
import time     #importa time para hacer delays
from datetime import date, datetime #importa libreria dia de hoy fechas
import os

directory = r'.\imagenes'
contador = 0
for entry in os.scandir(directory):
    if (entry.path.endswith(".jpg") or entry.path.endswith(".JPG")) and entry.is_file():
        print(entry.path)
        
        umbrali = 85
        umbrals = 3
        edges = 0
        objetos = 10
        grosor = 2

        image = cv.imread(entry.path, 3)
        dimensions = image.shape
        h = image.shape[0]
        w = image.shape[1]
        ch = image.shape[2]
        
        roi = image.copy()
        roi = roi[int(h*0.22):int(h*0.62), int(w*0.37):int(w*0.8)]
        segmentacion = roi.copy()
        image = roi    
        
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        
        median_pix = np.median(gray)
        lower = int(median_pix*0.6)
        upper = int(lower*1.4)
        
        canny_i = lower
        canny_s = upper
        
        edges = cv.Canny(blur, lower, upper)
        (contornos,_) = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #contenido = contornos[0]
        objetos = int(len(contornos))
        print("He encontrado {} objetos".format(len(contornos)))
            

        print (objetos)    
        print (lower, upper)

        edges = cv.Canny(blur, lower, upper)

        image2 = image.copy()
        canny = edges.copy()
        
        
        canny = cv.drawContours(canny, contornos[0], -1, (255,255,255), thickness = grosor)  

        canny = cv.GaussianBlur(canny, (7, 7), 0)
        
        thresh = cv.threshold(canny, 5, 255, cv.THRESH_BINARY)[1]

        # get the (largest) contour
        contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        big_contour = max(contours, key=cv.contourArea)

        # draw white filled contour on black background
        mask = np.zeros(image.shape[:2], np.uint8)
        mask = cv.drawContours(mask, [big_contour], 0, (255,255,255), cv.FILLED)

        # save results
        
        result = cv.bitwise_and(image, image, mask=mask)

        #grabaimagenes

        Area= np.sum(mask)
        Area=int(Area)
        
        lab = cv.cvtColor(result, cv.COLOR_BGR2LAB)
        L,A,B = cv.split(lab)
        
        mL = np.mean(L)
        mA = np.mean(A)
        mB = np.mean(B)
        
        
        hoy = date.today()
        ahora = datetime.now()
        tiempo_actual = ahora.strftime("%H:%M:%S")
        
            
        archivo = open('valores_papa.csv', "a")
        cadena = (str(hoy)+";"+str(tiempo_actual)+";"+str('00_'+str(entry.name))+
                    ";"+str(canny_i)+";"+str(canny_s)+
                    ";"+str(mL)+";"+str(mA)+";"+str(mB)+";"+str(Area)+
                    ";"+str(Area*11.3774/3924705)+"\n")
        archivo.write(cadena)
        archivo.close()
        
        path = ".\salida\\"
        print (path+entry.name)
        cv.imwrite(str(path+entry.name), result)
        cv.imwrite(str(path+entry.name)+'_gris.jpg', gray)
        cv.imwrite(str(path+entry.name)+'_blur.jpg', blur)
        cv.imwrite(str(path+entry.name)+'_b_.jpg', edges )
        cv.imwrite(str(path+entry.name)+'_m_.jpg',mask)
        cv.imwrite(str(path+entry.name)+'_segmentado.jpg',segmentacion)
    
        contador = contador+1
    
    print (contador)
    
#exit()


    
    


                                                                                         
