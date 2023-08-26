import requests
import json
from confluent_kafka import Producer


def get_and_save_weather_data():
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
            "bootstrap.servers": "localhost:9092",  # Replace with your Kafka broker details
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
