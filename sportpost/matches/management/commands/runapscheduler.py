import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime
from matches.models import Team,Match



logger = logging.getLogger(__name__)


def my_job():
  try:
    games = scoreboard.ScoreBoard()
    for game in games.games.data:
      
      game_id=game.get("gameId")
      short_name_home=game.get("homeTeam").get("teamTricode")
      short_name_away=game.get("awayTeam").get("teamTricode")
      team_id_home=game.get("homeTeam").get("teamId")
      team_id_away=game.get("awayTeam").get("teamId")
      home_team_name=game.get("homeTeam").get("teamName")
      away_team_name=game.get("awayTeam").get("teamName")
      if home_team_name=="Timberwolves":
        home_team_name="Wolves"
      if away_team_name=="Timberwolves":
        away_team_name="Wolves"
      home_team_logo=f"images/team_logo/{home_team_name}.svg"
      away_team_logo=f"images/team_logo/{away_team_name}.svg"

      home_score=game.get("homeTeam").get("score")
      away_score=game.get("awayTeam").get("score")
      game_time_utc=game.get("gameTimeUTC")
      game_time_utc_fixed = game_time_utc.replace("Z", "+00:00")
      dt_utc = datetime.fromisoformat(game_time_utc_fixed)
      date=dt_utc.date()
      time=dt_utc.time()
      game_clock=game.get("gameClock")
      game_status=game.get("gameStatusText")
      home_team,_=Team.objects.get_or_create(name=home_team_name,team_id=team_id_home,short_name=short_name_home,logo=home_team_logo)
      away_team,_=Team.objects.get_or_create(name=away_team_name,team_id=team_id_away,short_name=short_name_away,logo=away_team_logo)
      Match.objects.update_or_create(
        game_id=game_id,
        defaults={
          "home_team":home_team,
          "away_team":away_team,
          "home_score":home_score,
          "away_score":away_score,
          "date":date,
          "time":time,
          "game_clock":game_clock,
          "game_status":game_status,


        }
      )





  except Exception as e:
    print(e)
def delete_old_job_executions(max_age=604_800):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
      my_job,
      trigger=CronTrigger(second="*/15"),  # Every 10 seconds
      id="my_job",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True,
    )
    logger.info("Added job 'my_job'.")

    scheduler.add_job(
      delete_old_job_executions,
      trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
      ),  # Midnight on Monday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")