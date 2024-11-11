from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def send_activation_email(user_id):
    user = User.objects.get(pk=user_id)
    activation_link = f"https://videoflix.marco-engelhardt.ch/activate/{user.pk}/{account_activation_token.make_token(user)}"
    
    mail_subject = 'Aktiviere deinen Account'
    html_content = render_to_string('activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })
    msg = EmailMessage(mail_subject, html_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.content_subtype = "html"
    msg.send()


def send_password_reset_email(user_id):
    user = User.objects.get(pk=user_id)
    token_generator = PasswordResetTokenGenerator()
    reset_link = f"https://videoflix.marco-engelhardt.ch/password-reset/{user.pk}/{token_generator.make_token(user)}"
    
    mail_subject = 'Videoflix - Passwort zurücksetzen'
    html_content = render_to_string('password_reset_email.html', {
        'user': user,
        'reset_link': reset_link,
    })
    msg = EmailMessage(mail_subject, html_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.content_subtype = "html"
    msg.send()