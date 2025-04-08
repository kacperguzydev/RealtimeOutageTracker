import time
import logging
from datetime import datetime

from postgre_table import create_database, create_tables
from kafka_producer import produce_outage_summary
from reddit_monitor import RedditMonitor
import config
from monitoring import start_monitoring_server, record_success, record_error

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def perform_outage_check():
    """Check for service outages and send the summary to Kafka."""
    # Ensure our database and table are available.
    create_database()
    create_tables()

    services = [
        "instagram", "facebook", "whatsapp", "youtube",
        "twitter", "snapchat", "tiktok", "netflix",
        "discord", "amazon"
    ]

    reddit_monitor = RedditMonitor(
        client_id=config.reddit_config["client_id"],
        client_secret=config.reddit_config["client_secret"],
        user_agent=config.reddit_config["user_agent"]
    )

    current_time = datetime.utcnow().isoformat()
    summary_list = []
    print(f"\nOutage Check at {current_time} UTC\n")

    for service in services:
        search_phrase = f"{service} down OR {service} not working"
        try:
            results = reddit_monitor.search_outage_mentions(search_phrase)
            count = len(results)
            print(f"{service.capitalize()}: {count} posts")
            summary_list.append({
                "timestamp": current_time,
                "service": service,
                "count": count
            })
        except Exception as err:
            logger.error("Error checking %s: %s", service, err)

    produce_outage_summary(summary_list)
    print("\nSummary sent to Kafka.\n")


if __name__ == "__main__":
    start_monitoring_server(8000)  # Expose metrics on port 8000
    while True:
        try:
            perform_outage_check()
            record_success()
        except Exception as e:
            record_error()
            logger.error("Outage check failed: %s", e)
        time.sleep(3600)
