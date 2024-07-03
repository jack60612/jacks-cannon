import asyncio
import time

import network
import urequests  # from micropython

from cannon.buttons.fire_button import FireButton
from cannon.constants import LED, Constants, PinValues


class NetworkClient:
    """
    Class for the network server & Wifi Access Point
    """

    wlan: network.WLAN
    fire_button: FireButton

    def __init__(self) -> None:
        """
        Initialize the network server
        """
        self.start_wifi()
        self.fire_button: FireButton = FireButton(pin=PinValues.remote_button_pin)

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
        while self.wlan.status() != 3:  # 3 is connected
            LED.on()
            time.sleep(0.5)
            LED.off()
            print("Connecting to wifi")
            time.sleep(0.5)
        print("WIFI Connected")
        print(self.wlan.ifconfig())

    async def button_client(self):
        # Core loop
        while True:
            self.fire_button.button.press.clear()
            await self.fire_button.button.press.wait()
            print("Fire button pressed")
            await self.make_request()

    async def make_request(self) -> None:
        """
        Make a request to the server
        """
        print("Making request")
        response = urequests.get("http://192.168.4.1/trigger/activate")
        r_text: str = response.text
        if response.status_code != 200:
            print("Error making request")
            for _ in range(10): # blink 10 times for 1 second
                await self.led_toggle_time(100)
            return
        elif "triggered" in r_text:
            print("triggered")
            for _ in range(2):  # blink 2 seconds for 1 second
                self.led_toggle_time(500)
        elif "safety on" in r_text:
            print("safety on")
            for _ in range(5):  # blink 5 times for 1 second
                await self.led_toggle_time(200)

    async def led_toggle_time(self, time_ms: int) -> None:
        """
        Toggle the LED for a certain amount of time
        :param time_ms: The time to toggle the LED for in ms
        """
        LED.on()
        await asyncio.sleep_ms(time_ms)
        LED.off()

    async def start(self) -> None:
        """
        Start the webserver
        """
        await self.button_client()
