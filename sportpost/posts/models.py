from django.db import models, IntegrityError
from django.contrib.auth.models import User
from matches.models import Match
from django.utils import timezone
from crum import get_current_request
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image=models.ImageField(null=True,blank=True,upload_to="images/posts_images")
    created_at = models.DateTimeField(auto_now_add=True)
    game=models.ForeignKey(Match,on_delete=models.CASCADE,related_name="game",null=True,blank=True)
    parent_post = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name="replies", 
        on_delete=models.CASCADE
    )
    repost_of = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='retweets',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"self:{self.user.username}"

    @property
    def text_direction(self):
        """
        Returns 'text-right' if the first non-whitespace character
        is an Arabic character, otherwise 'text-left'.
        """
        if self.content:
            stripped = self.content.strip()
            if stripped:
                first_char = stripped[0]
                if '\u0600' <= first_char <= '\u06FF':
                    return "text-right"
        return "text-left"
    @property
    def time_since(self):
       
        now = timezone.now()
        diff = now - self.created_at
        seconds = diff.total_seconds()

        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}m"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours}h"
        else:
            days = int(seconds / 86400)
            return f"{days}d"
    @property
    def is_repost_bookmarked(self):
        from accounts.models import Bookmark
        user = get_current_request().user
        if user.is_authenticated:
            target = self.repost_of if self.repost_of else self
            return Bookmark.objects.filter(user=user, post=target).exists()
        return False
    @property
    def is_repost_liked(self):
        from accounts.models import Like
        user = get_current_request().user
        if user.is_authenticated:
            target = self.repost_of if self.repost_of else self
            return Like.objects.filter(user=user, post=target).exists()
        return False