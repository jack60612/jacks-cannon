import asyncio
import time

import network
import urequests  # from micropython
import machine

from cannon.buttons.fire_button import FireButton
from cannon.constants import LED, Constants, PinValues


class NetworkClient:
    """
    Class for the network server & Wifi Access Point
    """

    wlan: network.WLAN
    fire_button: FireButton
    watchdog: machine.WDT
    def __init__(self) -> None:
        """
        Initialize the network server
        """
        self.fire_button: FireButton = FireButton(pin=PinValues.remote_button_pin)
        #self.fire_button.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=None, wake=machine.DEEPSLEEP)
        self.watchdog = machine.WDT(timeout=Constants.watchdog_timeout)  # watchdog timer
        self.start_wifi() # we dont feed the watchdog after we start looping here.

    def start_wifi(self) -> None:
        """
        Start the WI-FI access point
        """
        self.wlan: network.WLAN = network.WLAN(
            network.STA_IF
        )  # station instead of ap mode
        self.wlan.active(True)
        self.wlan.connect(ssid=Constants.ssid, key=Constants.password)
        # wait for connection to come up
        # pre loop watchdog feeding, about 6 tries to connect before we reset.
        self.watchdog.feed()
        loops = 0
        while self.wlan.status() != 3:  # 3 is connected
            self.led_toggle_time(500)
            print("Connecting to wifi")
            time.sleep_ms(500)
            loops += 1
            self.watchdog.feed()
            if loops > 10:
                print("Failed to connect to wifi, resetting")
                reset()
        print("WIFI Connected")
        print(self.wlan.ifconfig())

    async def button_client(self):
        self.watchdog.feed() # feed the watchdog, yay we started. so we don't reset
        count = 0
        # Core loop
        while True:
            self.fire_button.button.press.clear()
            try: # wait for the button to be pressed
                await asyncio.wait_for_ms(self.fire_button.button.press.wait(), timeout=5000)
            except asyncio.TimeoutError:
                print("Timeout waiting for button press")
                self.watchdog.feed() # feed the watchdog, so we don't reset
                count += 1 # add one to count
                if count > 6: # 30 seconds
                    print("Timeout waiting for button press for 30 seconds, going into deepsleep.")
                    #machine.deepsleep()
                continue
            else: # button pressed
                count = 0 
            print("Fire button pressed")
            self.watchdog.feed() # feed the watchdog, so we don't reset
            await self.make_request()

    async def make_request(self) -> None:
        """
        Make a request to the server
        """
        print("Making request")
        try:
            response = urequests.get("http://192.168.4.1/trigger/activate")
        except OSError as e:
            error = True
            await self.handle_error(e)
            print("Error:", e)
        else:
            error = False if response.status_code == 200 else True
        if error:
            print("Error making request")
            for _ in range(10): # blink 10 times for 1 second
                self.led_toggle_time(100)
                self.watchdog.feed()
                time.sleep_ms(100)
            return
        r_text: str = response.text
        if "triggered" in r_text:
            print("triggered")
            for _ in range(2):  # blink 2 seconds for 1 second
                self.led_toggle_time(500)
                self.watchdog.feed()
                time.sleep_ms(500)
        elif "safety on" in r_text:
            print("safety on")
            for _ in range(5):  # blink 5 times for 1 second
                self.led_toggle_time(200)
                self.watchdog.feed()
                time.sleep_ms(200)
        else:
            print("Unknown response")
            for _ in range(10):
                self.led_toggle_time(100)
                self.watchdog.feed()
                time.sleep_ms(100)

    def led_toggle_time(self, time_ms: int) -> None:
        """
        Toggle the LED for a certain amount of time
        :param time_ms: The time to toggle the LED for in ms
        """
        LED.toggle()
        time.sleep_ms(time_ms)
        LED.toggle()
    
    async def handle_error(self, e: OSError) -> None:
        """
        Handle an error
        :param e: The error to handle
        """
        if e.args[0] == 113:
            print("No route to host, attempting to reconnect to wifi")
            self.start_wifi()

    async def start(self) -> None:
        """
        Start the webserver
        """
        await self.button_client()
