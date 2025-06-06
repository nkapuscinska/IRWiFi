from machine import Pin, PWM
import time

class IRSender:
    def __init__(self, pin_number = 26, carrier_freq=38000):
        self.pin = Pin(pin_number, Pin.OUT)
        self.pwm = PWM(self.pin, freq=carrier_freq, duty=0)  # modulacja 38 kHz

    def _carrier_on(self):
        self.pwm.duty(512)  # ~50% wypełnienia

    def _carrier_off(self):
        self.pwm.duty(0)

    def _send_pulse(self, duration_us):
        self._carrier_on()
        time.sleep_us(duration_us)
        self._carrier_off()

    def _send_space(self, duration_us):
        time.sleep_us(duration_us)

    def send_nec(self, code_hex):
        # NEC: nagłówek 9ms + 4.5ms
        self._send_pulse(9000)
        self._send_space(4500)

        code = int(code_hex, 16)
        bits = f"{code:032b}"

        for bit in bits:
            self._send_pulse(560)
            if bit == "1":
                self._send_space(1690)
            else:
                self._send_space(560)

        # zakończenie: końcowy impuls
        self._send_pulse(560)

    def send_repeat(self):
        # Powtarzanie NEC: 9ms + 2.25ms + 560us
        self._send_pulse(9000)
        self._send_space(2250)
        self._send_pulse(560)

