from datetime import date
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Video(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to = 'videos', blank = True, null =True)
    thumbnail = models.FileField(upload_to = 'thumbnails', blank=True, null=True)
    created_at = models.DateField(default=date.today)
     # Verknüpfung zur Kategorie
    categories = models.ManyToManyField(Category, related_name='videos')

    def __str__(self):
        return self.title
    
