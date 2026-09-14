import redis
import json
import time
import random
from datetime import datetime

# Connect to the local Redis broker
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Define a list of mock events that might happen during a procedure
events = [
    {"source": "Agent 1: The Eye", "event": "Incision made", "risk_level": "low"},
    {"source": "Agent 2: The Monitor", "event": "Heart rate stable at 72 bpm", "risk_level": "low"},
    {"source": "Agent 3: The Guardian", "event": "Scalpel detected near critical vessel", "risk_level": "high"},
    {"source": "Agent 1: The Eye", "event": "Gallbladder extraction complete", "risk_level": "low"}
]

print("Starting mock surgery stream...")

for event in events:
    # Add a timestamp to the payload
    payload = event.copy()
    payload["timestamp"] = datetime.now().isoformat()
    
    # Publish the JSON payload to the "surgery_stream" channel
    r.publish("surgery_stream", json.dumps(payload))
    print(f"Published: {payload['event']}")
    
    # Wait a few seconds before the next event to simulate real time
    time.sleep(random.uniform(2.0, 5.0))

print("Mock surgery complete. End of stream.")