import streamlit as st
import pandas as pd
import psycopg2
import config
import logging

# Configure logging in a straightforward style.
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("dashboard")


@st.cache_data
def fetch_outage_data():
    """
    Connect to PostgreSQL and retrieve outage records.
    Returns a DataFrame with the outage data.
    """
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        query = """
        SELECT id, timestamp, service, count
        FROM reddit_outage_summary
        ORDER BY timestamp DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        logger.info("Outage data retrieved successfully.")
        return df
    except Exception as e:
        logger.error("Error fetching outage data: %s", e)
        return pd.DataFrame()


# Set up page title and layout.
st.set_page_config(page_title="Reddit Outage Dashboard", layout="wide")
st.title("Reddit Outage Dashboard")
st.write("This dashboard displays service outage data over time.")

# Get the data from the database.
data = fetch_outage_data()

if data.empty:
    st.warning("No outage data found. Please check back later.")
else:
    # Convert the timestamp field from string to datetime.
    data["timestamp"] = pd.to_datetime(data["timestamp"])

    st.subheader("Raw Outage Data")
    st.dataframe(data)

    # Allow filtering by service.
    services = sorted(data["service"].unique())
    selected = st.multiselect("Select services:", services, default=services)
    filtered = data[data["service"].isin(selected)]

    st.subheader("Outage Trend Over Time")
    # Plot a line chart with outage counts over time.
    chart_data = filtered.set_index("timestamp")[["count"]]
    st.line_chart(chart_data)

    st.subheader("Total Outages per Service")
    # Group data by service for a summary view.
    summary = filtered.groupby("service", as_index=False)["count"].sum().set_index("service")
    st.bar_chart(summary)
