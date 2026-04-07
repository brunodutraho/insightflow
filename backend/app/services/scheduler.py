from apscheduler.schedulers.background import BackgroundScheduler
from app.services.collector import run_collector
import logging

logger = logging.getLogger("app")

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Added collection task
    # 1-minute 'interval' for testing now, in production it would be 'hours=1'
    #scheduler.add_job(
     #   run_collector, 
      #  "interval", 
       # minutes=1, 
        #id="collector_job",
        #replace_existing=True
    #)
    
    scheduler.start()
    logger.info("Scheduler started: Data collection running every 1 minute.")
