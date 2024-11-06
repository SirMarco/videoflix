from streaming.tasks import generate_video_thumbnail, convert_to_hls
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
import os
import django_rq
import shutil

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        source = instance.video_file.path

        output_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id))

        instance.status = 'Uploading'
        instance.save(update_fields=['status'])

        queue = django_rq.get_queue('low', autocommit=True)
        queue.enqueue(convert_to_hls, source, output_dir, instance.id)

        hls_playlist_url = os.path.join('hls', str(instance.id), 'master.m3u8')

        thumbnail_relative_path = generate_video_thumbnail(instance.video_file.path, instance.id)

        instance.hls_playlist = hls_playlist_url
        instance.thumbnail = thumbnail_relative_path
        instance.save(update_fields=['status','hls_playlist', 'thumbnail'])
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print(f'Video-Datei mit ID {instance.id} wurde gelöscht')

    hls_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id))
    if os.path.isdir(hls_dir):
        shutil.rmtree(hls_dir)
        print(f'HLS-Verzeichnis für Video mit ID {instance.id} wurde gelöscht')

    if instance.thumbnail:
        thumbnail_path = instance.thumbnail.path  # Korrektur: .path hinzufügen, um den tatsächlichen Pfad zu erhalten
        if os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)
            print(f'Thumbnail für Video mit ID {instance.id} wurde gelöscht')
