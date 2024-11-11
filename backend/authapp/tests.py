from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .tokens import account_activation_token


class UserAuthTests(APITestCase):
    def setUp(self):
        self.email = "testuser@example.de"
        self.password = "password"
        self.user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.user.is_active = True
        self.user.save()

    def test_login_successful(self):
        url = reverse('login')
        data = {'username': self.email, 'password': self.password}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('token', response.data)

    def test_login_failed_invalid_credentials(self):
        url = reverse('login')
        data = {'username': self.email, 'password': 'wrongpassword'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertNotIn('token', response.data)


class ActivateViewTests(APITestCase):
    def setUp(self):
        self.email = "testuser@example.de"
        self.password = "password"
        self.user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.user.is_active = False
        self.user.save()

        self.token = account_activation_token.make_token(self.user)
        self.activation_url = reverse('activate', kwargs={'id': self.user.pk, 'token': self.token})

    def test_activate_user_successful(self):
        response = self.client.get(self.activation_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Account erfolgreich aktiviert')

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_user_invalid_token(self):
        invalid_url = reverse('activate', kwargs={'id': self.user.pk, 'token': 'invalidtoken'})
        response = self.client.get(invalid_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Ungültig', response.data['error'])
    
        
class PasswordResetRequestTests(APITestCase):    
    def setUp(self):
        self.email = "testuser@example.de"
        self.user = User.objects.create_user(username=self.email, email=self.email, password="password")
        self.password_reset_url = reverse('password_reset')

    def test_password_reset_request_success(self):
        response = self.client.post(self.password_reset_url, data={'email': self.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Überprüfe deine E-Mail, um dein Passwort zurückzusetzen.')

    def test_password_reset_request_user_not_found(self):
        response = self.client.post(self.password_reset_url, data={'email': 'wrong@example.de'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'E-Mail ist nicht registriert.')
