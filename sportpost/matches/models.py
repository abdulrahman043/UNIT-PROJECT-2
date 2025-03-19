from django.db import models

# Create your models here.
class Match(models.Model):
    game_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"