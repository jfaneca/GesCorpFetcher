import logging
import logging.handlers

# --- Configuration ---
LOG_FILENAME = 'gescorp_fetcher.log'
# When to rotate: 'midnight' (default) or 'H', 'M', 'S', 'D', 'W0'-'W6'
WHEN = 'midnight'
# The interval of rotation (e.g., 1 for daily, 7 for weekly if WHEN='D')
INTERVAL = 1
# The number of backup files to keep (e.g., 5 means the current day + 5 previous days)
BACKUP_COUNT = 30
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

class Logger:
    def __init__(self):
        # --- Setup Logger ---
        self.logger = logging.getLogger('MyDailyRotator')
        self.logger.setLevel(logging.INFO)

        # Create a formatter
        formatter = logging.Formatter(LOG_FORMAT)

        # Create a handler for daily rotation
        # 'D' means rotation happens every day, and at 'midnight' it rotates
        handler = logging.handlers.TimedRotatingFileHandler(
            filename=LOG_FILENAME,
            when=WHEN,
            interval=INTERVAL,
            backupCount=BACKUP_COUNT,
            encoding='utf-8',
            # suffix: The file name suffix is determined by strftime() applied to the time of rotation.
            # The default is "%Y-%m-%d" (e.g., mylog.log.2025-10-04) for daily rotation.
        )

        # Set the formatter for the handler
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger