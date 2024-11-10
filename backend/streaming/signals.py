from streaming.tasks import generate_video_thumbnail, convert_to_hls, generate_video_teaser, update_video_status
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
import os
import django_rq
import shutil

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created and instance.video_file:
        source = instance.video_file.path

        output_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id))

        thumbnail_relative_path = generate_video_thumbnail(instance.video_file.path, instance.id)
        instance.thumbnail = thumbnail_relative_path
        instance.save(update_fields=['thumbnail'])

        instance.status = 'Uploading'
        instance.save(update_fields=['status'])

        queue = django_rq.get_queue('low', autocommit=True)
        hls_job = queue.enqueue(convert_to_hls, source, output_dir, instance.id)
        teaser_job = queue.enqueue(generate_video_teaser, instance.video_file.path, instance.id)

        hls_playlist_url = os.path.join('hls', str(instance.id), 'master.m3u8')

        instance.hls_playlist = hls_playlist_url
        instance.teaser_file = os.path.join('teasers', f'{instance.id}_teaser.mp4')
        instance.save(update_fields=['hls_playlist', 'teaser_file'])

        queue.enqueue(update_video_status, instance.id, depends_on=[hls_job, teaser_job])
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)

    hls_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id))
    if os.path.isdir(hls_dir):
        shutil.rmtree(hls_dir)

    if instance.thumbnail:
        thumbnail_path = instance.thumbnail.path
        if os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)

    if instance.teaser_file:
        teaser_file = instance.teaser_file.path
        if os.path.isfile(teaser_file):
            os.remove(teaser_file)