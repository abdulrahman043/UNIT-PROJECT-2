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
import datetime

import requests


logger = logging.getLogger(__name__)


def my_job():

    url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Navigate JSON structure:
        league_schedule = data.get("leagueSchedule", {})
        game_dates = league_schedule.get("gameDates", [])
        for date_entry in game_dates:
            # date_entry might be like: {"gameDate": "10/04/2024 00:00:00", "games": [ ... ]}
            date_str = date_entry.get("gameDate")
            try:
                # Assuming the date is in "MM/DD/YYYY HH:MM:SS" format:
                dt = datetime.datetime.strptime(date_str, "%m/%d/%Y %H:%M:%S")
                game_date = dt.date()
            except Exception as e:
                logger.error("Error parsing date '%s': %s", date_str, e)
                continue

            for game in date_entry.get("games", []):
                game_id = game.get("gameId")
                # Extract team info:
                home_info = game.get("homeTeam", {})
                away_info = game.get("awayTeam", {})
                home_team_name = home_info.get("teamName")
                away_team_name = away_info.get("teamName")
                if home_team_name == "Timberwolves":
                    home_team_name = "Wolves"
                if away_team_name == "Timberwolves":
                    away_team_name = "Wolves"
                home_team_logo = f"images/team_logo/{home_team_name}.svg"
                away_team_logo = f"images/team_logo/{away_team_name}.svg"
                team_id_home = home_info.get("teamId")
                team_id_away = away_info.get("teamId")
                short_name_home = home_info.get("teamTricode")
                short_name_away = away_info.get("teamTricode")
                home_score = int(home_info.get("score") or 0)
                away_score = int(away_info.get("score") or 0)

                # Game time - here we use gameTimeUTC
                game_time_utc = game.get("gameTimeUTC")
                if game_time_utc:
                    try:
                        # Convert to ISO format:
                        game_time_utc_fixed = game_time_utc.replace("Z", "+00:00")
                        dt_utc = datetime.datetime.fromisoformat(game_time_utc_fixed)
                        game_time = dt_utc.time()
                    except Exception as e:
                        logger.error("Error parsing game time '%s': %s", game_time_utc, e)
                        game_time = datetime.time(0, 0)
                else:
                    game_time = datetime.time(0, 0)

                game_status = game.get("gameStatusText", "")
                game_clock = game.get("gameClock", "")

                # Update teams:
                home_team, _ = Team.objects.get_or_create(
                    team_id=team_id_home,
                    defaults={
                        "name": home_team_name,
                        "short_name": short_name_home,
                        "logo": home_team_logo,
                    }
                )
                away_team, _ = Team.objects.get_or_create(
                    team_id=team_id_away,
                    defaults={
                        "name": away_team_name,
                        "short_name": short_name_away,
                        "logo": away_team_logo,
                    }
                )
                # Update or create the match:
                Match.objects.update_or_create(
                    game_id=game_id,
                    defaults={
                        "home_team": home_team,
                        "away_team": away_team,
                        "home_score": home_score,
                        "away_score": away_score,
                        "date": game_date,
                        "time": game_time,
                        "game_clock": game_clock,
                        "game_status": game_status,
                        "last_updated": datetime.datetime.now(),
                    }
                )
                logger.info("Updated match %s on %s at %s", game_id, game_date, game_time)
    except Exception as e:
        logger.error("Error updating full schedule: %s", e)
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