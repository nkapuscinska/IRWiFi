from IR_Recive import IRReceiver
from IR_Send import IRSender

class MQTTCommandHandler:
    def __init__(self, recive_pin=23, send_pin=26, mqtt_manager=None):
        self.write_mode = False
        self.ir = IRReceiver(pin_number=recive_pin)
        self.sender = IRSender(pin_number=send_pin)
        self.mqtt_manager = mqtt_manager  

    def callback(self, topic, msg):
        try:
            command = msg.decode().strip()
            print(f"MQTT message received: {command}")

            if self.write_mode:
                print("Saving new IR code...")
                self.ir._save_code(command)
                print("Code saved. Exiting write mode.")
                self.write_mode = False
                return

            if command.lower() == "write":
                print("Entering write mode. Send IR code to save...")
                self.write_mode = True

            elif command.lower() == "delete":
                print("Deleting all saved IR codes...")
                self.ir.clear_codes()
                print("All codes deleted.")

            elif command.lower() == "show":
                codes = self.ir.get_saved_codes()
                if not codes:
                    print("No saved IR codes.")
                    if self.mqtt_manager:
                        self.mqtt_manager.publish(b"ir/send", b"[]")
                else:
                    print("Sending list of all saved IR codes via MQTT (ir/send):")
                    if self.mqtt_manager:
                        import ujson
                        codes_json = ujson.dumps(codes)
                        self.mqtt_manager.publish(b"ir/send", codes_json.encode())
            elif command.isdigit() and 1 <= int(command) <= 10:
                number = int(command) - 1
                codes = self.ir.get_saved_codes()
                if 0 <= number < len(codes):
                    try:
                        print(f"Sending code #{command}: {codes[number]}")
                        self.sender.send_nec(codes[number])
                        print("Sent.")
                    except Exception as e:
                        print(f"Error sending code #{command}: {e}")
                else:
                    print(f"No code saved under number {command}.")
            else:
                print("Unknown command.")

        except Exception as e:
            print("Error handling MQTT message:", e)