from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from content.models import Movie

@receiver(post_delete, sender=Movie)
def delete_movie_files(sender, instance, **kwargs):
    instance.video.delete()