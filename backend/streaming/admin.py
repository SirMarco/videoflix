from django.contrib import admin

from .models import PlaybackProgress, Video, Category

# Register your models here.


class VideoAdmin(admin.ModelAdmin):
    exclude = ('slug', 'hls_playlist', )  # Blendet das 'slug'-Feld komplett aus

admin.site.register(Video, VideoAdmin)
admin.site.register(Category)
admin.site.register(PlaybackProgress)