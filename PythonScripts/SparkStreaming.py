from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, size
import os

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell"

# Create a Spark session
spark = SparkSession.builder.appName("KafkaWordCount").getOrCreate()

# Define Kafka parameters
kafka_params = {
    "kafka.bootstrap.servers": "localhost:9092",  # Kafka broker address
    "subscribe": "weather-data-topic",  # Kafka topic to subscribe to
    "startingOffsets": "earliest",
}

# Read data from Kafka topic as a DataFrame
kafka_df = spark.readStream.format("kafka").options(**kafka_params).load()

# Convert value column to string
kafka_df = kafka_df.selectExpr("CAST(value AS STRING) as record")

# Split the record into words and calculate the number of words
word_count_df = kafka_df.select(size(split(col("record"), " ")).alias("word_count"))

# Display the word count in the console
query = word_count_df.writeStream.outputMode("append").format("console").start()
print(query.status)

# Await termination
query.awaitTermination()

# Stop the Spark session
spark.stop()
