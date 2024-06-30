import time

from cannon.buttons.fire_button import FireButton
from cannon.buttons.safety_button import SafetyButton
from cannon.relay import Relay


def main() -> None:
    """
    Main function for the cannon
    """
    fire_button: FireButton = FireButton()
    safety_button: SafetyButton = SafetyButton()
    main_relay: Relay = Relay()
    while True:
        if safety_button.is_pressed():
            if fire_button.is_pressed():
                main_relay.relay_on()
                time.sleep_ms(100)
                main_relay.relay_off()


if __name__ == "__main__":
    main()
