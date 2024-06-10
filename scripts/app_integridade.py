import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
port = 1883
topic = "teste/integridade"

def on_message(client, userdata, msg):
    modified_message = msg.payload.decode().replace("original", "tampered")
    client.publish(topic, modified_message)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever()
