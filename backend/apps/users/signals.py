from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_delete, sender=UserProfile)
def delete_profile_avatar(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete(save=False)
