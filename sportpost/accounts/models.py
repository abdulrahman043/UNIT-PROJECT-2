from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
    upload_to='images/profile_images/',
    default='images/profile_images/default.png',
    blank=True,
    null=True
    )
    bio = models.TextField(blank=True)
