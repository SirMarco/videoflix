from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .tokens import account_activation_token

class UserAuthTests(APITestCase):
    def setUp(self):
        # Erstelle einen Testbenutzer, der für die Login-Tests verwendet wird
        self.email = "testuser@example.com"
        self.password = "securepassword123"
        self.user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.user.is_active = True  # Der Benutzer muss aktiv sein, um sich einzuloggen
        self.user.save()

    def test_login_successful(self):
        # Versuche, dich mit den richtigen Anmeldeinformationen einzuloggen
        url = reverse('login')  # Angenommen, dass der Login-Endpunkt als 'login' benannt wurde
        data = {'username': self.email, 'password': self.password}

        # Sende eine POST-Anfrage an die LoginView
        response = self.client.post(url, data, format='json')

        # Überprüfe, ob der Statuscode erfolgreich ist
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Überprüfe, ob ein Token zurückgegeben wird
        self.assertIn('token', response.data)

    def test_login_failed_invalid_credentials(self):
        # Versuche, dich mit falschen Anmeldeinformationen einzuloggen
        url = reverse('login')  # Angenommen, dass der Login-Endpunkt als 'login' benannt wurde
        data = {'username': self.email, 'password': 'falschesPasswort'}

        # Sende eine POST-Anfrage an die LoginView
        response = self.client.post(url, data, format='json')

        # Überprüfe, ob der Statuscode für ungültige Anmeldeinformationen zurückgegeben wird
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Überprüfe, dass kein Token zurückgegeben wurde
        self.assertNotIn('token', response.data)

class ActivateViewTests(APITestCase):

    def setUp(self):
        # Erstelle einen inaktiven Benutzer zur Verwendung in Tests
        self.email = "testuser@example.com"
        self.password = "securepassword123"
        self.user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.user.is_active = False  # Benutzer ist inaktiv, bis er aktiviert wird
        self.user.save()

        # Generiere ein Aktivierungstoken für diesen Benutzer
        self.token = account_activation_token.make_token(self.user)
        self.activation_url = reverse('activate', kwargs={'id': self.user.pk, 'token': self.token})

    def test_activate_user_successful(self):
        # Teste die erfolgreiche Aktivierung eines Benutzers
        response = self.client.get(self.activation_url)
        
        # Überprüfe, ob die Aktivierung erfolgreich war
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Account erfolgreich aktiviert')

        # Stelle sicher, dass der Benutzer nun aktiv ist
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_user_invalid_token(self):
        # Teste die Aktivierung mit einem ungültigen Token
        invalid_url = reverse('activate', kwargs={'id': self.user.pk, 'token': 'invalidtoken'})
        response = self.client.get(invalid_url)
        
        # Überprüfe, ob der Aktivierungsversuch mit einem ungültigen Token fehlschlägt
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Ungültiger oder abgelaufener Link')     
        
class PasswordResetRequestTests(APITestCase):
    
    def setUp(self):
        self.email = "testuser@example.com"
        self.user = User.objects.create_user(username=self.email, email=self.email, password="password123")
        self.password_reset_url = reverse('password_reset')

    def test_password_reset_request_success(self):
        # Test für einen erfolgreichen Passwort-Reset-Request
        response = self.client.post(self.password_reset_url, data={'email': self.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Überprüfe deine E-Mail, um dein Passwort zurückzusetzen.')

    def test_password_reset_request_user_not_found(self):
        # Test für den Fall, dass die E-Mail nicht existiert
        response = self.client.post(self.password_reset_url, data={'email': 'notfound@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'E-Mail ist nicht registriert.')
