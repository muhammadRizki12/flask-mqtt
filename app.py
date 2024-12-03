from flask import Flask, jsonify, request
from flask_mqtt import Mqtt
import json

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = ''
# app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0

# Initialize MQTT
mqtt = Mqtt(app)

# Subscription Topics
CROWD_FRAME_TOPIC = 'mqtt-crowd-frame'
FATIGUE_FRAME_TOPIC = 'mqtt-fatigue-frame'

# Publication Topics
CROWD_RESULT_TOPIC = 'mqtt-crowd-result'
FATIGUE_RESULT_TOPIC = 'mqtt-fatigue-result'

# Global variables to store latest received messages
latest_crowd_frame = None
latest_fatigue_frame = None

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('Connected to MQTT Broker')

    # Subscribe to topics
    mqtt.subscribe(CROWD_FRAME_TOPIC)
    mqtt.subscribe(FATIGUE_FRAME_TOPIC)

    print(f'Subscribed to {CROWD_FRAME_TOPIC} and {FATIGUE_FRAME_TOPIC}')

@mqtt.on_message()
def handle_mqtt_message(clientt, userdata, message):
    global latest_crowd_frame, latest_fatigue_frame
    topic = message.topic
    payload = message.payload.decode('utf-8')

    try:
        # parse the payload
        data = json.loads(payload)

        if topic == CROWD_FRAME_TOPIC:
            latest_crowd_frame = data
            print(latest_crowd_frame)
            # process crowd frame and publish result
            crowd_result = process_crowd_frame(data)
            mqtt.publish(CROWD_RESULT_TOPIC, json.dumps(crowd_result))

        elif topic == FATIGUE_FRAME_TOPIC:
            latest_fatigue_frame = data
            print(latest_fatigue_frame)
            # process fatigue frame and publish result
            fatigue_result = process_fatigue_frame(data)
            mqtt.publish(FATIGUE_RESULT_TOPIC, json.dumps(fatigue_result))

    except json.JSONDecodeError:
        print(f'Error decoding JSON from topic {topic}')
    except Exception as e:
        print(f'Error processing message from {topic}: {e}')


def process_crowd_frame(frame_data):
    return {
        'status': 'true',
        'message': 'this is crowd frame'
    }

def process_fatigue_frame(frame_data):
    return {
        'status': 'true',
        'message': 'this is fatigue frame'
    }

if __name__ == '__app__':
    app.run(debug=True)