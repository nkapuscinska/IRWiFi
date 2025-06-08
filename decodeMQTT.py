from IR_Recive import IRReceiver
from IR_Send import IRSender

RECIVE_PIN = 23
SEND_PIN = 26


write_mode = False


def mqtt_callback(topic, msg):
    global write_mode
        
    ir = IRReceiver(pin_number=RECIVE_PIN)
    sender = IRSender(pin_number=SEND_PIN)  # GPIO26 for sending

    try:
        command = msg.decode().strip()
        print(f"📥 MQTT message received: {command}")

        if write_mode:
            print("Saving new IR code...")
            ir._save_code(command)
            print("✅ Code saved. Exiting write mode.")
            write_mode = False
            return

        if command.lower() == "write":
            print("Entering write mode. Send IR code to save...")
            write_mode = True

        elif command.lower() == "delete":
            print("Deleting all saved IR codes...")
            ir.clear_codes()
            print("✅ All codes deleted.")

        elif command.isdigit() and 1 <= int(command) <= 10:
            idx = int(command) - 1
            codes = ir.get_saved_codes()
            if 0 <= idx < len(codes):
                try:
                    print(f"Sending code #{command}: {codes[idx]}")
                except Exception as e:
                    print(f"Sending code #{command}: [cannot display code: {e}]")
                sender.send_nec(codes[idx])
                print("✅ Sent.")
            else:
                print(f"⚠️ No code saved under number {command}.")
        else:
            print("⚠️ Unknown command.")

    except Exception as e:
        print("❌ Error handling MQTT message:", e)