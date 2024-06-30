from machine import Pin

from cannon.constants import Constants


class Relay:
    """
    Class for controlling the relay
    """

    pin_number: int
    pin: Pin

    def __init__(self, pin: int = Constants.relay_pin) -> None:
        """
        Initialize the relay
        :param pin: The pin the relay is connected to
        """
        self.pin_number: int = pin
        self.pin = Pin(self.pin_number, Pin.OUT)
        self.relay_off()

    def relay_on(self) -> None:
        """
        Fire the relay
        """
        self.pin.on()

    def relay_off(self) -> None:
        """
        Reset the relay
        """
        self.pin.off()

    def relay_state(self) -> bool:
        """
        Get the state of the relay
        :return: True if the relay is on, False otherwise
        """
        return self.pin.value() == 1
