from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.utils.crypto import get_random_string
import os


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.is_counselor:
        temp_password = get_random_string(length=12)
        instance.set_password(temp_password)
        instance.save(update_fields=['password'])

        subject = 'Welcome to career guidance'
        message = (
            f'Hello {instance.username},\n\n'
            f'Your counselor account has been created successfully.\n'
            f'Please log in and change your password as soon as possible.\n'
            f'login url: {os.getenv("COUNSELOR_LOGIN_URL")}\n'
            f'Your email: {instance.email}\n\n'
            f'Your temporary password is: {temp_password}\n'
            f'Thank you for registering as a counselor!'
        )
        from_email = os.environ.get('EMAIL_HOST_USER')
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)

# post_save.connect(send_welcome_email, sender=User, dispatch_uid="create_counselor_profile")
