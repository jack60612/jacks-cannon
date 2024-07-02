from cannon.buttons.button import Button
from cannon.constants import Constants, PinValues


class SafetyButton(Button):
    """
    Class for interacting with the safety button
    """

    def __init__(
        self,
        pin: int = PinValues.safety_switch_pin,
        debounce_window: int = Constants.debounce_window,
    ) -> None:
        """
        Initialize the safety switch
        :param pin: The pin the safety switch is connected to
        """
        super().__init__(pin=pin, debounce_window=debounce_window)
