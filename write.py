from rc522 import MFRC522

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

def write_steam_id_to_card(reader, key, steam_id):
    print("")
    print("Please place card on reader")
    print("")

    try:
        while True:
            (stat, tag_type) = reader.request(reader.REQIDL)

            if stat == reader.OK:
                (stat, uid) = reader.SelectTagSN()
                if stat == reader.OK:
                    print("Card detected %s" % uidToString(uid))
                    print("SteamID: {}".format(steam_id))

                    absoluteBlock = 4
                    value = [ord(x) for x in str(steam_id)]

                    status = reader.auth(reader.AUTHENT1A, absoluteBlock, key, uid)

                    if status == reader.OK:
                        status = reader.write(absoluteBlock, value)

                        if status == reader.OK:
                            print("Write successful")
                            reader.MFRC522_DumpClassic1K(uid, keyA=key)
                            print("Done")
                        else:
                            print("Unable to write")
                    else:
                        print("Authentication error for writing")
                    break
    except KeyboardInterrupt:
        print("Bye")

# SteamID to write
steam_id_to_write = 76561199022018738

# Setup for the RFID-reader
reader = MFRC522(sck=10, mosi=11, miso=12, rst=14, cs=15, spi_id=1)

# Key definition
key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# Write SteamID to keycard
write_steam_id_to_card(reader, key, steam_id_to_write)