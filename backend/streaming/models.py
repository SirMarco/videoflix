from datetime import date
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Video(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(max_length=500,)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    teaser_file = models.FileField(upload_to='teasers', blank=True, null=True)
    hls_playlist = models.FileField(blank=True, null=True)
    thumbnail = models.FileField(upload_to = 'thumbnails', blank=True, null=True)
    created_at = models.DateField(default=date.today)
    categories = models.ManyToManyField(Category, related_name='videos')
    status = models.CharField(max_length=10, default='pending')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Video.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PlaybackProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)
    seen = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.video.title} - {self.user.username} ({self.progress}%)"

    