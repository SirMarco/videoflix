from streaming.tasks import generate_video_thumbnail, convert_to_hls
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
import os
# from django_rq import enqueue
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        # Quellpfad des hochgeladenen Videos
        source = instance.video_file.path
        
        # Zielordner für HLS-Dateien
        output_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id))

        instance.status = 'Uploading'
        instance.save(update_fields=['status'])
        
        # Starte die Konvertierung zu HLS
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_to_hls, source, output_dir, instance.id)
        #master_playlist = convert_to_hls(source, output_dir)
        
        # Pfad, der in der Datenbank gespeichert wird (relativ zu MEDIA_URL)
        hls_playlist_url = os.path.join('hls', str(instance.id), 'master.m3u8')

        thumbnail_relative_path = generate_video_thumbnail(instance.video_file.path, instance.id)
        # In der Datenbank speichern
        instance.hls_playlist = hls_playlist_url
        instance.thumbnail = thumbnail_relative_path
        instance.save(update_fields=['status','hls_playlist', 'thumbnail'])
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):

    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print(f'Video mit ID {instance.id} wurde gelöscht')
