import json
import time
import uuid
import random
from datetime import datetime

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

USERS = ["user_1", "user_2", "user_3"]
EVENT_TYPES = ["click", "purchase"]


def generate_event() -> dict:
    event_type = random.choice(EVENT_TYPES)

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "user_id": random.choice(USERS),
        "timestamp": datetime.utcnow().isoformat(),
    }

    if event_type == "purchase":
        event["amount"] = round(random.uniform(5, 50), 2)

    return event


if __name__ == "__main__":
    print("Producer running...")

    while True:
        event = generate_event()
        producer.send("user-events", value=event)
        print("Sent:", event)
        time.sleep(1)
