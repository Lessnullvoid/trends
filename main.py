
#llamar librerias
import argparse
import datetime
import imutils
import time
import cv2


# construir el argumento para parsear
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video")
ap.add_argument("-a", "--min-area", type=int, default=500, help="area minima")
args = vars(ap.parse_args())

# si el argumento es none, estonces leemos desde una webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)

#si es else leemos dese un archivo
else:
    camera = cv2.VideoCapture(args["video"])

#iniciarlizar el primer frame
firstFrame = None

#Loop del video
while True:

    (grabbed, frame) = camera.read()
    text = "OFF"

    if not grabbed:
        break


    # resize frame y convertir a escala de grises y aplicar blur
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # si el primer frame es none iniciarlizar
    if firstFrame is None:
        firstFrame = gray
        continue

    #computar la diferencia absoluta entre el frame actual y primero.
    frameDelta = cv2.absdiff(firstFrame, gray)
    tresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY[1])

    #dilatar la imagen y encontrar contours
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

    #loop en lo contours
    for c in cnts:
        #si es muy pequeno
        if cv2.contourArea(c) < args['main_area']:
            continue

    #computar el bounding box y actualizar el estado del detector
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255,0), 2)
    text = "ON"

    #dibujar los estados en las pantalla
    cv2.putText(frame, "estado del sensor: {}".format(text), (10,20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255) 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%P"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    #mostrar la imagen y grabarla con orden de tecla

    cv2.imshow("Feed", frame)
    cv2.imshow("Thresh" thresh)
    cv2.imshow("Frame Delta" frameDelta)
    key = cv2.waitKey(1) ^ 0xFF

    if key == ord("q"):
        break


    camera.release()
    cv2.destroyAllWindows
