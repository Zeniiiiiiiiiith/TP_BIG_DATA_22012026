import json
from fastapi import FastAPI
from kafka import KafkaConsumer, KafkaProducer
import threading

api = FastAPI()

BOOTSTRAP = "kafka:9092"
TOPIC_IN = "parsed-events"
TOPIC_OUT = "alerts"

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP, value_serializer=lambda v: json.dumps(v).encode("utf-8"))

def score_event(event: dict) -> dict:
    status = int(event.get("status") or 0)
    label = "suspect" if status >= 400 else "legitime"
    event["prediction"] = label
    return event

def consume_loop():
    consumer = KafkaConsumer(
        TOPIC_IN,
        bootstrap_servers=BOOTSTRAP,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    for msg in consumer:
        event = msg.value
        out = score_event(event)
        if out["prediction"] == "suspect":
            producer.send(TOPIC_OUT, out)

threading.Thread(target=consume_loop, daemon=True).start()

@api.get("/health")
def health():
    return {"ok": True}
