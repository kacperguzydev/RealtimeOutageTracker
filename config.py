import os

reddit_config = {
    "client_id": "qFqu8QQ9LRvZeL-Zhts0WA",
    "client_secret": "fEVymX51_1JdqUeaeAWYbwUvWz7jnQ",
    "user_agent": "OutageScope by u/Secure-Resident5712"
}

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "outrage")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "reddit_outage_topic")

JDBC_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
JDBC_PROPERTIES = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "driver": "org.postgresql.Driver"
}
