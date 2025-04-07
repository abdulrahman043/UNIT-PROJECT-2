from django.db import models, IntegrityError
from django.contrib.auth.models import User
from matches.models import Match
from django.utils import timezone
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
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
 