from django.contrib import admin
from django.urls import path

from streaming.views import LoginView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),

]
