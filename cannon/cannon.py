import asyncio
import time

from machine import Pin  # Watchdog Timer

from cannon.buttons.fire_button import FireButton
from cannon.buttons.safety_button import SafetyButton
from cannon.constants import Constants
from cannon.network_server import NetworkServer
from cannon.relay import Relay

LED = Pin("LED", Pin.OUT)


class Cannon:
    """
    Class for the cannon
    """

    fire_button: FireButton
    safety_button: SafetyButton
    main_relay: Relay
    network_server: NetworkServer
    fire_time: int
    main_loop_time: int
    watchdog_timeout: int

    def __init__(self) -> None:
        """
        Initialize the cannon
        """
        self.fire_button: FireButton = FireButton()
        self.safety_button: SafetyButton = SafetyButton()
        self.main_relay: Relay = Relay()
        self.network_server: NetworkServer = NetworkServer(self.fire_cannon)
        self.fire_time: int = Constants.fire_time
        self.main_loop_time: int = Constants.main_loop_time
        self.watchdog_timeout: int = Constants.watchdog_timeout

    async def start(self) -> None:
        """
        Main function for the cannon
        :return:
        """
        LED.on()
        # wdt = WDT(timeout=self.watchdog_timeout)  # watchdog timer
        await self.network_server.start()  # Start the network server
        LED.off()
        # Core loop
        while True:
            self.fire_button.button.press.clear()
            await self.fire_button.button.press.wait()
            print("Fire button pressed")
            await self.fire_cannon()
            # wdt.feed()
            # print("Looping")

    async def fire_cannon(self) -> None:
        """
        Fire the cannon
        """
        print("Fire Command Received")
        if self.safety_button.is_pressed():
            print("Safety released, firing")
            LED.on()
            self.main_relay.relay_on()
            print("Solenoid on")
            # this is purposely blocking, so that the time is accurate
            time.sleep_ms(self.fire_time)
            self.main_relay.relay_off()
            LED.off()
            print("Solenoid off")
        else:
            print("Safety not released, not firing")


def main() -> None:
    """
    Starts event loop
    """
    cannon: Cannon = Cannon()
    try:
        asyncio.run(cannon.start())
    finally:
        asyncio.new_event_loop()


if __name__ == "__main__":
    main()
