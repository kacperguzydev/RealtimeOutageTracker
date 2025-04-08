from prometheus_client import start_http_server, Counter
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Prometheus metrics
outage_checks_total = Counter('outage_checks_total', 'Total number of outage checks processed')
outage_errors_total = Counter('outage_errors_total', 'Total number of errors during outage checks')

def start_monitoring_server(port=8000):
    """Starts an HTTP server to expose Prometheus metrics."""
    start_http_server(port)
    logger.info("Monitoring server started on port %d", port)

def record_success():
    """Increment the counter for successful outage checks."""
    outage_checks_total.inc()

def record_error():
    """Increment the counter for errors during outage checks."""
    outage_errors_total.inc()
