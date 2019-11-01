from django.db import models
from django.utils import timezone

from accounts.models import User
# Create your models here.

# :TODO:
# 1. Update the password every time the key is updated.
# 2. "Show Password" button on the admin page.


class PasswordVault(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.username

    @property
    def encrypt(self):
        encrypted = []
        user_defined_key = self.user.key_set.all().order_by('-updated_at').first()
        key = user_defined_key.key if user_defined_key else " "

        for i, c in enumerate(self.password):
            key_c = ord(key[i % len(key)])
            msg_c = ord(c)
            encrypted.append(chr((msg_c + key_c) % 127))
        return ''.join(encrypted)

    def save(self, *args, **kwargs):
        # On save, update timestamps and encrypt password
        self.updated_at = timezone.now()
        self.password = self.encrypt

        return super(PasswordVault, self).save(*args, **kwargs)

    @property
    def decrypt(self):
        msg = []
        user_defined_key = self.user.key_set.all().first()
        key = user_defined_key.key if user_defined_key else " "

        for i, c in enumerate(self.password):
            key_c = ord(key[i % len(key)])
            enc_c = ord(c)
            msg.append(chr((enc_c - key_c) % 127))
        return ''.join(msg)


class Key(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    previous_key = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # On save, update timestamps and encrypt password
        self.updated_at = timezone.now()
        return super(Key, self).save(*args, **kwargs)
