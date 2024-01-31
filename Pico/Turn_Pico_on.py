import serial
from serial.tools import list_ports

"""
This code is used to start up all the components connected to the pico (LCD, neopixel, RFID).

"""

# Function to start the pico
def start_pico():
    available_ports = list_ports.comports()
    selected_port = available_ports[0].device

    # Open a connection with the Pico
    with serial.Serial(port=selected_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            # Send a command to execute a file on the pico
            serial_port.write(b'exec(open("master.py").read())\r\n')
            # Close the connection with the pico
            serial_port.close()