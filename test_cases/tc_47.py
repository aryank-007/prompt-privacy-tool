# Logging setup — no secrets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_event(event):
    logger.info("Event received: " + str(event))
