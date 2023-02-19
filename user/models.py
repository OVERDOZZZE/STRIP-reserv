from django.contrib.auth.models import AbstractUser
from django.db import models
# from django_auth.models import UserManager


# Create your models here.

class Avatar(models.Model):
    image = models.ImageField(upload_to='media/', null=True)


class CustomUser(AbstractUser):
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, null=True, related_name='avatar', blank=True)

    @property
    def get_image(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url
