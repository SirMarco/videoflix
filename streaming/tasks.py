import subprocess
import os
from django.conf import settings

def convert_to_hls(source, output_dir):
    """
    Konvertiert das Quellvideo in mehrere Auflösungen und erzeugt eine HLS-Playlist.
    
    :param source: Pfad zur Originalvideodatei
    :param output_dir: Zielverzeichnis für die HLS-Dateien
    """
    # Erstelle das Ausgabe-Verzeichnis, wenn es nicht existiert
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Pfade für die Ausgabe der verschiedenen Auflösungen
    master_playlist_path = os.path.join(output_dir, 'master.m3u8')

    cmd = f"""
    ffmpeg -i "{source}" \
    -vf "scale=w=1280:h=720:force_original_aspect_ratio=decrease" -c:a aac -ar 48000 -c:v h264 -profile:v main -crf 20 -sc_threshold 0 -g 48 -keyint_min 48 -hls_time 4 -hls_playlist_type vod -b:v 2000k -maxrate 2000k -bufsize 4000k -b:a 192k -hls_segment_filename "{output_dir}/720p_%03d.ts" "{output_dir}/720p.m3u8" \
    -vf "scale=w=854:h=480:force_original_aspect_ratio=decrease" -c:a aac -ar 48000 -c:v h264 -profile:v main -crf 20 -sc_threshold 0 -g 48 -keyint_min 48 -hls_time 4 -hls_playlist_type vod -b:v 1000k -maxrate 1000k -bufsize 2000k -b:a 128k -hls_segment_filename "{output_dir}/480p_%03d.ts" "{output_dir}/480p.m3u8" \
    -vf "scale=w=640:h=360:force_original_aspect_ratio=decrease" -c:a aac -ar 48000 -c:v h264 -profile:v main -crf 20 -sc_threshold 0 -g 48 -keyint_min 48 -hls_time 4 -hls_playlist_type vod -b:v 500k -maxrate 500k -bufsize 1000k -b:a 128k -hls_segment_filename "{output_dir}/360p_%03d.ts" "{output_dir}/360p.m3u8"
    """

    # Führe den FFmpeg-Befehl aus, um das Video in HLS-Format zu konvertieren
    subprocess.run(cmd, shell=True, check=True)

    # Erstelle die Master-Playlist (master.m3u8)
    with open(master_playlist_path, 'w') as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=1280x720\n")
        f.write("720p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=854x480\n")
        f.write("480p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=500000,RESOLUTION=640x360\n")
        f.write("360p.m3u8\n")
    
    print(f"HLS-Konvertierung abgeschlossen und in {output_dir} gespeichert.")

def generate_video_thumbnail(source, video_id):
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir) 
    thumbnail_path = os.path.join(thumbnail_dir, f'{video_id}.jpg')
    cmd = f'ffmpeg -i "{source}" -ss 00:00:01.000 -vframes 1 "{thumbnail_path}"'
    subprocess.run(cmd)

    return os.path.join('thumbnails', f'{video_id}.jpg')  # Pfad zurückgeben, damit dieser in der Datenbank gespeichert werden kann