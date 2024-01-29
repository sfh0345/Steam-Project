import machine
import neopixel
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd

"""
This is the code to deactivate the components connected to the Pico, which are the LCD screen and the NeoPixel. 
This code is executed once the user has closed the dashboard.

"""

# Configure parameters for the LCD
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Configure parameters for the NeoPixels
np = neopixel.NeoPixel(Pin(9), 8)


# Function that turns off the LCD
def turn_lcd_off():
    lcd.backlight_off() # turn off the LCD


# Function that turns off the Neopixel
def turn_neopixel_off():
    np.fill((0, 0, 0))  # turn of all pixels (black)
    np.write() # Update the noepixel


# Call the functions
turn_lcd_off()
turn_neopixel_off()