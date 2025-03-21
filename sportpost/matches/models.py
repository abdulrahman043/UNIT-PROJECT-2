from django.db import models

# Create your models here.
class Team(models.Model):
    team_id=models.CharField(max_length=100, unique=True, blank=True, null=True)
    name=models.CharField(max_length=50,unique=True)
    leauge=models.CharField(max_length=6,null=True,blank=True)
    short_name=models.CharField(max_length=100, unique=True, blank=True, null=True)
    logo = models.ImageField(
    upload_to='images/team_logo/',
    default='images/team_logo/default.png',
    blank=True,
    null=True
    )
class Match(models.Model):
    game_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    home_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='home_matches')
    away_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='away_matches')
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    date=models.DateField()
    time=models.TimeField()
    last_updated = models.DateTimeField(auto_now_add=True)
    game_status= models.CharField(max_length=100,  blank=True, null=True)
    game_clock=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"