from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

import os

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell"

# Create a Spark session
spark = SparkSession.builder.appName("KafkaJSONProcessing").getOrCreate()

# Define Kafka parameters
kafka_params = {
    "kafka.bootstrap.servers": "localhost:9092",  # Kafka broker address
    "subscribe": "weather-data-topic",  # Kafka topic to subscribe to
    "startingOffsets": "earliest",
}

# Define the schema for the JSON data
json_schema = StructType(
    [
        StructField("city", StringType(), True),
        StructField("temperature", IntegerType(), True),
    ]
)

# Read data from Kafka topic as a DataFrame
kafka_df = spark.readStream.format("kafka").options(**kafka_params).load()

# Parse the JSON data and select fields
parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")
parsed_df = parsed_df.select(from_json("json_str", json_schema).alias("data")).select(
    "data.*"
)

# Perform any processing you need on the parsed_df DataFrame
# For example, you can calculate statistics or filter data based on conditions

# Display the processed data in the console
query = parsed_df.writeStream.outputMode("append").format("console").start()
print(query.status)


# Await termination
query.awaitTermination()

# Stop the Spark session
spark.stop()
