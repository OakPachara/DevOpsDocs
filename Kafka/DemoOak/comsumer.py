import json
from confluent_kafka import Consumer, KafkaError

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'oak_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)

consumer.subscribe(['orders_topic'])

print("Consuming messages from 'orders_topic'...")

try:
    while True:
        msg = consumer.poll(1.0)  # Timeout of 1 second

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print("Error while consuming message: {}".format(msg.error()))
                break

        print("Received message: Key: {}, Value: {}".format(msg.key().decode('utf-8'), msg.value().decode('utf-8')))
except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()
