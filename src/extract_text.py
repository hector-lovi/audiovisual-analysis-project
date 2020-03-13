import os
import moviepy.editor
import speech_recognition as sr


def extractAudio(video):
    '''
    Transforma el archivo video a un archivo audio, devuelve el audio en formato texto.
    '''
    vFile = moviepy.editor.VideoFileClip(video)
    aFile = vFile.audio

    save = f"{video[:-4]}.wav"
    aFile.write_audiofile(save)

    re = sr.Recognizer()

    with sr.AudioFile(save) as source:
        info_audio = re.record(source)
        text = re.recognize_google(info_audio, language='es-ES')

    os.remove(save)

    return text
