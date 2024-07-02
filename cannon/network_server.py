import asyncio
import time

import network

from cannon.constants import Constants


class NetworkServer:
    """
    Class for the network server & Wifi Access Point
    """

    html: str
    wlan: network.WLAN
    addr: tuple[str, int]

    def __init__(self, trigger_callback) -> None:
        """
        Initialize the network server
        """
        self.main_task = None
        self.start_wifi()
        self.trigger_callback = trigger_callback
        self.html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>%s</p>
    </body>
</html>
"""

    def start_wifi(self) -> None:
        """
        Start the WI-FI access point
        """
        self.wlan: network.WLAN = network.WLAN(network.AP_IF)
        self.wlan.config(essid=Constants.ssid, password=Constants.password)
        self.wlan.active(True)
        # wait for connection to come up
        while not self.wlan.active():
            time.sleep(1)
        print("AP Mode Is Active, You can Now Connect")
        print("IP Address To Connect to:: " + self.wlan.ifconfig()[0])

    async def serve_client(self, reader, writer):
        print("Client connected")
        request_line = await reader.readline()
        print("Request:", request_line)
        # We are not interested in HTTP request headers, skip them
        while await reader.readline() != b"\r\n":
            pass

        request = str(request_line)
        triggered = request.find("/trigger/activate")
        print("triggered remotely = " + str(triggered))

        stateis = ""
        if triggered == 6:
            print("triggered remotely")
            await self.trigger_callback()
            stateis = "triggered"

        response = self.html % stateis
        writer.write("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        writer.write(response)

        await writer.drain()
        await writer.wait_closed()
        print("Client disconnected")

    async def start(self) -> None:
        """
        Start the webserver
        """
        self.main_task = await asyncio.create_task(
            asyncio.start_server(self.serve_client, "0.0.0.0", 80)
        )
        # await asyncio.start_server(self.serve_client, "0.0.0.0",80)
