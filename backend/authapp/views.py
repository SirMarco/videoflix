from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .tokens import account_activation_token
from .tasks import send_activation_email
import django_rq


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
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Überprüfe, ob der Benutzer bereits existiert
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            return Response({'error': 'Diese E-Mail ist bereits registriert'}, status=status.HTTP_400_BAD_REQUEST)

        # Erstelle den neuen Benutzer
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()

        # Sende Aktivierungsmail asynchron über die 'high' Queue
        high_queue = django_rq.get_queue('high', autocommit=True)
        high_queue.enqueue(send_activation_email, user.pk)

        # Sende Bestätigungsantwort zurück
        return Response({'message': 'Überprüfe deine E-Mail, um deinen Account zu aktivieren.'}, status=status.HTTP_201_CREATED)
    
class ActivateView(APIView):
    permission_classes = []
    def get(self, request, id, token):
        try:
            user = User.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account erfolgreich aktiviert'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ungültiger oder abgelaufener Link'}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetRequestView(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'E-Mail ist nicht registriert.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()

        reset_link = f"https://videoflix.marco-engelhardt.ch/password-reset/{user.pk}/{token_generator.make_token(user)}"

        mail_subject = 'Passwort zurücksetzen'
        text_content = f"Hallo {user.username},\n\nDu hast eine Anfrage zum Zurücksetzen deines Passworts gestellt. Klicke auf den folgenden Link, um dein Passwort zurückzusetzen:\n\n{reset_link}\n\nWenn du diese Anfrage nicht gestellt hast, ignoriere bitte diese E-Mail."
        html_content  = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        msg = EmailMultiAlternatives(mail_subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response({'message': 'Überprüfe deine E-Mail, um dein Passwort zurückzusetzen.'}, status=status.HTTP_200_OK)     
    
class PasswordResetConfirmView(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            # uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Ungültiger Benutzer.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()

        if user is not None and token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Passwort erfolgreich zurückgesetzt.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ungültiges Token oder abgelaufener Link.'}, status=status.HTTP_400_BAD_REQUEST)