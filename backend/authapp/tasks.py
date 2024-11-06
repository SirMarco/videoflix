from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .tokens import account_activation_token
import logging

logger = logging.getLogger(__name__)

def send_activation_email(user_id):
    try:
        user = User.objects.get(pk=user_id)
        activation_link = f"https://videoflix.marco-engelhardt.ch/activate/{user.pk}/{account_activation_token.make_token(user)}"
        
        mail_subject = 'Aktiviere deinen Account'
        text_content = f"Hallo {user.username},\n\nBitte klicke auf den unten stehenden Link, um deinen Account zu aktivieren:\n\n{activation_link}\n\nWenn du den Account nicht erstellt hast, ignoriere bitte diese E-Mail."

        html_content = render_to_string('activation_email.html', {
            'user': user,
            'activation_link': activation_link, 
        })
        
        msg = EmailMultiAlternatives(mail_subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
    except User.DoesNotExist:
        logger.error(f"User mit ID {user_id} existiert nicht")
    except Exception as e:
        logger.error(f"Fehler beim Senden der Aktivierungs-E-Mail: {str(e)}")
