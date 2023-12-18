def read_serial(port):
    """Read data from serial port and return as string."""
    line = port.read(1000)
    return line.decode()


def steamidinput(steamid64):
    if len(steamid64) != 17:
        time = canvas.create_text(
            162.0,
            1013.0,
            anchor="nw",
            text="We konden uw SteamID niet vinden. Zorg ervoor dat u het SteamID64 heeft",
            fill="#FFFFFF",
            font=("Motiva Sans Bold", 40 * -1)
        )
        window.after(4000, lambda: canvas.delete(time))
    else:
        status1 = getsteamuserinfo(steamid64)
        if status1 == 0:
            time = canvas.create_text(
                262.0,
                1013.0,
                anchor="nw",
                text="Er is iets mis gegaan. Probeer het later opnieuw",
                fill="#FFFFFF",
                font=("Motiva Sans Bold", 40 * -1)
            )
            window.after(4000, lambda: canvas.delete(time))
        elif status1 == 1:
            time = canvas.create_text(
                340.0,
                1013.0,
                anchor="nw",
                text="Er is geen steam gebruiker gevonden met dat SteamID64",
                fill="#FFFFFF",
                font=("Motiva Sans Bold", 40 * -1)
            )
            window.after(4000, lambda: canvas.delete(time))
        else:
            name = status1[0]
            avatarurl = status1[1]
            status = status1[2]
            window.destroy()
            dashboardwindow(name, avatarurl, status, steamid64)
# Define an event to signal the thread to stop
stop_event = threading.Event()

def serial_thread(stop_event):
    """Function to run serial communication in a separate thread."""
    # predifine de port voor serial
    pico_port = "COM12"

    # Open een verbinding met de Pico
    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            print("[INFO] Gebruik seriële poort", serial_port.name)
        else:
            print("[INFO] Open seriële poort", serial_port.name, "...")
            serial_port.open()

    # Open een verbinding met de Pico
    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            print("[INFO] Gebruik seriële poort", serial_port.name)
        else:
            print("[INFO] Open seriële poort", serial_port.name, "...")
            serial_port.open()

        try:
            steamid_received = False # Flag to indicate if SteamID has been received
            while not steamid_received and not stop_event.is_set():
                # Lees de seriële gegevens van de Pico
                pico_output = read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')

                # Controleer of de ontvangen gegevens de verwachte indeling hebben
                if pico_output.startswith("steamid64:"):
                    steamid64 = pico_output.split(":")[1].strip()
                    print("[PICO] SteamID64 ontvangen:", steamid64)

                    # Set the flag to True to exit the loop
                    steamid_received = True

                    # Doe hier iets met de ontvangen steamid64, bijv. sla het op in een variabele of bestand.
                    window.after(100, lambda: steamidinput(steamid64))  # Use after() to call steamidinput

                else:
                    print("[PICO] Ongeldige gegevensindeling ontvangen:", pico_output)

                # Een korte pauze om overbelasting te voorkomen
                time.sleep(1)

        except KeyboardInterrupt:
            print("[INFO] Ctrl+C gedetecteerd. Beëindigen.")
        finally:
            # Sluit verbinding met de Pico
            serial_port.close()
            print("[INFO] Seriële poort gesloten. Tot ziens.")

# Create a thread for serial communication
serial_thread = threading.Thread(target=serial_thread, args=(stop_event,), daemon=True)
serial_thread.start()



# Function to be called when the window is closed
def on_close():
    if serial_thread.is_alive():
        stop_event.set()
        serial_thread.join()  # Wait for the serial thread to finish before exiting
        window.destroy()


# Bind the stop_event.set() method to the window close event
window.protocol("WM_DELETE_WINDOW", stop_event.set)