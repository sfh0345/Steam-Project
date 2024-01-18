from machine import Pin
import time
import neopixel

np = neopixel.NeoPixel(Pin(9), 8)

# wacht voor de data via de serieele connectie
while True:
    data = input()

    # stuur de NeoPixel aan op basis van online vrienden
    led_count = int(data[1:])

    # als er geen vrienden online zijn
    if led_count < 1:
        for _ in range(5):  # Blink all 8 LEDs in rodd voor 5x
            np.fill((255, 0, 0))
            np.write()
            time.sleep(0.5)
            np.fill((0, 0, 0))
            np.write()
            time.sleep(0.5)
            # na 5x blinken gaan alle LEDs uit

    # als er 1-8 vrienden online zijn
    elif 1 <= led_count <= 8:
        for index in range(led_count):
            np[index] = (255, 0, 255)
            np.write()
            time.sleep(0.5)

        # wacht 5 sec voordat alle LEDs uitgeschakeld worden
        time.sleep(5)
        np.fill((0, 0, 0))
        np.write()

    # schakel alle LEDs aan en knippert de laatste als er meer dan 8 vrienden online zijn
    elif led_count > 8:
        # schakel de 1-7 LEDs aan
        for index in range(7):
            np[index] = (0, 255, 0)
            np.write()
            time.sleep(0.3)

        for _ in range(5):  # Blink de laatste (8ste LED) voor 5x
            np[7] = (0, 255, 0)
            np.write()
            time.sleep(0.5)
            np[7] = (0, 0, 0)
            np.write()
            time.sleep(0.5)

        # schakel alle LEDs uit nadat de blink voorbij is
        np[7] = (0, 255, 0)
        np.write()
        time.sleep(0.5)
        np.fill((0, 0, 0))
        np.write()
