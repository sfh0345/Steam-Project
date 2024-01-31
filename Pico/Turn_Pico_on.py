import serial
from serial.tools import list_ports

def start_pico():
    available_ports = list_ports.comports()
    selected_port = available_ports[0].device

    # Open a connection with the Pico
    with serial.Serial(port=selected_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            # Stuur een commando om master.py uit te voeren
            serial_port.write(b'exec(open("master.py").read())\r\n')
            # Sluit verbinding met de Pico
            serial_port.close()