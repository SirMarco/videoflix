from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include('authapp.urls')),
    path('api/v1/', include('streaming.urls'))
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
) + debug_toolbar_urls()


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


handler404 = custom_404_view
