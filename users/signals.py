from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

'''
Automatically create a user profile after a user has been created.
The signal will be fired once the user is created.
Otherwise we need to manually add the profile in the admin page, which is a nightmare.
'''

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()