import os
import cv2
import json
import imutils
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array


def videoAnalyze(video):
    '''
    Video-analisis capaz de reconocer el restro de personas y clasificar por género.
    '''
    # Cargar modelo
    with open('..\\output\\model_sequential84.16370153427124.json', 'r') as f:
        model_json = json.load(f)

    model = model_from_json(model_json)
    model.load_weights(
        '..\\output\\model_sequential84.16370153427124.h5')

    face_cascade = cv2.CascadeClassifier(
        '..\\haarcascade_frontalface_default.xml')

    # Crear carpeta para guardar frame
    path = video.split('/')[-1][:-4]
    if not os.path.exists(f'..\\output\\frames\\{path}'):
        os.mkdir(f'..\\output\\frames\\{path}')

    cap = cv2.VideoCapture(video)
    result = []

    while cap.isOpened():
        image = cap.read()[1]

        try:
            frame = imutils.resize(image, width=400)
            color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(
                color,
                scaleFactor=1.1,
                minNeighbors=5
            )

            frameClone = frame.copy()

            if len(face) > 0:
                for n in range(len(face)):
                    (x, y, w, h) = face[n]
                    roi = color[y:y+h, x:x+w]
                    roi = cv2.resize(roi, (60, 60))
                    roi = np.stack(roi)

                    p = np.expand_dims(roi, axis=0).reshape(
                        np.expand_dims(roi, axis=0).shape[0], 60, 60, 1)

                    genre = model.predict(p)[0]
                    label = ['man', 'woman'][np.argmax(genre)]

                    result.append(label)

                    if genre.max() > 0.80:
                        if label == 'man':
                            cv2.rectangle(frameClone, (x, y),
                                          (x + w, y + h), (0, 0, 255), 1)
                            cv2.putText(frameClone, label, (x, y - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

                        elif label == 'woman':
                            cv2.rectangle(frameClone, (x, y),
                                          (x + w, y + h), (0, 255, 0), 1)
                            cv2.putText(frameClone, label, (x, y - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

                    elif not os.path.exists(f'..\\output\\frames\\{path}\\frame.jpg'):
                        cv2.imwrite(
                            f'..\\output\\frames\\{path}\\frame.jpg', frame)

            cv2.imshow('Análisis visual',
                       imutils.resize(frameClone, width=400))

        except:
            cap.release()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    m = result.count('man')
    w = result.count('woman')

    true_m = float("{0:.2f}".format((m/(m+w))*100))
    true_w = float("{0:.2f}".format((w/(m+w))*100))

    return list((true_w, true_m))


# videoAnalyze('..\\input\\video_prueba1.mpg')
