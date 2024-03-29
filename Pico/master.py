from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from RC522_read import MFRC522, getblockvalue
import utime
import neopixel
import time

"""
This is the main code for the components connected to the Pico. It is used to display messages and control the neopixel during the login process for Steam. 
Additionally, it controls the neopixel according to online friends after the user has successfully logged in.

"""

# Configure parameters for the NeoPixel
np = neopixel.NeoPixel(Pin(21), 30)
brightness = 1  # Set the brightness to 50%
num_leds = 30

# Configure parameters for the RFID
reader = MFRC522(sck=10, mosi=11, miso=12, rst=14, cs=15, spi_id=1)

# Configure parameters for the LCD
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)


# Function to create a white wave on the neopixel
def whitewave():
    animation_length = 5
    sleep_time = 0.03
    for i in range(num_leds - animation_length + 1):
        np.fill((0, 0, 0)) # Set all LEDs to black
        # Set the animation color for the current position
        for j in range(animation_length):
            position = i + j
            np[position] = (int(255 * brightness), int(255 * brightness), int(255 * brightness))  # White color

        np.write()
        utime.sleep(sleep_time)

    for i in range(num_leds - 1, animation_length - 1, -1):
        np.fill((0, 0, 0)) # Set all LEDs to black
        # Set the animation color for the current position
        for j in range(animation_length):
            position = i - j
            np[position] = (int(255 * brightness), int(255 * brightness), int(255 * brightness))  # White color

        np.write()
        utime.sleep(sleep_time)


# Function to create a green wave on the neopixel
def greensucces():
    for i in range(15):
        np.fill((0, 0, 0)) # Set all LEDs to black
        # Set the green component for the LEDs in the middle and create a wave
        for j in range(i + 1):
            np[14 - j] = [0, int(255 * brightness), 0]
            np[15 + j] = [0, int(255 * brightness), 0]
        np.write()
        utime.sleep(0.07)  # Adjust the sleep time to control the speed of the animation
    utime.sleep(0.1)


# Function to create a red wave on the neopixel
def rederror():
    for i in range(15):
        np.fill((0, 0, 0)) # Set all LEDs to black
        # Set the green component for the LEDs in the middle and create a wave
        for j in range(i + 1):
            np[14 - j] = [int(255 * brightness), 0, 0]
            np[15 + j] = [int(255 * brightness), 0, 0]
        np.write()
        utime.sleep(0.03)  # Adjust the sleep time to control the speed of the animation
    utime.sleep(0.2)


# Function to create a pulsing effect on the neopixel
def pulsing():
    loop123 = True
    range123 = [0.79, 0.78, 0.77, 0.76, 0.75, 0.74, 0.73, 0.72, 0.71, 0.7, 0.69, 0.68, 0.67, 0.66, 0.65, 0.64, 0.63,
                0.62, 0.61, 0.6, 0.59, 0.58, 0.57, 0.56, 0.55, 0.54, 0.53, 0.52, 0.51, 0.5, 0.49, 0.48, 0.47, 0.46,
                0.45, 0.44, 0.43, 0.42, 0.41, 0.4, 0.39, 0.38, 0.37, 0.36, 0.35, 0.34, 0.33, 0.32, 0.31, 0.3, 0.29,
                0.28, 0.27, 0.26, 0.25, 0.24, 0.23, 0.22, 0.21, 0.2, 0.19, 0.18, 0.17, 0.16, 0.15, 0.14, 0.13, 0.12,
                0.11, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
    for i in range123:
        utime.sleep(0.005)
        np.fill([0, 0, int(255 * i)])
        np.write()
    listreverse = reversed(range123)
    for i in listreverse:
        utime.sleep(0.005)
        np.fill([0, 0, int(255 * i)])
        np.write()


output = 0

loop = 0
loop1 = 0
friendlist = 100
loop1234 = True

# print("debug1")
while True:  # Outer loop for continuous operation
    gelukt = False  # Reset gelukt flag for each iteration

    while not gelukt:
        lcd.move_to(0, 0)
        lcd.putstr("  TAP TO LOGIN  ")
        lcd.move_to(0, 1)
        lcd.putstr("   SteamCard.   ")
        pulsing()
        lcd.move_to(0, 1)
        lcd.putstr("   SteamCard..  ")
        lcd.move_to(0, 1)
        lcd.putstr("   SteamCard... ")
        pulsing()

        try:
            reader.init()
            (stat, tag_type) = reader.request(reader.REQIDL)
            if stat == reader.OK:
                (stat, uid) = reader.SelectTagSN()
                if stat == reader.OK:
                    defaultKey = [255, 255, 255, 255, 255, 255]
                    var = reader.MFRC522_DumpClassic1K(uid, Start=4, End=6, keyA=defaultKey)
                    # print("debug auth")
                    while loop < 2:
                        if loop < 2:
                            # Display messages for authentication
                            lcd.move_to(0, 0)
                            lcd.putstr(" AUTHENTICATING ")
                            if output > 0:
                                lcd.move_to(0, 1)
                            lcd.putstr(" Please wait   ")
                            whitewave()
                            lcd.move_to(0, 1)
                            lcd.putstr(" Please wait.  ")
                            whitewave()
                            lcd.move_to(0, 1)
                            lcd.putstr(" Please wait.. ")
                            lcd.move_to(0, 1)
                            lcd.putstr(" Please wait...")
                            whitewave()
                            lcd.move_to(0, 1)
                            loop = loop + 1
                    else: # error if no user is found
                        if friendlist == 10:
                            lcd.move_to(0, 1)
                            lcd.clear()
                            lcd.putstr("     ERROR       ")
                            lcd.move_to(0, 1)
                            lcd.putstr(" no user found   ")
                            loop3 = 0
                            while loop3 < 5:
                                rederror()
                                loop3 = loop3 + 1
                            gelukt = False
                            loop = 0
                            loop1 = 0

                        else:
                            steamid64 = getblockvalue()
                            print(f"steamid64: {steamid64}")
                            gelukt = True
                            if gelukt == True:
                                # Display success message for login
                                lcd.move_to(0, 0)
                                lcd.clear()
                                lcd.putstr(" LOGIN SUCCESS  ")
                                lcd.move_to(0, 1)
                                lcd.putstr("retrieve profile")
                                loop5 = 0
                                while loop5 < 5:
                                    greensucces()
                                    loop5 = loop5 + 1

                                # turn off all LEDs between succes and showing online friends on the neopixel
                                np.fill((0, 0, 0))
                                np.write()
                                time.sleep(3.0)

                                gelukt = False
                                loop = 0
                                loop1 = 0
                    output = 1

                    gelukt = True  # Set gelukt flag to exit the outer loop


        except Exception as e:
            print(f"Error: {e}")
            # Add any error handling or logging if needed

    # Wait for data (online friends) from the serial connection
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
