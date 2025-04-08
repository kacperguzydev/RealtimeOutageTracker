import os
os.environ["HADOOP_HOME"] = "C:\\hadoop"

import logging
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, TimestampType, StringType, IntegerType
import config

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(__name__)

logger = setup_logger()

def write_to_postgres(batch_df: DataFrame, batch_id: int) -> None:
    """Writes a deduplicated batch of data to PostgreSQL."""
    try:
        deduped_df = batch_df.dropDuplicates(["timestamp", "service"])
        row_count = deduped_df.count()
        deduped_df.write.mode("append").jdbc(
            url=config.JDBC_URL,
            table="reddit_outage_summary",
            properties=config.JDBC_PROPERTIES
        )
        logger.info("Batch %d written with %d unique rows.", batch_id, row_count)
    except Exception as exc:
        logger.error("Error writing batch %d: %s", batch_id, exc)

def main() -> None:
    spark = (
        SparkSession.builder.appName("RedditOutageToPostgre")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.postgresql:postgresql:42.2.18")
        .getOrCreate()
    )

    schema = StructType([
        StructField("timestamp", TimestampType(), True),
        StructField("service", StringType(), True),
        StructField("count", IntegerType(), True)
    ])

    # Added option "failOnDataLoss" to avoid failing if offsets change
    kafka_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", config.KAFKA_BROKER)
        .option("subscribe", config.KAFKA_TOPIC)
        .option("failOnDataLoss", "false")
        .load()
    )

    json_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")
    outage_df = json_df.select(F.from_json(F.col("json_str"), schema).alias("data")).select("data.*")

    query = (
        outage_df.writeStream.outputMode("append")
        .foreachBatch(write_to_postgres)
        .option("checkpointLocation", "/tmp/checkpoint_reddit_outage")
        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
