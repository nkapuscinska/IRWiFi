from umqtt.simple import MQTTClient

class MQTTManager:
    def __init__(self, client_id, broker, port=1883, user=None, password=None, keepalive=60, debug=False):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.keepalive = keepalive
        self.debug = debug
        self.client = None
        self.connected = False

    def connect(self):
        self.client = MQTTClient(
            client_id=self.client_id,
            server=self.broker,
            port=self.port,
            user=self.user,
            password=self.password,
            keepalive=self.keepalive
            
        )
        try:
            self.client.connect()
            self.connected = True
            if self.debug:
                print("Connected to MQTT broker:", self.broker)
        except Exception as e:
            print("MQTT connection error:", e)
            self.connected = False

    def disconnect(self):
        if self.client:
            self.client.disconnect()
            self.connected = False
            if self.debug:
                print("Disconnected from MQTT broker.")

    def publish(self, topic, message):
        try:
            self.client.publish(topic, message)
            if self.debug:
                print(f"Published: [{topic}] {message}")
        except Exception as e:
            print("MQTT publish error:", e)

    def subscribe(self, topic, callback):
        if not self.connected:
            self.connect()
        try:
            self.client.set_callback(callback)
            self.client.subscribe(topic)
            if self.debug:
                print("Subscribed to topic:", topic)
        except Exception as e:
            print("MQTT subscribe error:", e)

    def check_msg(self):
        if self.client:
            try:
                self.client.check_msg()
            except Exception as e:
                print("MQTT message check error:", e)
