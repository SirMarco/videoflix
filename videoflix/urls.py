from django.contrib import admin
from django.urls import path

from streaming.views import LoginView, RegisterView, ActivateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/activate/<int:id>/<str:token>/', ActivateView.as_view(), name='activate'),
]
