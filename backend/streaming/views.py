from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from django.conf import settings

from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .models import PlaybackProgress, Video
from streaming.models import Video
from .serializers import VideoSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
class VideosView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'slug'

class PlaybackProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_slug):
        video = get_object_or_404(Video, slug=video_slug)        
        progress_record = PlaybackProgress.objects.filter(user=request.user, video=video).first()
        progress = progress_record.progress if progress_record else 0.0
        return Response({"progress": progress})

    def post(self, request, video_slug):
        progress = request.data.get("progress")
        seen = request.data.get("seen", False)
        video = get_object_or_404(Video, slug=video_slug)

        progress_record, created = PlaybackProgress.objects.get_or_create(user=request.user, video=video)
        progress_record.progress = progress
        if seen:
            progress_record.seen = True
        progress_record.save()
        
        return Response({"message": "Progress saved successfully"})
    
