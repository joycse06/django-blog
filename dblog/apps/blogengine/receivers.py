from django.dispatch import receiver
from userena.signals import signup_complete


@receiver(signup_complete)
def handle_sign_up_complete(sender, **kwargs):
    user = kwargs['user']
    user.is_staff = True
    user.save()