from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from streaming.views import GetPlaybackProgress, VideosView, VideoDetailView, SavePlaybackProgress

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),

    path('api/v1/', include('authapp.urls')),

    path('api/v1/videos/', VideosView.as_view(), name='videos'),
    path('api/v1/videos/<slug:video_slug>/', VideoDetailView.as_view(), name='video_detail'),
    path('api/v1/save-progress/', SavePlaybackProgress.as_view(), name='save-progress'),
    path('api/v1/get-progress/<slug:video_slug>/', GetPlaybackProgress.as_view(), name='get-progress'),
    
]   + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()