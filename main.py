import time
import scanwifi
from MQTT import MQTTManager
from IR_Recive import IRReceiver
from IR_Send import IRSender
from decodeMQTT import mqtt_callback
# MQTT configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC_RECEIVED = b"ir/received"
MQTT_TOPIC_SEND = b"ir/send"


def main():
    print("Scanning for WiFi networks:")
    scanwifi.scan_networks()

    print("Starting IR receiver on GPIO23")

    mqtt = MQTTManager(client_id="esp-ir", broker=MQTT_BROKER, port=MQTT_PORT, debug=True)

    mqtt.connect()
    mqtt.subscribe(MQTT_TOPIC_RECEIVED, mqtt_callback)

    print("Listening for MQTT commands. Press Ctrl+C to exit.")
    try:
        while True:
            try:
                mqtt.check_msg()
            except Exception as e:
                print(f"MQTT message check error: {e}")
                # Spróbuj ponownie połączyć się z brokerem
                try:
                    mqtt.connect()
                    mqtt.subscribe(MQTT_TOPIC_RECEIVED, mqtt_callback)
                    print("Reconnected to MQTT broker.")
                except :
                # Exception as e2:
                    # print(f"Reconnection failed: {e2}")
                    time.sleep(2)  # Poczekaj chwilę przed kolejną próbą
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        mqtt.disconnect()

if __name__ == "__main__":
    main()
