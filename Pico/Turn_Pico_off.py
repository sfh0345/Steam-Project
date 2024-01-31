import serial
from serial.tools import list_ports
import time

# def read_serial(port):
#     line = port.read(1000)
#     return line.decode()

# detecteer automatisch alle beschikbare serial poorten
available_ports = list_ports.comports()
if not available_ports:
    print("[ERROR] Geen serial ports gevonden!")
    exit()

# selecteer de eerste beschikbare poort
selected_port = available_ports[0].device

# Open een connectie met de serial poort
with serial.Serial(port=selected_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    # Gebruik de poort als deze open/beschikbaar is
    if serial_port.isOpen():
        print("[INFO] De serial port wordt gebruikt:", serial_port.name)

        serial_port.write(b'exec(open("main.py").read())\r\n')

        # Wait for the script execution to complete (adjust the delay as needed)
        # time.sleep(5)

        # Send Ctrl+C to interrupt execution and reset
        serial_port.write(b'\x03')
        time.sleep(1)  # Adjust the delay as needed

    else:
        # Open de poort als deze niet open is
        print("[INFO] De serial port wordt geopend:", serial_port.name, "...")
        serial_port.open()

        serial_port.write(b'exec(open("main.py").read())\r\n')