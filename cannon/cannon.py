try:
    import asyncio
except ImportError:
    import uasyncio as asyncio
from machine import WDT, Pin  # Watchdog Timer

from cannon.buttons.fire_button import FireButton
from cannon.buttons.safety_button import SafetyButton
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

    def __init__(self) -> None:
        """
        Initialize the cannon
        """
        self.fire_button: FireButton = FireButton()
        self.safety_button: SafetyButton = SafetyButton()
        self.main_relay: Relay = Relay()
        self.network_server: NetworkServer = NetworkServer(self.fire_cannon)

    async def start(self) -> None:
        """
        Main function for the cannon
        :return:
        """
        wdt = WDT(timeout=2000)  # 2 seconds
        await self.network_server.start()  # Start the network server
        # Core loop
        while True:
            if self.fire_button.is_pressed():
                print("Fire button pressed")
                await self.fire_cannon()
            await asyncio.sleep_ms(100)
            wdt.feed()
            #print("Looping")

    async def fire_cannon(self) -> None:
        """
        Fire the cannon
        """
        milliseconds: int = 100
        print("Fire Command Received")
        if self.safety_button.is_pressed():
            print("Safety released, firing")
            LED.on()
            self.main_relay.relay_on()
            print("Solenoid on")
            await asyncio.sleep_ms(milliseconds)
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
