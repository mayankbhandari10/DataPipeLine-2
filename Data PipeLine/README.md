
### GitHub Link
https://github.com/mayankbhandari10/DataPipeLine-2/tree/master


# Data Pipeline for Weather Data

This project is a data pipeline that extracts weather data from an external API, saves it to a JSON file, and publishes it to a Kafka topic.

## Getting Started

These instructions will help you set up and run the data pipeline on your local machine.

### Prerequisites

You will need the following software installed on your machine:

- Python 3.x
- Apache Kafka (Make sure the Kafka broker is running on `localhost:9092`)

### Kafka Setup

1. Download and extract Apache Kafka from the official website.
2. Open a terminal and navigate to the Kafka directory.
3. Start the ZooKeeper server:

   ```sh
   bin/zookeeper-server-start.sh config/zookeeper.properties

### Start the Kafka server:
bin/kafka-server-start.sh config/server.properties

### Create a Kafka topic for weather data:
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic weather-data-topic


#### Installing Dependencies
pip install -r requirements.txt

### Running the Data Pipeline

1) Make sure your Kafka broker is running on localhost:9092.

2) Run the data pipeline script by executing the following command:
- python DataExtract.py

This script will:

Make an API request to fetch weather data.
Save the weather data to a JSON file named weather_data.json.
Publish the weather data to the Kafka topic weather-data-topic.

### Running Unit Tests
python -m unittest discover tests


