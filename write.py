from rc522 import MFRC522

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

def write_steam_id_to_card(reader, key, steam_id, blockid):
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
                    print("Writing SteamID to sector 2, block 1 (absolute block 9)")
                    print("SteamID: {}".format(steam_id))

                    absoluteBlock = blockid
                    value = [ord(x) for x in str(steam_id)]

                    status = reader.auth(reader.AUTHENT1A, absoluteBlock, key, uid)

                    if status == reader.OK:
                        status = reader.write(absoluteBlock, value)

                        if status == reader.OK:
                            print("Write successful")
                            reader.MFRC522_DumpClassic1K(uid, keyA=key)
                        else:
                            print("Unable to write")
                    else:
                        pass
                    break
    except KeyboardInterrupt:
        print("Bye")


# splits het SteamID
steam_id_to_write = 7656119900000000000
steam_id_to_write1 = 220187380000000000

# Setup voor de RFID-reader
reader = MFRC522(sck=10, mosi=11, miso=12, rst=14, cs=15, spi_id=1)

# definitie voor Key (auth?)
key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# schrijf de eerste 8 bytes van SteamID naar keycard
write_steam_id_to_card(reader, key, steam_id_to_write, 4)

# reset de module en schrijf de laatste 8 bytes naar keycard
reader.init()
write_steam_id_to_card(reader, key, steam_id_to_write1, 5)