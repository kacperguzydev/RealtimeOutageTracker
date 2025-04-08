import json
import time
import logging
from kafka import KafkaProducer
import config

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(__name__)

logger = setup_logger()

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def key_serializer(key: str) -> bytes:
    return key.encode("utf-8")

def produce_outage_summary(summary_data):
    """Sends outage summary data to Kafka."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=config.KAFKA_BROKER,
            value_serializer=json_serializer,
            key_serializer=key_serializer
        )
    except Exception as exc:
        logger.error("Kafka producer initialization failed: %s", exc)
        return

    if not summary_data:
        logger.warning("No data to send to Kafka.")
        return

    logger.info("Sending %d records to Kafka.", len(summary_data))
    for record in summary_data:
        message_key = f"{record['service']}_{record['timestamp']}"
        try:
            producer.send(config.KAFKA_TOPIC, key=message_key, value=record)
            logger.info("Sent record: %s", message_key)
        except Exception as exc:
            logger.error("Error sending %s: %s", message_key, exc)
        time.sleep(0.1)

    try:
        producer.flush()
        logger.info("All Kafka messages flushed successfully.")
    except Exception as exc:
        logger.error("Error flushing Kafka producer: %s", exc)

if __name__ == "__main__":
    test_data = [
        {"timestamp": "2023-04-07T12:00:00", "service": "instagram", "count": 10},
        {"timestamp": "2023-04-07T12:00:00", "service": "facebook", "count": 5},
    ]
    produce_outage_summary(test_data)
