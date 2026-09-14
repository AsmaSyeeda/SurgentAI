import redis
import json

# Connect to the local Redis broker
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Subscribe to the surgery stream
pubsub = r.pubsub()
pubsub.subscribe("surgery_stream")

print("Agent 4: The Recorder is listening...")
transcript = []

try:
    for message in pubsub.listen():
        if message["type"] == "message":
            # Parse the incoming JSON payload
            data = json.loads(message["data"])
            
            # Log the event
            log_entry = f"[{data['timestamp']}] {data['source']}: {data['event']} (Risk: {data['risk_level']})"
            print(log_entry)
            
            # Store it in the transcript buffer for the LLM later
            transcript.append(data)
            
except KeyboardInterrupt:
    print("\nAgent 4 stopped. Final Transcript Buffer contains", len(transcript), "events.")