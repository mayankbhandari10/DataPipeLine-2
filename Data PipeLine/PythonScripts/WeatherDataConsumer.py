from confluent_kafka import Consumer, KafkaError


def consume_weather_data():
    consumer_conf = {
        "bootstrap.servers": "localhost:9092",  # Replace with your Kafka broker details
        "group.id": "weather-data-group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(["weather-data-topic"])

    print("*********************Consumer process started.**************************\n")

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
