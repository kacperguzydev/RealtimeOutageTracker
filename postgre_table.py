import psycopg2
from psycopg2 import sql
import config
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(__name__)

logger = setup_logger()

def create_database():
    """Creates the target PostgreSQL database if it does not exist."""
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database="postgres",
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (config.DB_NAME,))
        if cur.fetchone() is None:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config.DB_NAME)))
            logger.info("Database '%s' created.", config.DB_NAME)
        else:
            logger.info("Database '%s' already exists.", config.DB_NAME)
        cur.close()
        conn.close()
    except Exception as e:
        logger.error("Failed to create database: %s", e)
        raise

def get_connection():
    """Returns a connection to the target PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        logger.info("Connected to database '%s'.", config.DB_NAME)
        return conn
    except Exception as e:
        logger.error("Error connecting to PostgreSQL: %s", e)
        raise

def create_tables():
    """Creates the reddit_outage_summary table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reddit_outage_summary (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ,
                service VARCHAR(50),
                count INTEGER
            );
        """)
        conn.commit()
        logger.info("Table 'reddit_outage_summary' is set up.")
    except Exception as e:
        conn.rollback()
        logger.error("Error creating table: %s", e)
    finally:
        cur.close()
        conn.close()