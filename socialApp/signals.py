from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

# Signals allow you to attach code to certain events in Django, such as the creation of a new user from google
# What it does is listen to the post_save signal that is fired every time a User object is saved. When a new user is created (created=True), a UserProfile instance associated with that user is automatically created

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
