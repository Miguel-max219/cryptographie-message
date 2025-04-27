from django.db import models
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import re
from django.conf import settings
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=2000)

def is_base64(s):
    return bool(re.fullmatch(r'^[A-Za-z0-9+/]+={0,2}$', s))

class Message(models.Model):
    value = models.TextField()
    user = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    iv = models.CharField(max_length=255, default='valeurpardefaut')

    def get_key(self):
        try:
            return EncryptionKey.objects.get(room=self.room).key[:32].encode('utf-8')
        except EncryptionKey.DoesNotExist:
            return settings.SECRET_KEY[:32].encode('utf-8')

    def pad(self, s):
        return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    def unpad(self, s):
        return s[:-ord(s[-1])]

    def encrypt(self, plaintext, iv):
        key = self.get_key()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = self.pad(plaintext).encode('utf-8')
        ciphertext = cipher.encrypt(padded)
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext, iv):
        if not is_base64(iv):
            return '[IV invalide]'
        try:
            iv_bytes = base64.b64decode(iv)
            key = self.get_key()
            cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
            decoded = base64.b64decode(ciphertext)
            plaintext = cipher.decrypt(decoded)
            return self.unpad(plaintext.decode('utf-8'))
        except Exception as e:
            return f'[Erreur de déchiffrement : {e}]'

    def save(self, *args, **kwargs):
        iv = get_random_bytes(16)
        self.iv = base64.b64encode(iv).decode('utf-8')
        self.value = self.encrypt(self.value, iv)
        self.user = self.encrypt(self.user, iv)
        super().save(*args, **kwargs)

    def get_decrypted(self):
        try:
            decrypted_value = self.decrypt(self.value, self.iv)
            decrypted_user = self.decrypt(self.user, self.iv)
        except Exception as e:
            decrypted_value = f"[Erreur de déchiffrement: {e}]"
            decrypted_user = f"[Erreur de déchiffrement: {e}]"

        return {
            'user': decrypted_user,
            'value': decrypted_value,
            'date': timezone.localtime(self.date).strftime('%Y-%m-%d %H:%M:%S'),
        }
class EncryptionKey(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Clé pour la salle {self.room.name}"