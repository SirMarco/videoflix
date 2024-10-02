import subprocess
import os
from django.conf import settings

import subprocess
import os

def convert_to_hls(source, output_dir):
    """
    https://www.botreetechnologies.com/blog/video-audio-transmuxing-into-hls-using-ffmpeg-hls-muxer-in-django/
    Konvertiert ein Video in HLS-Segmente in verschiedenen Auflösungen und erstellt eine Master-Playlist (M3U8).
    
    :param source: Pfad zur Originalvideodatei
    :param output_dir: Zielverzeichnis für die HLS-Dateien
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, output_dir)

    print('der source dir:' + source)
    print('der output dir:' + output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # HLS für 1080p, 720p und 480p erstellen
    resolutions = [
        ("1280x720", "720p", "2000k"),
        ("640x360", "360p", "500k"),
    ]

    for res, name, bitrate in resolutions:
        output_path = os.path.join(output_dir, f'{name}.m3u8')
        segment_path = os.path.join(output_dir, f'{name}_%03d.ts')


        # FFmpeg-Befehl für jede Auflösung
        cmd = [
            'ffmpeg', '-i', source,
            '-vf', f'scale={res}:force_original_aspect_ratio=decrease',
            '-c:a', 'aac', '-ar', '48000', '-c:v', 'h264', '-profile:v', 'main', '-crf', '20',
            '-g', '48', '-keyint_min', '48',
            '-hls_time', '4', '-hls_playlist_type', 'vod',
            '-b:v', bitrate, '-maxrate', bitrate, '-bufsize', f'{int(bitrate[:-1]) * 2}k',
            '-hls_segment_filename', segment_path, output_path
        ]

        # Führe den FFmpeg-Prozess aus
        try:
            subprocess.run(cmd, check=True)
            print(f"HLS für {name} erstellt: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Fehler bei der Konvertierung von {name}: {e}")

    # Master-Playlist erstellen
    master_playlist_path = os.path.join(output_dir, 'master.m3u8')
    with open(master_playlist_path, 'w') as f:
        f.write("#EXTM3U\n")
        for _, name, _ in resolutions:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate},RESOLUTION={name}\n")
            f.write(f"{name}.m3u8\n")

    print(f"Master-Playlist erstellt: {master_playlist_path}")
    return master_playlist_path



def convert_video_resolutions(source):
    """
    Konvertiert das Quellvideo in 1280p, 720p und 480p Auflösungen.
    
    :param source: Pfad zur Originalvideodatei
    """
    # Definiere die verschiedenen Auflösungen und die Dateinamen
    resolutions = {
        '1280p': '1280x720',
        '720p': '1280x720',
        '480p': '854x480',
    }

    for name, resolution in resolutions.items():
        target = f"{os.path.splitext(source)[0]}_{name}.mp4"
        cmd = f'ffmpeg -i "{source}" -vf "scale={resolution}:force_original_aspect_ratio=decrease" -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
        
        # Führe den FFmpeg-Befehl aus
        try:
            print(f"Konvertiere {name} Auflösung...")
            subprocess.run(cmd, shell=True, check=True)
            print(f"Erfolgreich konvertiert: {target}")
        except subprocess.CalledProcessError as e:
            print(f"Fehler bei der Konvertierung von {name}: {e}")

def generate_video_thumbnail(source, video_id):
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir) 
    thumbnail_path = os.path.join(thumbnail_dir, f'{video_id}.jpg')
    cmd = f'ffmpeg -i "{source}" -ss 00:00:01.000 -vframes 1 "{thumbnail_path}"'
    subprocess.run(cmd)

    return os.path.join('thumbnails', f'{video_id}.jpg')  # Pfad zurückgeben, damit dieser in der Datenbank gespeichert werden kann