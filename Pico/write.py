from RC522_write import MFRC522

"""
This code is used to write a SteamID onto the keycard for automatic login using NFC.

"""

# Function to show the uid of the keycard
def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring


# Function to write the SteamID onto a keycard
def write_steamid_to_card(reader, key, steam_id, blockid):
    print("")
    print("Please place card on reader")
    print("")

    try:
        while True:
            (stat, tag_type) = reader.request(reader.REQIDL)

            if stat == reader.OK:
                (stat, uid) = reader.SelectTagSN()
                if stat == reader.OK:
                    print("Card detected: %s" % uidToString(uid))
                    print("Writing SteamID: " + str(steam_id_1)[:-7] + str(steam_id_2)[:-8] + " to keycard")

                    absoluteBlock = blockid
                    value = [ord(x) for x in str(steam_id)]

                    status = reader.auth(reader.AUTHENT1A, absoluteBlock, key, uid)

                    if status == reader.OK:
                        status = reader.write(absoluteBlock, value)

                        if status == reader.OK:
                            reader.MFRC522_DumpClassic1K(uid, keyA=key)
                            print("")
                            print("Done: write successful!")
                        else:
                            print("Unable to write to card!")
                    else:
                        pass
                    break
    except KeyboardInterrupt:
        print("Bye")


# Setup for the RFID-reader
reader = MFRC522(sck=10, mosi=11, miso=12, rst=14, cs=15, spi_id=1)

# Key for auth
key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# split the SteamID: 76561199022018738

steam_id_1 = 7656119900000000

steam_id_2 = 2201873800000000

# write the first 8 bytes of the SteamID to the keycard
write_steamid_to_card(reader, key, steam_id_1, 4)

# reset the module and write the last 8 bytes to the keycard
reader.init()
write_steamid_to_card(reader, key, steam_id_2, 5)