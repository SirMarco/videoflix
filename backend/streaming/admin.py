from django.contrib import admin
from .models import PlaybackProgress, Video, Category

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_categories')
    fields = ('title', 'description', 'video_file', 'categories', 'created_at')
    list_filter = ('categories',)
    search_fields = ('title', 'description')

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass 

@admin.register(PlaybackProgress)
class PlaybackProgressAdmin(admin.ModelAdmin):
    list_display = ('video_title', 'user', 'progress', 'updated_at')
    list_filter = ('updated_at',)

    def video_title(self, obj):
        return obj.video.title
    video_title.short_description = 'Video Title'
