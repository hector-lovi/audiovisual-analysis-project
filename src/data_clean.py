import cv2


def cleanData(img):
    '''
    Reconoce el rostro de personas sobre imágenes:
    - Crea una sección que encuadra el rostro.
    - Transforma la imagen a escala de grises.
    - Reescala la imagen a 48x48.
    - Traduce la información del cuadrante a np.array.

    En el caso de no reconocer ningun rostro devuelve /no.
    '''

    face_cascade = cv2.CascadeClassifier(
        '../haarcascade_frontalface_default.xml')

    try:
        image = cv2.imread(img, cv2.IMREAD_COLOR)
        face_p = face_cascade.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5
        )

        (x, y, w, h) = face_p[0]

        crop_image = image[y:y+h, x:x+w]

        img_data = cv2.resize(crop_image, (60, 60))

    except:
        pass

    return img_data
