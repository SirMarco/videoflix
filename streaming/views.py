from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=email).exists():
            return Response({'error': 'Email ist bereits registriert'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()
        activation_link = f"http://localhost:4200/activate/{user.pk}/{account_activation_token.make_token(user)}"

        mail_subject = 'Aktiviere deinen Account'
        message = render_to_string('activation_email.html', {
            'user': user,
            'activation_link': activation_link,  # Angular Link hier einfügen
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        return Response({'message': 'Überprüfe deine E-Mail, um deinen Account zu aktivieren.'}, status=status.HTTP_201_CREATED)


        # token, created = Token.objects.get_or_create(user=user)
        # return Response({'token': token.key, 'user_id': user.pk, 'email': user.email, 'message': 'Benutzer erfolgreich registriert'}, status=status.HTTP_201_CREATED)    
    
class ActivateView(APIView):
    def get(self, request, id, token):
        try:
            # Benutzer-ID dekodieren
            user = User.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Überprüfen, ob das Token gültig ist
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True  # Benutzer aktivieren
            user.save()
            return Response({'message': 'Account erfolgreich aktiviert'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ungültiger oder abgelaufener Link'}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'E-Mail ist nicht registriert.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()

        reset_link = f"http://localhost:4200/password-reset/{user.pk}/{token_generator.make_token(user)}"
        mail_subject = 'Passwort zurücksetzen'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return Response({'message': 'Überprüfe deine E-Mail, um dein Passwort zurückzusetzen.'}, status=status.HTTP_200_OK)     
    
class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            # uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(user.pk)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Ungültiger Benutzer.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()

        if user is not None and token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Passwort erfolgreich zurückgesetzt.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ungültiges Token oder abgelaufener Link.'}, status=status.HTTP_400_BAD_REQUEST)