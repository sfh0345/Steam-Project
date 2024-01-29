from getuserfriendlist import get_friend_usernames
from serial.tools import list_ports
import serial

def online_friends():
    var = get_friend_usernames("76561199022018730")  # SteamID is predefined moet veranderen bij merge
    friend_list_names = len(var[0])
    friend_list_count = var[1]
    friend_list = friend_list_names + friend_list_count
    return friend_list

def read_serial(port):
    line = port.read(1000)
    return line.decode()

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
    else:
        # Open de poort als deze niet open is
        print("[INFO] De serial port wordt geopend:", serial_port.name, "...")
        serial_port.open()

    # stuur de data automatisch zonder input te geven met een commando
    data = f"O{online_friends()}\r"
    serial_port.write(data.encode())
    pico_output = read_serial(serial_port)
    pico_output = pico_output.replace('\r\n', ' ')

    # printen om de te versturen data te zien (om te testen)
    # print("[PICO] " + pico_output)

    # Sluit de connectie met Pico
    serial_port.close()
    print("[INFO] De serial port wordt gesloten!")