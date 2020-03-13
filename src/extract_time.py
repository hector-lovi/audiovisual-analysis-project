from moviepy.editor import VideoFileClip


def extractTime(Video):
    '''
    Extraer la duración de un video.
    '''
    clip = VideoFileClip(Video)
    return int(clip.duration)
