import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Video, Category, PlaybackProgress
from .serializers import VideoSerializer
from django.contrib.auth.models import User
from django.utils.text import slugify

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def video():
    return Video.objects.create(title="Test Video", slug="test-video", description="Test Description")


def test_video_list(api_client, user, video):
    api_client.force_authenticate(user=user)

    url = reverse("videos") 
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    serialized_data = VideoSerializer([video], many=True).data
    assert response.json() == serialized_data


def test_video_detail(api_client, user, video):
    api_client.force_authenticate(user=user)

    url = reverse("video_detail", kwargs={"slug": video.slug})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    serialized_data = VideoSerializer(video).data
    assert response.json() == serialized_data


# MODELS VIDEO TEST
    
def test_video_creation_without_slug():
    video = Video.objects.create(title="Slug Video Test", description="A Slug video.")
    expected_slug = slugify("Slug Video Test")
    assert video.slug == expected_slug
    assert str(video) == "Slug Video Test"


def test_unique_slug_generation():
    video1 = Video.objects.create(title="Unique Video", description="First video.")
    video2 = Video.objects.create(title="Unique Video", description="Second video.")
    assert video1.slug != video2.slug


def test_video_category_relationship():
    category = Category.objects.create(name="Documentary")
    video = Video.objects.create(title="Documentary Video", description="A documentary.")
    video.categories.add(category)
    assert category in video.categories.all()


# MODELS PLAYBACK TEST


def test_playback_progress_creation():
    user = User.objects.create_user(username="testuser", password="password")
    video = Video.objects.create(title="Sample Video", description="Sample video description.")
    progress = PlaybackProgress.objects.create(user=user, video=video, progress=30.0)

    assert progress.user == user
    assert progress.video == video
    assert progress.progress == 30.0
    assert str(progress) == f"{video.title} - {user.username} (30.0%)"


def test_playback_progress_update():
    user = User.objects.create_user(username="testuser", password="password")
    video = Video.objects.create(title="Sample Video", description="Sample video description.")
    progress = PlaybackProgress.objects.create(user=user, video=video, progress=30.0)
    
    progress.progress = 70.0
    progress.seen = True
    progress.save()

    progress.refresh_from_db()
    assert progress.progress == 70.0
    assert progress.seen is True
