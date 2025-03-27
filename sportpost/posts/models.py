from django.db import models, IntegrityError
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
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

    class Meta:
        # Enforce that a user can repost a given post only once.
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'repost_of'],
                name='unique_repost',
                condition=models.Q(repost_of__isnull=False)
            )
        ]
