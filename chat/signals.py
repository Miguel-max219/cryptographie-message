from django.db.models.signals import post_save
from django.dispatch import receiver
from Crypto.Random import get_random_bytes
import base64
from .models import Room, EncryptionKey 

@receiver(post_save, sender=Room)
def create_encryption_key(sender, instance, created, **kwargs):
    if created:
        key = base64.urlsafe_b64encode(get_random_bytes(32)).decode()
        EncryptionKey.objects.create(room=instance, key=key)
