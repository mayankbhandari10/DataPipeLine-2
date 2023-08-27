provider "aws" {
  region = "us-east-1"  
}

resource "aws_instance" "kafka_instance" {
  ami           = "ami-0c55b159cbfafe1f0" 
  instance_type = "t2.micro"

  user_data = <<-EOF
#!/bin/bash
apt-get update
apt-get install -y python3-pip

# Install necessary Python packages
pip3 install requests
pip3 install confluent-kafka

# Copy the producer and consumer scripts to the instance
cat <<EOF > /home/ubuntu/producer.py
def get_and_save_weather_data():
    import requests
    import json
    from confluent_kafka import Producer

    headers = {
        "X-RapidAPI-Key": "12699d00bamshf3eb9effd15ea3ap11fac2jsn392eb7d52978",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
    }

    params = {"q": "53.1,-0.13"}

    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        weather_data = response.json()

        # Save data to a JSON file
        with open("weather_data.json", "w") as f:
            json.dump(weather_data, f, indent=4)  # indent for pretty formatting

        # Publish data to Kafka topic
        kafka_conf = {
            "bootstrap.servers": "localhost:9092",  
        }
        kafka_topic = "weather-data-topic"

        producer = Producer(kafka_conf)
        producer.produce(
            kafka_topic, key="weather-data", value=json.dumps(weather_data)
        )
        producer.flush()

        print("Weather data saved to weather_data.json and published to Kafka")
    else:
        print("Request failed with status code:", response.status_code)


# Call the function to get, save, and publish weather data
get_and_save_weather_data()
EOF

cat <<EOF > /home/ubuntu/consumer.py
def consume_weather_data():
    from confluent_kafka import Consumer, KafkaError

    consumer_conf = {
        "bootstrap.servers": "localhost:9092",  # Replace with your Kafka broker details
        "group.id": "weather-data-group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(["weather-data-topic"])

    print("*********************Consumer process started.**************************\\n")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
            else:
                print("Received message: {}".format(msg.value().decode("utf-8")))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print(
            "*********************** Consumer process finished.****************************"
        )


if __name__ == "__main__":
    consume_weather_data()
EOF

# Run the producer and consumer scripts
python3 /home/ubuntu/producer.py &
python3 /home/ubuntu/consumer.py &
EOF

  tags = {
    Name = "KafkaInstance"
  }
}
