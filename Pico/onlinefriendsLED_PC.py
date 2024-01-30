from getuserfriendlist import get_friend_usernames
from serial.tools import list_ports
import serial

"""
This code is run on the PC-side and is used to send the total online friends using the SteamID over to the Pico over a serial connection. 
The data is then used to control the neopixel, and based on the number of online friends, display a particular light pattern.

"""

# Function to gather the total of online friends
def online_friends():
    var = get_friend_usernames("76561199022018730")  # SteamID is predefined for testing
    friend_list_count = var[1]
    friend_list = friend_list_names + friend_list_count
    return friend_list

# Function to to read the serial port for testing
def read_serial(port):
    line = port.read(1000)
    return line.decode()

# Automatically detect all available serial ports
available_ports = list_ports.comports()
if not available_ports:
    print("[ERROR] Geen serial ports gevonden!")
    exit()

# Select the first available port
selected_port = available_ports[0].device

# Open a connection with the Pico
with serial.Serial(port=selected_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    # Use the port if available
    if serial_port.isOpen():
        print("[INFO] De serial port wordt gebruikt:", serial_port.name)
    else:
        # Open and use the port if not available
        print("[INFO] De serial port wordt geopend:", serial_port.name, "...")
        serial_port.open()

    # Send the data automatically over to the Pico
    data = f"O{online_friends()}\r"
    serial_port.write(data.encode())
    pico_output = read_serial(serial_port)
    pico_output = pico_output.replace('\r\n', ' ')

    # Print the data before sending (for testing)
    # print("[PICO] " + pico_output)

    # Close the connection with the Pico
    serial_port.close()
    print("[INFO] De serial port wordt gesloten!")