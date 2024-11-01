from machine import Pin


class PinValues:
    """
    Pin Values for the project
    """

    relay_pin = 2  # Relay Fire Pin (Output) (Connected to transistor)
    safety_switch_pin = 3  # Safety Switch Pin (Input) (Pull Up) (Active when Connected to ground)
    fire_button_pin = 4  # Fire Button Pin (Input) (Pull Down) (Active when 5v Signal)
    remote_button_pin = 5  # remote if enabled.


class Constants:
    """
    Other written constants for the project
    """

    ssid = "funnywifi"
    password = "hellothere"
    remote_enabled = False
    fire_time: int = 180  # Time to fire the cannon for in ms
    main_loop_time: int = 10  # 10ms loop time
    watchdog_timeout: int = (
        6000  # 6 seconds, watchdog timer, so if the program hangs, it will reset
    )
    debounce_window: int = 50  # 20ms debounce window


LED = Pin("LED", Pin.OUT)
