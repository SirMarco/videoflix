from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from streaming.views import LoginView, PasswordResetConfirmView, PasswordResetRequestView, RegisterView, ActivateView, VideosView, VideoDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/activate/<int:id>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('api/v1/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/v1/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/v1/videos/', VideosView.as_view(), name='videos'),
    path('api/v1/videos/<int:video_id>/', VideoDetailView.as_view(), name='video_detail'),
    # path('api/v1/media/', VideosView.as_view(), name='videos'),
    # path('api/v1/media/<int:video_id>/', VideoDetailView.as_view(), name='video_detail'),
]   + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]