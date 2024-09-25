from django.contrib import admin
from django.urls import path

from streaming.views import LoginView, PasswordResetConfirmView, PasswordResetRequestView, RegisterView, ActivateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/activate/<int:id>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
