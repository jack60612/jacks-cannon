from primitives import EButton  # events.py

from cannon.buttons.button import Button
from cannon.constants import Constants, PinValues


class FireButton(Button):
    """
    Class for interacting with the fire button
    """

    button: EButton

    def __init__(
        self,
        pin: int = PinValues.fire_button_pin,
        debounce_window: int = Constants.debounce_window,
    ) -> None:
        """
        Initialize the fire button
        :param pin: The pin the fire button is connected to
        """
        super().__init__(pin=pin, debounce_window=debounce_window)
        self.button = EButton(pin=self.pin)
        self.button.debounce_ms = self.debounce_window

    def is_pressed(self) -> bool:
        """
        Get the state of the safety switch, with debouncing
        :return: True if the safety switch is pressed, False otherwise
        """
        return self.button() == 1
