from cannon.buttons.button import Button
from cannon.constants import Constants, PinValues
from primitives import ESwitch  # events.py


class SafetyButton(Button):
    """
    Class for interacting with the safety button
    """

    switch: ESwitch

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
        self.switch = ESwitch(pin=self.pin)
        self.switch.debounce_ms = self.debounce_window

    def is_pressed(self) -> bool:
        """
        Get the state of the safety switch, with debouncing
        :return: True if the safety switch is pressed, False otherwise
        """
        return self.switch() == 1
