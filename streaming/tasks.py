import subprocess
import os
from django.conf import settings

def convert_480p(source):
    target = source + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)

def generate_video_thumbnail(source, video_id):
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir) 
    thumbnail_path = os.path.join(thumbnail_dir, f'{video_id}.jpg')
    cmd = f'ffmpeg -i "{source}" -ss 00:00:01.000 -vframes 1 "{thumbnail_path}"'
    subprocess.run(cmd)

    return os.path.join('thumbnails', f'{video_id}.jpg')  # Pfad zurückgeben, damit dieser in der Datenbank gespeichert werden kann