from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


# signals
@receiver(post_save,sender=User)
def user_signal(sender, instance=None, created=False, **kwargs):
    if created:
        print("Profile created")
    else:
        print("Profile Updated")

    print(instance.username)