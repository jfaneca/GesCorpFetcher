import requests

from app.config import AppConfig
from app.db_client import DBClient
from app.gescorp_client import GescorpClient
from apscheduler.schedulers.blocking import BlockingScheduler

from app.logger import Logger
from app.orchestrator import Orchestrator
from app.sms_sender import SMSSender

logger = Logger()
app_logger = logger.get_logger()
app_config = AppConfig()
gescorp_client = GescorpClient(logger, app_config)
db_client = DBClient(logger)
sms_sender = SMSSender(logger=logger, api_url=app_config.sms_sender_url, user=app_config.sms_sender_usr, password=app_config.sms_sender_pwd)
orchestrator = Orchestrator(logger, app_config,gescorp_client, db_client, sms_sender)

def fetch_gescorp_alerts():
    orchestrator.notify_new_alerts()

# Initialize the scheduler
scheduler = BlockingScheduler()

# Add the job: Use the 'interval' trigger
scheduler.add_job(fetch_gescorp_alerts, 'interval', seconds=30, id='30_sec_job')

app_logger.info("Starting APScheduler (press Ctrl+C to exit)...")

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    # Shut down the scheduler gracefully when the user hits Ctrl+C
    scheduler.shutdown()
