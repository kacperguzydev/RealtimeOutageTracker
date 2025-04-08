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

## Getting Started

### Running with Docker

When running in Docker, use these settings in **config.py** so your containers communicate correctly:

```python
DB_HOST = os.getenv("DB_HOST", "postgres")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "host.docker.internal:9092")
Steps:
Clone the Repository:

bash
Copy
git clone https://github.com/kacperguzydev/RealtimeOutageTracker.git
cd RealtimeOutageTracker
Configure Kafka on Your Host (if not containerized):

In your Kafka broker’s server.properties (typically in C:\kafka_all\kafka\config\server.properties), ensure you have:

properties
Copy
listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT://localhost:9092
auto.create.topics.enable=true
Start Zookeeper and Kafka:

batch
Copy
C:\kafka_all\kafka\bin\windows\zookeeper-server-start.bat C:\kafka_all\kafka\config\zookeeper.properties
C:\kafka_all\kafka\bin\windows\kafka-server-start.bat C:\kafka_all\kafka\config\server.properties
Build and Run Docker Containers:

From the project directory, run:

bash
Copy
docker-compose up --build
The following containers will start:

PostgreSQL: Exposed on port 5432.

Main App: Runs main.py (includes a monitoring server on port 8000).

Spark Streaming: Processes Kafka messages and writes to PostgreSQL.

Streamlit App: Dashboard available at port 8501.

Starting Components:

Although Docker Compose starts everything concurrently, note the following startup details:

Streamlit: Access the dashboard at http://localhost:8501.

Monitoring (Prometheus Metrics): Available at http://localhost:8000.

If needed, you can start services individually:

Start Streamlit:

bash
Copy
docker-compose up streamlit_app
Start Spark Streaming:

bash
Copy
docker-compose up spark_streaming
Start Main App:

bash
Copy
docker-compose up main_app
Running Locally (Without Docker)
If you run the application directly on your host:

Update config.py:

python
Copy
DB_HOST = os.getenv("DB_HOST", "localhost")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
Ensure your local PostgreSQL and Kafka brokers are running.

Run each component in separate terminals:

Streamlit Dashboard:

bash
Copy
streamlit run streamlit_app.py --server.enableCORS false
Spark Streaming:

bash
Copy
python spark_streaming.py
Main App:

bash
Copy
python main.py
Troubleshooting
Kafka Topic Creation:
If the reddit_outage_topic isn’t auto-created, manually create it with:

batch
Copy
kafka-topics.bat --create --topic reddit_outage_topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
Spark Data Loss:
If Spark reports data loss (offset changes), set the Kafka option failOnDataLoss to "false" in spark_streaming.py.

Docker Networking:
Remember: Inside Docker, localhost refers to the container. Use host.docker.internal:9092 to connect to your host’s Kafka broker.
