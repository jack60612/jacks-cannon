from button import Button

from cannon.constants import Constants


class FireButton(Button):
    """
    Class for interacting with the fire button
    """

    def __init__(self, pin: int = Constants.fire_button_pin) -> None:
        """
        Initialize the fire button
        :param pin: The pin the fire button is connected to
        """
        super().__init__(pin)
