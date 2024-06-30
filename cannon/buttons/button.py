import time

from machine import Pin


class Button:
    """
    Class for controlling a button, which is connected to a pin and ground
    """

    pin_number: int
    pin: Pin  # pin, in pull down mode, so that it reads 1 when pressed
    last_value: bool

    def __init__(self, pin: int) -> None:
        """
        Initialize the button
        :param pin: The pin the button is connected to
        """
        self.pin_number: int = pin
        self.pin = Pin(
            self.pin_number, Pin.IN, Pin.PULL_UP
        )  # pull up because the button connects to ground
        self.last_value = False

    def button_state_raw(self) -> bool:
        """
        Get the state of the button
        :return: True if the button is pressed, False otherwise
        """
        return self.pin.value() == 0

    def button_state(self) -> bool:
        """
        Get the debounced state of the button
        :return: True if the button is pressed, False otherwise
        """
        # wait for pin to change value
        # it needs to be stable for a continuous 20ms
        if self.button_state_raw == self.last_value:
            return self.last_value
        new_value = self.button_state_raw()
        active = 0
        while active < 20:  # wait for 20ms with the same value
            if self.button_state_raw() == new_value:
                active += 1  # if the value is still changed count up
            elif -20 > active:  # if the value flipped back return the old value
                return self.last_value
            elif active > 0:  # if the value flipped, reset the counter
                active = -1
            else:  # if the value is still old count negative
                active += -1
            time.sleep_ms(1)
        self.last_value = new_value
        return new_value  # if the value is stable for 20ms, return it

    def is_pressed(self) -> bool:
        """
        Check if the button is pressed
        :return: True if the button is pressed, False otherwise
        """
        return self.button_state()
