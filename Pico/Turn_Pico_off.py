import serial
from serial.tools import list_ports
import time

"""
This code is used to turn the pico off on startup and after the user has closed the dashboard.
"""

# automatically detect all available ports
available_ports = list_ports.comports()
if not available_ports:
    print("[ERROR] Geen serial ports gevonden!")
    exit()

# select the first available port
selected_port = available_ports[0].device

# Open a connection with the serial port
with serial.Serial(port=selected_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    # Use the port if open/available
    if serial_port.isOpen():
        print("[INFO] De serial port wordt gebruikt:", serial_port.name)

        # execute to run the file on the pico
        serial_port.write(b'exec(open("main.py").read())\r\n')
        serial_port.write(b'\x03')
        time.sleep(1)

    else:
        # Open the port when not open
        print("[INFO] De serial port wordt geopend:", serial_port.name, "...")
        serial_port.open()

        serial_port.write(b'exec(open("main.py").read())\r\n')