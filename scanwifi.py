import network
import time

KNOWN_NETWORKS = {
    "UPC4489698_2.4GHz": "Pawel130130",
    "InnaSiec": "InneHaslo123"
}

class WiFi:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = network.WLAN(network.STA_IF)
            cls._instance.active(True)
        return cls._instance

def scan_networks():
    wlan = WiFi.get_instance()

    print("Activating interface...")

    timeout = 10
    while not wlan.active() and timeout > 0:
        print("... Waiting for WiFi activation...")
        time.sleep(1)
        timeout -= 1

    if not wlan.active():
        print("❌ Failed to activate WiFi interface.")
        return

    print("✅ Interface active. Scanning for networks...")
    time.sleep(1)

    try:
        networks = wlan.scan()
    except Exception as e:
        print("❌ Error during scan:", e)
        return

    if not networks:
        print("No networks found.")
        return

    found_ssids = []

    for net in networks:
        try:
            ssid = net[0].decode('utf-8')
        except UnicodeDecodeError:
            ssid = "<unreadable name>"

        if not ssid:
            continue  # skip empty SSIDs

        found_ssids.append(ssid)
        print(f"Found network: {ssid} (RSSI: {net[3]} dBm)")

    # Check for known networks
    for ssid in KNOWN_NETWORKS:
        if ssid in found_ssids:
            print(f"🔍 Attempting to connect to {ssid}...")
            wlan.connect(ssid, KNOWN_NETWORKS[ssid])

            # Wait for connection
            for _ in range(10):
                if wlan.isconnected():
                    break
                print("⏳ Connecting...")
                time.sleep(1)

            if wlan.isconnected():
                print("✅ Connected to:", ssid)
                print("IP Address:", wlan.ifconfig()[0])
            else:
                print("❌ Failed to connect to", ssid)
            return

    print("❌ No known networks available.")
