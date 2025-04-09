from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/profile_images/', default='images/profile_images/default.png',blank=True,null=True)
    bio = models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=30)
    @property
    def text_direction(self):
        if self.bio:
            stripped = self.bio.strip()
            if stripped:
                first_char = stripped[0]
                if '\u0600' <= first_char <= '\u06FF':
                    return "text-right"
        return "text-left"
class Follow(models.Model):
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
    created_at=models.DateTimeField(auto_now_add=True)

class Bookmark(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True ,related_name="likes")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="receiver"
    )
    sent = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="sent"
    )
    reply = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    