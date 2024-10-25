from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from authapp.tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .models import PlaybackProgress, Video
from .serializers import VideoSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# @cache_page(CACHE_TTL)
class VideosView(APIView):
    #method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

# @cache_page(CACHE_TTL)
class VideoDetailView(APIView):
    #@method_decorator(cache_page(CACHE_TTL))
    def get(self, request, video_slug, *args, **kwargs):
        video = get_object_or_404(Video, slug=video_slug)
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetPlaybackProgress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_slug):
        try:
            video = Video.objects.get(slug=video_slug)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

        try:
            progress_record = PlaybackProgress.objects.get(user=request.user, video=video)
            return Response({"progress": progress_record.progress})
        except PlaybackProgress.DoesNotExist:
            return Response({"progress": 0.0})

class SavePlaybackProgress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        video_slug = request.data.get("video_slug")
        progress = request.data.get("progress")
        seen = request.data.get('seen', False)
        print(f"Video Slug: {video_slug}, Progress: {progress}")

        try:
            video = Video.objects.get(slug=video_slug)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)
        user = request.user

        progress_record, created = PlaybackProgress.objects.get_or_create(user=user, video=video)
        progress_record.progress = progress

        if seen:
            progress_record.seen = True
         
        progress_record.save()
        return Response({"message": "Progress saved successfully"})


    
