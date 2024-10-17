from django.contrib import admin

from .models import PlaybackProgress, Video, Category

# Register your models here.

admin.site.register(Video)
admin.site.register(Category)
admin.site.register(PlaybackProgress)