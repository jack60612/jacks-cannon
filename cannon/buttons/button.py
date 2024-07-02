from machine import Pin


class Button:
    """
    Class for controlling a button, which is connected to a pin and ground
    """

    pin_number: int
    pin: Pin  # pin, in pull down mode, so that it reads 1 when pressed
    last_value: bool
    debounce_window: int

    def __init__(self, pin: int, debounce_window: int) -> None:
        """
        Initialize the button
        :param pin: The pin the button is connected to
        """
        self.pin_number: int = pin
        self.pin = Pin(
            self.pin_number, Pin.IN, Pin.PULL_UP
        )  # pull up because the button connects to ground
        self.last_value = False
        self.debounce_window = debounce_window

    def is_pressed_raw(self) -> bool:
        """
        Get the state of the button
        :return: True if the button is pressed, False otherwise
        """
        return self.pin.value() == 0

    def is_pressed(self) -> bool:
        """
        Get the state of the button, with debouncing
        :return: True if the button is pressed, False otherwise
        """
        pass
