from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailService:
    @staticmethod
    def send_password_reset_email(user_email, reset_url):
        subject = 'Password Reset Request'
        html_message = render_to_string('resources/emails/password_reset.html', {
            'reset_url': reset_url
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message
        ) 