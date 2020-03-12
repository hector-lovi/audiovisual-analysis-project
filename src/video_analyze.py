import cv2
import json
import imutils
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array


def videoAnalyze(video):

    with open('../output/model_sequential84.16370153427124.json', 'r') as f:
        model_json = json.load(f)

    model = model_from_json(model_json)
    model.load_weights(
        '../output/model_sequential84.16370153427124.h5')

    face_cascade = cv2.CascadeClassifier(
        '../haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(video)

    while cap.isOpened():
        frame = cap.read()[1]
        frame = imutils.resize(frame, width=400)
        frameClone = frame.copy()

        try:
            color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(
                color,
                scaleFactor=1.1,
                minNeighbors=5
            )

            if len(face) > 0:
                (x, y, w, h) = face[0]
                roi = color[y:y+h, x:x+w]
                roi = cv2.resize(roi, (60, 60))
                roi = np.stack(roi)
                # if K.image_data_format() == 'channels_first':
                #    roi = roi.reshape(1, 60, 60, 1)
                # else:
                #    roi = roi.reshape(1, 60, 60, 1)

                p = np.expand_dims(roi, axis=0).reshape(
                    np.expand_dims(roi, axis=0).shape[0], 60, 60, 1)

                # predict(np.expand_dims(np_image,axis=0))[0]

                genre = model.predict(p)[0]
                label = ['man', 'woman'][np.argmax(genre)]

                if genre.max() > 0.77:
                    cv2.rectangle(frameClone, (x, y),
                                  (x + w, y + h), (0, 255, 0), 1)
                    cv2.putText(frameClone, label, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

            cv2.imshow('Advertising Analyze',
                       imutils.resize(frameClone, width=450))

        except Exception as e:
            cap.release()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


videoAnalyze('../video_prueba2.mpg')
