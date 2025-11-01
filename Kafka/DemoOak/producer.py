import json
import uuid

from confluent_kafka import Producer

producer_config = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(producer_config)
order = {
    "order_id": str(uuid.uuid4()),
    "user_name": "oak",
    "item": "Cake",
    "quantity": 1
}
order2 = {
    "order_id": str(uuid.uuid4()),
    "user_name": "oak 2",
    "item": "Coke",
    "quantity": 3
}
value = json.dumps(order).encode("utf-8")
value2 = json.dumps(order2).encode("utf-8")

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result."""
    if err:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} {}".format(msg.topic(), msg.value().decode("utf-8")))



producer.produce(
    topic="orders_topic",
    value=value,
    key=str(uuid.uuid4()),
    callback=delivery_report
)
producer.produce(
    topic="orders_topic",
    value=value2,
    key=str(uuid.uuid4()),
    callback=delivery_report
)

producer.flush()
