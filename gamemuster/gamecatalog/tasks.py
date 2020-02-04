from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from django.core.management import call_command


logger = get_task_logger(__name__)


# executes daily at midnight
@periodic_task(run_every=(crontab(minute=0, hour=0)))
def load_games():
    logger.info('Start load_games task')

    call_command('loadgames')

    logger.info('Games information loaded')
