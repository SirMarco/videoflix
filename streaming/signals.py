from streaming.tasks import generate_video_thumbnail, convert_to_hls
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        # Erstelle den HLS-Ordner für das Video
        video_id = instance.id
        source = instance.video_file.path
        hls_output_dir = os.path.join('media', 'hls', str(video_id))
        
        # Konvertiere das Video in HLS
        convert_to_hls(source, hls_output_dir)
        
        # Setze den HLS-Pfad (optional, falls du den Pfad speichern möchtest)
        instance.hls_path = f'/media/hls/{video_id}/master.m3u8'
        
        # Generiere ein Thumbnail (bleibt unverändert)
        thumbnail_relative_path = generate_video_thumbnail(instance.video_file.path, instance.id)
        instance.thumbnail = thumbnail_relative_path
        instance.save()
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):

    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print(f'Video mit ID {instance.id} wurde gelöscht')
