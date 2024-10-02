from streaming.tasks import convert_video_resolutions, generate_video_thumbnail, convert_to_hls
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os

@receiver(post_save, sender=Video)
# def video_post_save(sender, instance, created, **kwargs):
#     print('Video wurde gespeichert')
#     if created:
#         source = instance.video_file.path
        
#     # Starte die Konvertierung in verschiedene Auflösungen
#         resolutions = convert_video_resolutions(source)
    
#     # Speichere die Pfade zu den verschiedenen Auflösungen
#         instance.video_1280p = f'videos/{os.path.basename(resolutions["1280p"])}'
#         instance.video_720p = f'videos/{os.path.basename(resolutions["720p"])}'
#         instance.video_480p = f'videos/{os.path.basename(resolutions["480p"])}'
#         thumbnail_relative_path = generate_video_thumbnail(instance.video_file.path, instance.id)
#         instance.thumbnail = thumbnail_relative_path
#         instance.save()

def video_post_save(sender, instance, created, **kwargs):
    if created:
        # Quellpfad des hochgeladenen Videos
        source = instance.video_file.path
        
        # Zielordner für HLS-Dateien
        output_dir = os.path.join('hls', str(instance.id))
        
        # Starte die Konvertierung zu HLS
        master_playlist = convert_to_hls(source, output_dir)
        
        # Speichere den Pfad zur Master-Playlist im Model
        instance.hls_playlist = master_playlist
        instance.save()
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):

    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print(f'Video mit ID {instance.id} wurde gelöscht')
