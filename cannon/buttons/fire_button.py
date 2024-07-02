from cannon.buttons.button import Button
from cannon.constants import Constants, PinValues


class FireButton(Button):
    """
    Class for interacting with the fire button
    """

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

    def button_triggered(self) -> bool:
        """
        Check if the button is pressed and not already tracked as pressed
        :return: True if the button is pressed and not already tracked as pressed, False otherwise
        """
        last_val = self.last_value
        button_state = self.debounced()
        if (
            button_state and not last_val
        ):  # if the button is pressed and the last value was not pressed
            return True
        else:  # if the button is not pressed or the last value was pressed
            return False
