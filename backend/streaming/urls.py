from django.urls import path
from streaming.views import VideosView, VideoDetailView, PlaybackProgressView

urlpatterns = [
    path('videos/', VideosView.as_view(), name='videos'),
    path('videos/<slug:slug>/', VideoDetailView.as_view(), name='video_detail'),
    path('progress/<slug:video_slug>/', PlaybackProgressView.as_view(), name='playback-progress')
]
