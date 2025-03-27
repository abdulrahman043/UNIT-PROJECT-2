from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
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
    created_at=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=30)
    @property
    def text_direction(self):
        """
        Returns 'text-right' if the first non-whitespace character
        is an Arabic character, otherwise 'text-left'.
        """
        if self.bio:
            stripped = self.bio.strip()
            if stripped:
                first_char = stripped[0]
                # Arabic Unicode block range: 0600 to 06FF
                if '\u0600' <= first_char <= '\u06FF':
                    return "text-right"
        return "text-left"

class Bookmark(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

