from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Chingu(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    custom_username = models.CharField(max_length=20)
    avatar          = models.ImageField(null=True, blank=True)
    bio             = models.TextField()
    birthday        = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
     


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Chingu.objects.create(user=instance)
        profile.save()
