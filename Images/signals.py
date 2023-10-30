from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance: Image, **kwargs):
    """This signal in responsible for keep ``total_likes`` field updated
    whenever a the users_like changed."""
    instance.total_likes = instance.users_like.count()
    instance.save()
