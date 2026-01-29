import json
import redis
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


consumer = KafkaConsumer(
    "user-events",
    bootstrap_servers="localhost:9092",
    group_id="user-events-processor",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("Consumer running...")

admin = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
)

try:
    admin.create_topics(
        new_topics=[
            NewTopic(
                name="user-events-dlq",
                num_partitions=1,
                replication_factor=1,
            )
        ]
    )
    print("DLQ topic created")
except TopicAlreadyExistsError:
    pass


for msg in consumer:
    try:
        raw_value = msg.value.decode("utf-8")
        event_id = event["event_id"] 
        
        if r.sismember("processed_events", event_id):
            print("Skipping duplicate event:", event_id)
            continue
        r.sadd("processed_events", event_id)

        event = json.loads(raw_value)

        user_id = event["user_id"]
        event_type = event["event_type"]

        if event_type == "click":
            r.incr(f"user:{user_id}:clicks")
        elif event_type == "purchase":
            r.incrbyfloat(
                f"user:{user_id}:total_spent",
                event.get("amount", 0.0),
            )

        print("Processed:", event)

    except Exception as e:
        print("Skipping invalid message:", msg.value, e)

