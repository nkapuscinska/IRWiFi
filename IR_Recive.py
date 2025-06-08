from machine import Pin, Timer
import time
import ujson

class IRReceiver:
    def __init__(self, pin_number=23, storage_file="ir_codes.json"):
        self.pin = Pin(pin_number, Pin.IN)
        self.timer = Timer(0)
        self.storage_file = storage_file

        self.raw_data = []
        self.reading = False
        self.last_time = 0

        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self._ir_callback)
        self.timer.init(period=250, mode=Timer.PERIODIC, callback=lambda t: self._check_reading())

    def _ir_callback(self, pin):
        now = time.ticks_us()
        if not self.reading:
            self.raw_data = []
            self.reading = True
            self.last_time = time.ticks_us()
            return  # pomiń pierwszy duration
        duration = time.ticks_diff(now, self.last_time)
        self.last_time = now
        self.raw_data.append(duration)

    def _check_reading(self):
        if self.reading and len(self.raw_data) > 10:
            code = self._decode_nec(self.raw_data)
            if code:
                print("Odebrano kod IR: 👍", code)
                self._save_code(code)
            self.reading = False
            self.last_time = 0


    def _decode_nec(self, data):
        if len(data) < 48:
            return None

        bits = ""
        for duration in data[1:]:
            if duration > 1600:  # typowo: 1 = ~1.7ms, 0 = ~0.6ms
                bits += "1"
            else:
                bits += "0"
        try:
            return hex(int(bits[:32], 2))
        except:
            return None

    def _save_code(self, code):
        try:
            with open(self.storage_file, "r") as f:
                codes = ujson.load(f)
        except:
            codes = []

        codes.append(code)

        with open(self.storage_file, "w") as f:
            ujson.dump(codes, f)

    def clear_codes(self):
        with open(self.storage_file, "w") as f:
            ujson.dump([], f)

    def get_saved_codes(self):
        try:
            with open(self.storage_file, "r") as f:
                return ujson.load(f)
        except:
            return []
