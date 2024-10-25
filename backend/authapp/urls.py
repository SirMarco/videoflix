# authapp/urls.py
from django.urls import path
from authapp.views import LoginView, RegisterView, ActivateView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<int:id>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
