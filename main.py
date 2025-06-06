import time
import scanwifi
from IR_Recive import IRReceiver
from IR_Send import IRSender

def main():
    print("Scanning for WiFi networks:")
    scanwifi.scan_networks()

    print("Starting IR receiver on GPIO23")
    ir = IRReceiver(pin_number=23)

    sender = IRSender(pin_number=26)  # GPIO26 for sending

    try:
        while True:
            print("\nOptions:")
            print("  [1] Show saved IR codes")
            print("  [2] Send an IR code")
            print("  [q] Quit")
            choice = input("Select an option: ").strip().lower()

            if choice == "1":
                codes = ir.get_saved_codes()
                if not codes:
                    print("No saved IR codes.")
                else:
                    print("Saved IR codes:")
                    for idx, code in enumerate(codes):
                        print(f"  [{idx}] {code}")

            elif choice == "2":
                codes = ir.get_saved_codes()
                if not codes:
                    print("No codes to send.")
                    continue

                print("Select code number to send:")
                for idx, code in enumerate(codes):
                    print(f"  [{idx}] {code}")

                selected = input("Code number: ").strip()
                if selected.isdigit():
                    idx = int(selected)
                    if 0 <= idx < len(codes):
                        print(f"📤 Sending code: {codes[idx]}")
                        sender.send_nec(codes[idx])
                        print("✅ Sent.")
                    else:
                        print("❌ Invalid number.")
                else:
                    print("❌ Not a valid number.")

            elif choice == "q":
                print("Exiting program...")
                break

            else:
                print("❌ Unknown option.")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted.")

if __name__ == "__main__":
    main()
