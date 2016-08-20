from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Post(models.Model):
    #author = models.ForeignKey('auth.User')
    tweetContent = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200,default='')
    sent = models.CharField(max_length=200,default='')
    bad = models.CharField(max_length=200,default='')

    def __str__(self):
        return self.tweetContent


class blacklist(models.Model):
    #author = models.ForeignKey('auth.User')
    tweetContent = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.tweetContent