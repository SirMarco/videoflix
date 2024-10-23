import subprocess
import os
from django.conf import settings
from .models import Video
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def convert_to_hls(source, output_dir, video_id):
    """
    Konvertiert ein Video in HLS-Segmente in verschiedenen Auflösungen und erstellt eine Master-Playlist (M3U8).
    
    :param source: Pfad zur Originalvideodatei
    :param output_dir: Zielverzeichnis für die HLS-Dateien
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # HLS für 1080p, 720p und 480p erstellen
    resolutions = [
        ("1920x1080", "1080p", "4500000"),  # 4.5 Mbps für 1080p
        ("1280x720", "720p", "2000000"),    # 2 Mbps für 720p
        ("854x480", "480p", "1000000"),     # 1 Mbps für 480p
    ]

    for res, name, bitrate in resolutions:
        output_path = os.path.join(output_dir, f'{name}.m3u8')
        segment_path = os.path.join(output_dir, f'{name}_%03d.ts')

        # FFmpeg-Befehl für jede Auflösung, angepasst für 480p
        if name == "480p":
            cmd = [
                '/usr/bin/ffmpeg', '-i', source,
                '-vf', f'scale=trunc(oh*a/2)*2:480',
                '-c:a', 'aac', '-ar', '48000', '-c:v', 'h264', '-profile:v', 'main', '-crf', '20',
                '-g', '48', '-keyint_min', '48',
                '-hls_time', '4', '-hls_playlist_type', 'vod',
                '-b:v', bitrate, '-maxrate', bitrate, '-bufsize', f'{int(int(bitrate) * 2)}',
                '-hls_segment_filename', segment_path, output_path
            ]
        else:
            cmd = [
                '/usr/bin/ffmpeg', '-i', source,
                '-vf', f'scale={res}:force_original_aspect_ratio=decrease',
                '-c:a', 'aac', '-ar', '48000', '-c:v', 'h264', '-profile:v', 'main', '-crf', '20',
                '-g', '48', '-keyint_min', '48',
                '-hls_time', '4', '-hls_playlist_type', 'vod',
                '-b:v', bitrate, '-maxrate', bitrate, '-bufsize', f'{int(int(bitrate) * 2)}',
                '-hls_segment_filename', segment_path, output_path
            ]


        try:
            subprocess.run(cmd, check=True)
            print(f"HLS für {name} erstellt: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Fehler bei der Konvertierung von {name}: {e}")

    # Master-Playlist erstellen
    master_playlist_path = os.path.join(output_dir, 'master.m3u8')
    with open(master_playlist_path, 'w') as f:
        f.write("#EXTM3U\n")
        for res, name, bitrate in resolutions:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate},RESOLUTION={res}\n")
            f.write(f"{name}.m3u8\n")

    video = Video.objects.get(id=video_id)
    video.status = 'Done'
    video.save(update_fields=['status'])
    # Sende eine WebSocket-Nachricht, um den Status zu aktualisieren
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "broadcast",
        {
            "type": "video.status_update",
            "slug": video.slug,
            "status": video.status,
        }
    )
    
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

    # ffmpeg-Befehl als Liste an subprocess.run übergeben
    cmd = [
        '/usr/bin/ffmpeg', '-i', source, 
        '-ss', '00:00:01.000', 
        '-vframes', '1', 
        thumbnail_path
    ]
    
    # subprocess.run ausführen
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Fehlerbehandlung hinzufügen, falls ffmpeg fehlschlägt
    if result.returncode != 0:
        print(f"Fehler beim Erstellen des Thumbnails: {result.stderr.decode('utf-8')}")
        raise Exception(f"FFmpeg failed: {result.stderr.decode('utf-8')}")

    return os.path.join('thumbnails', f'{video_id}.jpg')  # Relativen Pfad zurückgeben