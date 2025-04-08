# RealtimeOutageTracker

RealtimeOutageTracker is a real-time data pipeline that monitors service outages by scraping Reddit, pushing outage data through Kafka, processing it with Spark Streaming, storing results in PostgreSQL, and visualizing trends in a Streamlit dashboard. Prometheus is used to expose basic metrics (e.g., total checks and errors).

## Features

- **Reddit Monitoring:** Searches for posts mentioning outages (e.g., "down" or "not working") for multiple services.
- **Kafka Integration:** Sends collected outage data to Kafka.
- **Spark Streaming:** Reads messages from Kafka, deduplicates data, and writes processed results to PostgreSQL.
- **PostgreSQL Storage:** Saves outage records for historical analysis.
- **Streamlit Dashboard:** Visualizes outage trends and service summaries.
- **Prometheus Monitoring:** Exposes metrics via an HTTP endpoint.

## Technologies Used

- Python 3.11
- Apache Kafka (using kafka-python)
- Apache Spark (PySpark)
- PostgreSQL
- Streamlit
- Prometheus Client
- Docker & Docker Compose

## Project Structure

- **main.py** – Coordinates outage checks, database setup, and sends outage data to Kafka.
- **kafka_producer.py** – Contains the Kafka producer implementation.
- **reddit_monitor.py** – Searches Reddit for service outage mentions.
- **spark_streaming.py** – Reads messages from Kafka, processes them with Spark, and writes results to PostgreSQL.
- **streamlit_app.py** – Runs the Streamlit dashboard to display outage trends.
- **postgre_table.py** – Manages PostgreSQL database and table creation.
- **config.py** – Stores configuration settings for Reddit, Kafka, and PostgreSQL.
- **monitoring.py** – Exposes Prometheus metrics via an HTTP server.
- **wait-for-it.sh** – Bash script (used in Docker) to wait until PostgreSQL is ready.
- **requirements.txt** – Lists Python dependencies.
- **Dockerfile** – Builds the application image.
- **docker-compose.yml** – Starts all containers (PostgreSQL, main app, Spark Streaming, and Streamlit).

## How to Start

### Using Docker

When running in Docker, the configuration is set to let your containers communicate over the Docker network. In **config.py** the following settings are used:

- `DB_HOST` is set to `"postgres"` (the service name defined in docker-compose)  
- `KAFKA_BROKER` is set to `"host.docker.internal:9092"` (so containers can reach Kafka running on your host)

#### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/kacperguzydev/RealtimeOutageTracker.git
   cd RealtimeOutageTracker
Ensure Kafka is Running on Your Host

Verify your Kafka broker is running using your Windows scripts:

batch
Copy
C:\kafka_all\kafka\bin\windows\zookeeper-server-start.bat C:\kafka_all\kafka\config\zookeeper.properties
C:\kafka_all\kafka\bin\windows\kafka-server-start.bat C:\kafka_all\kafka\config\server.properties
Your broker’s server.properties should have:

properties
Copy
listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT://localhost:9092
auto.create.topics.enable=true
Build and Start Docker Containers

In the project directory, run:

bash
Copy
docker-compose up --build
This command will build the images and run the following containers:

PostgreSQL: Accessible on port 5432.

Main App: Runs main.py (and starts a monitoring server on port 8000).

Spark Streaming: Processes data from Kafka and writes to PostgreSQL.

Streamlit App: Accessible on port 8501 (the dashboard).

Access the Running Services

Streamlit Dashboard: http://localhost:8501

Monitoring Metrics: http://localhost:8000

Note: Docker Compose starts all services concurrently. If you need to restart individual services, use:

bash
Copy
docker-compose up streamlit_app
docker-compose up spark_streaming
docker-compose up main_app
Running Locally (Without Docker)
If you choose to run the project directly on your host machine:

Update config.py to use localhost:

python
Copy
DB_HOST = os.getenv("DB_HOST", "localhost")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
Start PostgreSQL and Kafka Locally

Ensure both services are running on your machine (using your usual startup scripts).

Run the Application Components in Order

Open three separate terminal windows:

Start the Streamlit Dashboard:

bash
Copy
streamlit run streamlit_app.py --server.enableCORS false
Start Spark Streaming:

bash
Copy
python spark_streaming.py
Start the Main App:

bash
Copy
python main.py
Troubleshooting
Kafka Topic Auto-Creation:

If reddit_outage_topic isn’t created automatically, manually create it using:

batch
Copy
kafka-topics.bat --create --topic reddit_outage_topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
Spark Data Loss Warning:

If Spark reports data loss due to changed offsets, consider setting the Kafka option failOnDataLoss to "false" in spark_streaming.py.

Docker Networking:

Remember that inside Docker containers, localhost refers to the container. When using Docker, the configuration uses DB_HOST=postgres for PostgreSQL and KAFKA_BROKER=host.docker.internal:9092 for Kafka.
