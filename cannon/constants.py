from enum import Enum


class Constants(Enum):
    """
    Constants for the project
    """

    relay_pin = 2  # Relay Fire Pin (Output) (Connected to transistor)
    safety_switch_pin = 3  # Safety Switch Pin (Input) (Active when Connected to ground)
    fire_button_pin = 4  # Fire Button Pin (Input) (Active when Connected to ground)