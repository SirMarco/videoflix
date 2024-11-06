import os
import subprocess
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Video

FFMPEG_PATH = '/usr/bin/ffmpeg'
AUDIO_PARAMS = ['-c:a', 'aac', '-ar', '48000']
VIDEO_CODEC = ['-c:v', 'h264', '-profile:v', 'main', '-crf', '20', '-g', '48', '-keyint_min', '48']
HLS_PARAMS = ['-hls_time', '4', '-hls_playlist_type', 'vod']

RESOLUTIONS = [
    ("1920x1080", "1080p", "4500000"),
    ("1280x720", "720p", "2000000"),
    ("854x480", "480p", "1000000"),
]

def build_ffmpeg_command(source, res, name, bitrate, segment_path, output_path):
    scale_filter = f'scale=trunc(oh*a/2)*2:480' if name == "480p" else f'scale={res}:force_original_aspect_ratio=decrease'
    return [
        FFMPEG_PATH, '-i', source,
        '-vf', scale_filter,
        *AUDIO_PARAMS,
        *VIDEO_CODEC,
        '-b:v', bitrate, '-maxrate', bitrate, '-bufsize', str(int(bitrate) * 2),
        '-hls_segment_filename', segment_path,
        *HLS_PARAMS,
        output_path
    ]

def write_master_playlist(output_dir, resolutions):
    master_playlist_path = os.path.join(output_dir, 'master.m3u8')
    with open(master_playlist_path, 'w') as f:
        f.write("#EXTM3U\n")
        for res, name, bitrate in resolutions:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate},RESOLUTION={res}\n")
            f.write(f"{name}.m3u8\n")
    return master_playlist_path

def update_video_status(video_id):
    video = Video.objects.get(id=video_id)
    video.status = 'Done'
    video.save(update_fields=['status'])
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "broadcast",
        {
            "type": "video.status_update",
            "slug": video.slug,
            "status": video.status,
        }
    )

def generate_video_thumbnail(source, video_id):
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    os.makedirs(thumbnail_dir, exist_ok=True)
    
    thumbnail_path = os.path.join(thumbnail_dir, f'{video_id}.jpg')

    # ffmpeg command to generate thumbnail
    cmd = [
        FFMPEG_PATH, '-i', source, 
        '-ss', '00:00:01.000', 
        '-vframes', '1', 
        thumbnail_path
    ]
    
    # Execute the command
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Error handling if ffmpeg fails
    if result.returncode != 0:
        print(f"Error generating thumbnail: {result.stderr.decode('utf-8')}")
        raise Exception(f"FFmpeg failed: {result.stderr.decode('utf-8')}")

    return os.path.join('thumbnails', f'{video_id}.jpg')  # Return relative path

def convert_to_hls(source, output_dir, video_id):
    output_dir = os.path.join(settings.MEDIA_ROOT, output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for res, name, bitrate in RESOLUTIONS:
        output_path = os.path.join(output_dir, f'{name}.m3u8')
        segment_path = os.path.join(output_dir, f'{name}_%03d.ts')

        cmd = build_ffmpeg_command(source, res, name, bitrate, segment_path, output_path)

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion of {name}: {e}")
            continue

    master_playlist_path = write_master_playlist(output_dir, RESOLUTIONS)
    update_video_status(video_id)

    return master_playlist_path
