# RealtimeOutageTracker

RealtimeOutageTracker is a real-time data pipeline that monitors service outages by scraping Reddit, pushing outage data through Kafka, processing it with Spark Streaming, storing results in PostgreSQL, and visualizing trends in a Streamlit dashboard. Prometheus is also used to expose basic metrics.

## Features

- **Reddit Monitoring:** Searches for posts mentioning outages (e.g., "down" or "not working") for multiple services.
- **Kafka Integration:** Sends outage data to Kafka.
- **Spark Streaming:** Reads messages from Kafka, deduplicates data, and writes results to PostgreSQL.
- **PostgreSQL Storage:** Saves outage records for historical analysis.
- **Streamlit Dashboard:** Visualizes outage trends and service summaries.
- **Prometheus Monitoring:** Exposes metrics such as total checks and errors on an HTTP endpoint.

## Technologies Used

- Python 3.11
- Apache Kafka (using kafka-python)
- Apache Spark (PySpark)
- PostgreSQL
- Streamlit
- Prometheus Client
- Docker & Docker Compose

## Project Structure

- `main.py` – Coordinates outage checks, database setup, and sending outage data to Kafka.
- `kafka_producer.py` – Implements the Kafka producer.
- `reddit_monitor.py` – Searches Reddit for service outage mentions.
- `spark_streaming.py` – Reads messages from Kafka, processes them with Spark, and writes to PostgreSQL.
- `streamlit_app.py` – Runs the Streamlit dashboard to display outage trends.
- `postgre_table.py` – Manages PostgreSQL database and table creation.
- `config.py` – Stores configuration settings for Reddit, Kafka, and PostgreSQL.
- `monitoring.py` – Exposes Prometheus metrics.
- `wait-for-it.sh` – Bash script (used in Docker) to wait until PostgreSQL is ready.
- `requirements.txt` – Lists Python dependencies.
- `Dockerfile` – Builds the application image.
- `docker-compose.yml` – Starts all containers (PostgreSQL, main app, Spark streaming, and Streamlit).
