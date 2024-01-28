import machine
import neopixel
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd

"""
Dit is de code om de componenten die op de Pico zijn aangesloten uit te schakelen, dit zijn het LCD-scherm en de NeoPixel. 
Deze code wordt uitgevoerd zodra de gebruiker het dashboard heeft afgesloten.

"""

# Configureer parameters voor het LCD-scherm
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Configureer parameters voor de NeoPixels
np = neopixel.NeoPixel(Pin(9), 8)



def turn_lcd_off():
    lcd.backlight_off() # schakel het LCD-scherm uit


def turn_neopixel_off():
    np.fill((0, 0, 0))  # schakel alle pixels uit(black)
    np.write() # Update de NeoPixel


turn_lcd_off()
turn_neopixel_off()
