import asyncio
import time
import urllib.request  # Used to fetch file over HTTP

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# =========================
# CONFIG
# =========================

# URL to your Windows HTTP server file
URL = "http://192.168.10.1:8000/coords.txt"

# Azure IoT connection string
CONN_STR = "HostName=CNCIOTHub.azure-devices.net;DeviceId=PlasmaCutterRasperryPi;SharedAccessKey=H91+syKQpDm1+XbYcbJhDbKRGnhI+TK5zFItgQM5aVo="


# =========================
# READ XYZ FROM FILE
# =========================
async def read_xyz():
    try:
        # Request file from Windows PC
        with urllib.request.urlopen(URL, timeout=1) as response:
            data = response.read().decode().strip()

            # Expect format: "X,Y,Z"
            if data:
                parts = data.split(",")

                if len(parts) == 3:
                    x = float(parts[0])
                    y = float(parts[1])
                    z = float(parts[2])

                    return round(x, 2), round(y, 2), round(z, 2)

        return None, None, None

    except Exception as e:
        print(f"Error reading coords: {e}")
        return None, None, None


# =========================
# SEND TELEMETRY LOOP
# =========================
async def send_recurring_telemetry(device_client):

    # Connect to Azure IoT Hub
    await device_client.connect()

    while True:
        # Get XYZ values from file
        x, y, z = await read_xyz()

        if x is not None:
            # Format JSON message
            msg_txt = '{{"x": {x}, "y": {y}, "z": {z}}}'
            data = msg_txt.format(x=x, y=y, z=z)

            # Create Azure message
            msg = Message(data)
            msg.content_encoding = "utf-8"
            msg.content_type = "application/json"

            # Debug print
            print("Sending:", data)

            # Send to Azure
            await device_client.send_message(msg)

        else:
            print("Waiting for valid XYZ data...")

        # Wait before next send
        await asyncio.sleep(0.5)


# =========================
# MAIN PROGRAM
# =========================
def main():

    # Create IoT client
    device_client = IoTHubDeviceClient.create_from_connection_string(CONN_STR)

    print("Sending CNC position to Azure...")
    print("Press Ctrl+C to exit")

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(send_recurring_telemetry(device_client))

    except KeyboardInterrupt:
        print("User exit")

    finally:
        loop.run_until_complete(device_client.shutdown())
        loop.close()


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
