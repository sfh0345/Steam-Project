from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
from RC522_read import MFRC522, getblockvalue
import time

"""
From the 1602A LCD Datasheet. The I2C 1602 LCD module is a 2 line by 16 character display interfaced to an I2C daughter board.
Specifications: 2 lines by 16 characters
I2C Address Range: 0x20 to 0x27 (Default=0x27, addressable) 
Operating Voltage: 5 Vdc 
Contrast: Adjustable by potentiometer on I2C interface
Size: 80mm x 36mm x 20 mm
Viewable area: 66mm x 16mm 

Drivers provided by https://www.circuitschools.com/
Note: Adjust the potentiometer when you do not see any characters on the display 
"""

reader = MFRC522(sck=10, mosi=11, miso=12, rst=14, cs=15, spi_id=1)
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
# print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))

output = 0
gelukt = False
loop = 0
loop1 = 0
nfccard = False
friendlist = 100
loop1234 = True

# print("debug1")
while True:  # Outer loop for continuous operation
    gelukt = False  # Reset gelukt flag for each iteration

    while not gelukt:
        lcd.move_to(0, 0)
        lcd.putstr("  TAP TO LOGIN  ")
        if output > 0:
            lcd.move_to(0, 1)
        lcd.putstr("   SteamCard.   ")
        time.sleep(0.5)
        lcd.move_to(0, 1)
        lcd.putstr("   SteamCard..  ")
        time.sleep(0.5)
        lcd.move_to(0, 1)
        lcd.putstr("   SteamCard... ")
        time.sleep(0.0)
        lcd.move_to(0, 1)
        output = 1

        try:
            reader.init()
            (stat, tag_type) = reader.request(reader.REQIDL)
            if stat == reader.OK:
                (stat, uid) = reader.SelectTagSN()
                if stat == reader.OK:
                    defaultKey = [255, 255, 255, 255, 255, 255]
                    var = reader.MFRC522_DumpClassic1K(uid, Start=4, End=6, keyA=defaultKey)
                    # print("debug auth")
                    while loop < 3:
                        if loop < 3:
                            lcd.move_to(0, 0)
                            lcd.putstr(" AUTHENTICATING ")
                            if output > 0:
                                lcd.move_to(0, 1)
                            lcd.putstr(" Please wait   ")
                            time.sleep(0.1)
                            lcd.move_to(0, 1)
                            lcd.putstr(" Please wait.  ")
                            time.sleep(0.1)
                            lcd.move_to(0, 1)
                            lcd.putstr(" Please wait.. ")
                            time.sleep(0.1)
                            lcd.move_to(0, 1)
                            lcd.putstr(" Please wait...")
                            time.sleep(0.1)
                            lcd.move_to(0, 1)
                            loop = loop + 1
                        # error als er geen user gevonden word
                    else:
                        if friendlist == 10:
                            lcd.move_to(0, 1)
                            lcd.clear()
                            lcd.putstr("     ERROR       ")
                            lcd.move_to(0, 1)
                            lcd.putstr(" no user found   ")
                            time.sleep(5)
                            gelukt = False
                            loop = 0
                            nfccard = False
                            loop1 = 0

                        else:
                            steamid64 = getblockvalue()
                            print(steamid64)
                            gelukt = True
                            if gelukt == True:
                                lcd.move_to(0, 1)
                                lcd.clear()
                                lcd.putstr("INLOGGEN SUCCES")
                                lcd.move_to(0, 1)
                                lcd.putstr("Ophalen profiel")
                                gelukt = False
                                loop = 0
                                nfccard = False
                                loop1 = 0
                                time.sleep(3.5)
                    output = 1

                    gelukt = True  # Set gelukt flag to exit the outer loop


        except Exception as e:
            print(f"Error: {e}")
            # Add any error handling or logging if needed
