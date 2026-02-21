import paho.mqtt.client as mqtt
import time
import random
import json

# --- CONFIGURAÇÕES UBIDOTS ---
UBIDOTS_BROKER = "industrial.api.ubidots.com"
UBIDOTS_TOKEN  = "BBUS-2ZiGS45Bv0mDa3XzHxIJLkQkUNV3Oo"   # ideal: use o Default Token
DEVICE_LABEL   = "vending-machine"                        # <-- API LABEL do device (não o ID)

TOPIC = f"/v1.6/devices/{DEVICE_LABEL}"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("on_connect reason_code:", reason_code)

client = mqtt.Client(client_id="python_pub_01", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(UBIDOTS_TOKEN, password="")
client.on_connect = on_connect

try:
    print("Conectando ao broker do Ubidots...")
    client.connect(UBIDOTS_BROKER, 1883, keepalive=60)
    client.loop_start()

    while True:
        payload = {
            "temperatura": round(random.uniform(20, 30), 2),
            "umidade": round(random.uniform(40, 60), 2),
            "pressao": round(random.uniform(1000, 1020), 2),
            "luminosidade": random.randint(0, 100)
        }

        msg = json.dumps(payload)
        result = client.publish(TOPIC, payload=msg, qos=0)

        print(f"[{time.strftime('%H:%M:%S')}] TOPIC={TOPIC} -> {msg} | mid={result.mid} rc={result.rc}")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nEncerrando...")
finally:
    try:
        client.loop_stop()
        client.disconnect()
    except:
        pass
