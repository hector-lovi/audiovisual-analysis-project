import os
import moviepy.editor
import speech_recognition as sr
import langcodes


def languageDetect(lang):
    # lang = lang.lower()
    # lang = lang.capitalize()
    sp = ['es', 'ca', 'eu', 'gl']

    lang = langcodes.find(lang).language
    if lang == 'en':
        lang = lang + '-GB'

    elif lang in sp:
        lang = lang + '-ES'

    else:
        raise Exception(
            'Sorry, language not supported for analysis.\nPlease, select a valid language.')

    return lang


def extractAudio(video, lang):
    '''
    Transforma el archivo video a un archivo audio y devuelve el audio en formato texto.
    '''
    vFile = moviepy.editor.VideoFileClip(video)
    aFile = vFile.audio

    video = video.split('\\')[-1]
    save = f"{video[:-4]}.wav"
    aFile.write_audiofile(save)

    re = sr.Recognizer()

    with sr.AudioFile(save) as source:
        info_audio = re.record(source)
        text = re.recognize_google(info_audio, language=languageDetect(lang))

    os.remove(save)

    return text
