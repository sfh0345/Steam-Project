import time
import neopixel
from machine import Pin

"""

This code controls the NeoPixel to display color patterns corresponding to the number of online friends.

"""

# Configure parameters for the NeoPixel
np = neopixel.NeoPixel(Pin(21), 30)

# Wait for data from the serial connection
while True:
    data = input()

    # Control Neopixel based on the specified conditions
    led_count = int(data[1:])

    # If there are no friends online
    if led_count < 1:
        # Blink all 30 leds in red indefinitely
        while True:
            for _ in range(5):
                np.fill((255, 0, 0))
                np.write()
                time.sleep(0.5)
                np.fill((0, 0, 0))
                np.write()
                time.sleep(0.5)

    # If between 1 and 30 friends are online
    elif 1 <= led_count <= 30:
        # Turn on a LED for every online friend
        while True:
            for index in range(led_count):
                np[index] = (255, 0, 255)
                np.write()
                time.sleep(0.2)

    # If there are more than 30 friends online / more friends online than LEDs on NeoPixel
    elif led_count > 30:
        # Turn on all LEDs on the Neopixel
        while True:
            for index in range(29):
                np[index] = (0, 255, 255)
                np.write()
                time.sleep(0.2)
            # Blink the last LED (30)
            while True:
                np[29] = (0, 255, 255)
                np.write()
                time.sleep(0.5)
                np[29] = (0, 0, 0)
                np.write()
                time.sleep(0.2)
