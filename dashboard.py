def dashboardwindow(name, avatarurl, status, steamid64, picostatus):
    """
    Create a function to run the main dashboard window
    """
    import sys
    from getuserfriendlist import get_friend_usernames
    from getnewgame import getrecommendedgames
    # create a try axcept because otherwise the back button would give a error while importing itself
    try:
        from analytics import analytics
    except:
        pass

    from getmostplayedgameself import getmostplayedgamemyself
    from getmostplayedgenres import meest_gespeelde_genres

    friendlist = get_friend_usernames(steamid64)
    if friendlist == 10:
        print("Kan uw steam profiel niet ophalen...")
        print("Zorg ervoor dat u uw steamprofiel op openbaar heeft staan")
        sys.exit(1)
    # create a error message for if the steam profile is on private

    else:
        if friendlist == 0:
            friendlist = ['', 0]
            onlinefriends = 0
        else:
            onlinefriends = friendlist[1] + len(friendlist[0])

    # create a list for easy acces to the friendlist later on

    # This file was generated by the Tkinter Designer by Parth Jadhav
    # https://github.com/ParthJadhav/Tkinter-Designer

    from pathlib import Path
    import tkinter as tk
    from PIL import Image, ImageTk
    from io import BytesIO
    import requests
    from sys import platform

    def relative_to_assets(path: str) -> Path:
        """
            Create a function for the path to the assets
        """
        return ASSETS_PATH / Path(path)

    def add_image_to_canvas1(canvas, image_path, x, y, width, height):
        """
            Create a function to handle the placing of images on a canvas
        """
        # Load the image and resize it
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height))

        # Create a PhotoImage object from the resized image
        tk_image = ImageTk.PhotoImage(resized_image)

        # Create an image item at the specified coordinates
        canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
        return tk_image

    def add_urlimage_to_canvas(canvas, image_path, x, y, width, height):
        """
        Create a function that places url images on the canvas, profile pictures etc
        """
        # Download the image from the URL
        response = requests.get(image_path)
        image_data = BytesIO(response.content)

        # Load the image and resize it
        original_image = Image.open(image_data)
        resized_image = original_image.resize((width, height))

        # Create a PhotoImage object from the resized image
        tk_image = ImageTk.PhotoImage(resized_image)

        # Create an image item at the specified coordinates
        canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
        return tk_image


    def friends_on_LED(): # functie om het aantal online vrienden te verkrijgen
        """
        This function controls the noepixel based on the total of online friends and displays a certain LEDS based on that.
        """
        from getuserfriendlist import get_friend_usernames
        var = get_friend_usernames(steamid64)
        friend_list_names = len(var[0])
        friend_list_count = var[1]
        friend_list = friend_list_names + friend_list_count
        return friend_list

    if picostatus:
        try:
            from serial.tools import list_ports
            import serial

            available_ports = list_ports.comports()
            if not available_ports:
                print("[ERROR] Geen serial ports gevonden!")
                pass

            selected_port = available_ports[0].device

            with serial.Serial(port=selected_port, baudrate=115200, bytesize=8, parity='N', stopbits=1,
                               timeout=1) as serial_port:
                if serial_port.isOpen():
                    data = f"O{friends_on_LED()}\r"
                    serial_port.write(data.encode())
                serial_port.close()

        except:
            pass



    def close_pico():
        """
        THis is code controls the components connected to the Pico. Its used to turn them off once the user has closed the dashboard.
        """
        import serial
        from serial.tools import list_ports
        import time


        available_ports = list_ports.comports()
        if not available_ports:
            print("Serial ports afgesloten!")
            exit()

        selected_port = available_ports[0].device

        with serial.Serial(port=selected_port, baudrate=115200, bytesize=8, parity='N', stopbits=1,
                           timeout=1) as serial_port:
            if serial_port.isOpen():

                serial_port.write(b'exec(open("main.py").read())\r\n')
                serial_port.write(b'\x03')
                time.sleep(1)

            else:
                serial_port.open()
                serial_port.write(b'exec(open("main.py").read())\r\n')

    def moreinfodashboard():
        """
            Create the moreinfo button, if this button is clicked you go to the analytics window
        """
        window.destroy()
        analytics(name, avatarurl, status, steamid64, picostatus)


    # Check on what platform the user is, ctypes.windll only works on windows and gives a error when on linux or mac
    if platform == "linux" or platform == "linux2":
        pass
    elif platform == "darwin":
        pass
    elif platform == "win32":
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(True)

    # from tkinter import *
    # Explicit imports to satisfy Flake8
    from tkinter import Tk, Canvas, Entry, Button, PhotoImage

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("assets/frame1")

    window = Tk()

    window.geometry("1920x1080")
    window.configure(bg="#FFFFFF")
    window.title(f"Steam | Er zijn momenteel {onlinefriends} vrienden online")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=1080,
        width=1920,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        1920.0,
        1080.0,
        fill="#102431",
        outline="")

    # place the steamlogo
    image_path = "assets\logo_steam.png"
    image = add_image_to_canvas1(canvas, image_path, x=55, y=40, width=267, height=77)

    canvas.create_text(
        1500.0,
        35.0,
        anchor="nw",
        text=name,
        fill="#FFFFFF",
        font=("Motiva Sans Medium", 40 * -1)
    )

    # Create a table for the online status, online, offline, away, cant get status
    if status == 0:
        canvas.create_text(
            1500.0,
            85.0,
            anchor="nw",
            text="Offline",
            fill="#CACACA",
            font=("Motiva Sans Regular", 24 * -1)
        )
    elif status == 1:
        canvas.create_text(
            1500.0,
            85.0,
            anchor="nw",
            text="Online",
            fill="#FFFFFF",
            font=("Motiva Sans Regular", 24 * -1)
        )
    elif status == 2:
        canvas.create_text(
            1500.0,
            85.0,
            anchor="nw",
            text="Bezig",
            fill="#CACACA",
            font=("Motiva Sans Regular", 24 * -1)
        )
    elif status == 3 or status == 4:
        canvas.create_text(
            1500.0,
            85.0,
            anchor="nw",
            text="Afwezig",
            fill="#CACACA",
            font=("Motiva Sans Regular", 24 * -1)
        )
    else:
        canvas.create_text(
            1497.0,
            85.0,
            anchor="nw",
            text=f"Kan status niet ophalen {status}",
            fill="#CACACA",
            font=("Motiva Sans Regular", 24 * -1)
        )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        270.0,
        629.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#0D131B",
        fg="#000716",
        highlightthickness=0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        1203.5,
        629.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#0D131B",
        fg="#000716",
        highlightthickness=0
    )

    canvas.create_text(
        56.0,
        178.0,
        anchor="nw",
        text="Online vrienden:",
        fill="#FFFFFF",
        font=("Motiva Sans Medium", 40 * -1)
    )

    canvas.create_text(
        574.0,
        178.0,
        anchor="nw",
        text="Ontdek meer over je gamegedrag:",
        fill="#FFFFFF",
        font=("Motiva Sans Medium", 40 * -1)
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: moreinfodashboard(),
        relief="flat"
    )
    button_4.place(
        x=1875.0,
        y=409.0,
        width=54.0,
        height=442.0
    )

    # If a friends name is too long or there are less then 8 people online this gets handled

    friendlistcount = len(friendlist[0]) -1

    if friendlistcount >= 0:
        if friendlist[0][0][0] is not None:
            if len(friendlist[0][0][0]) > 25:
                formatted_friend_name_not = friendlist[0][0][0]
                formatted_friend_name0 = formatted_friend_name_not[:22] + "..."
            else:
                formatted_friend_name0 = friendlist[0][0][0]

    if friendlistcount >= 1:
        if friendlist[0][1][0] is not None:
            if len(friendlist[0][1][0]) > 25:
                formatted_friend_name_not = friendlist[0][1][0]
                formatted_friend_name1 = formatted_friend_name_not[:22] + "..."
            else:
                formatted_friend_name1 = friendlist[0][1][0]

    if friendlistcount >= 2:
        if friendlist[0][2][0] is not None:
            if len(friendlist[0][2][0]) > 25:
                formatted_friend_name_not = friendlist[0][2][0]
                formatted_friend_name2 = formatted_friend_name_not[:22] + "..."
            else:
                formatted_friend_name2 = friendlist[0][2][0]

    if friendlistcount >= 3:
        if friendlist[0][3][0] is not None:
            if len(friendlist[0][3][0]) > 25:
                formatted_friend_name_not = friendlist[0][3][0]
                formatted_friend_name3 = formatted_friend_name_not[:22] + "..."
            else:
                formatted_friend_name3 = friendlist[0][3][0]

    if friendlistcount >= 4:
        if friendlist[0][4][0] is not None:
            if len(friendlist[0][4][0]) > 25:
                formatted_friend_name_not = friendlist[0][4][0]
                formatted_friend_name4 = formatted_friend_name_not[:22] + "..."
            else:
                formatted_friend_name4 = friendlist[0][4][0]

    if friendlistcount >= 5:
        if friendlist[0][5][0] is not None:
            if len(friendlist[0][5][0]) > 25:
                formatted_friend_name_not = friendlist[0][5][0]
                formatted_friend_name5 = formatted_friend_name_not[:22] + "..."
            else:
                formatted_friend_name5 = friendlist[0][5][0]

    if friendlistcount >= 6:
        if friendlist[0][6][0] is not None:
            if len(friendlist[0][6][0]) > 25:
                formatted_friend_name_not = friendlist[0][6][0]
                formatted_friend_name6 = formatted_friend_name_not[:22] + "..."
            else:
                formatted_friend_name6 = friendlist[0][6][0]

    if friendlistcount >= 7:
        if friendlist[0][7][0] is not None:
            if len(friendlist[0][7][0]) > 25:
                formatted_friend_name_not = friendlist[0][7][0]
                formatted_friend_name7 = formatted_friend_name_not[:22] + "..."
            else:
                formatted_friend_name7 = friendlist[0][7][0]


    if friendlist == 0:
        canvas.create_text(
            78.0,
            985.0,
            anchor="nw",
            text=f"Er zijn momenteel geen vrienden online",
            fill="#C7D5E0",
            font=("Motiva Sans Medium", 20 * -1)
        )
        # If there are no friends on the friendlist create a nice message
    else:
        # Otherwise check if the element exists and place it
        if len(friendlist[0]) >= 1:
            canvas.create_text(
                86.0,
                260.0,
                # 270,

                anchor="nw",
                text=formatted_friend_name0,
                fill="#FFFFFF",
                font=("Motiva Sans Medium", 28 * -1)
            )

            entry_image_3 = PhotoImage(
                file=relative_to_assets("entry_3.png"))
            entry_bg_3 = canvas.create_image(
                61.5,
                287.5,
                image=entry_image_3
            )
            entry_3 = Entry(
                bd=0,
                bg="#66C0F4",
                fg="#000716",
                highlightthickness=0
            )
            if friendlist[0][0][2] is not None:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    291.0,
                    anchor="nw",
                    text=f"Playing {friendlist[0][0][2]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans Regular", 20 * -1)
                )
            else:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    291.0,
                    anchor="nw",
                    text=f"{friendlist[0][0][1]}",
                    fill="#CACACA",
                    font=("Motiva Sans Regular", 20 * -1)
                )


        if len(friendlist[0]) >= 2:
            canvas.create_text(
                86.0,
                351.0,
                anchor="nw",
                text=formatted_friend_name1,
                fill="#FFFFFF",
                font=("Motiva Sans Medium", 28 * -1)
            )

            entry_image_4 = PhotoImage(
                file=relative_to_assets("entry_4.png"))
            entry_bg_4 = canvas.create_image(
                61.5,
                378.5,
                image=entry_image_4
            )
            entry_4 = Entry(
                bd=0,
                bg="#66C0F4",
                fg="#000716",
                highlightthickness=0
            )
            if friendlist[0][1][2] is not None:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    382.0,
                    anchor="nw",
                    text=f"Playing {friendlist[0][1][2]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans Regular", 20 * -1)
                )
            else:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    382.0,
                    anchor="nw",
                    text=f"{friendlist[0][1][1]}",
                    fill="#CACACA",
                    font=("Motiva Sans Regular", 20 * -1)
                )

        if len(friendlist[0]) >= 3:
            canvas.create_text(
                86.0,
                443.0,
                anchor="nw",
                text=formatted_friend_name2,
                fill="#FFFFFF",
                font=("Motiva Sans Medium", 28 * -1)
            )

            entry_image_5 = PhotoImage(
                file=relative_to_assets("entry_5.png"))
            entry_bg_5 = canvas.create_image(
                61.5,
                469.5,
                image=entry_image_5
            )
            entry_5 = Entry(
                bd=0,
                bg="#66C0F4",
                fg="#000716",
                highlightthickness=0
            )
            if friendlist[0][2][2] is not None:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    474.0,
                    anchor="nw",
                    text=f"Playing {friendlist[0][2][2]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans Regular", 20 * -1)
                )
            else:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    474.0,
                    anchor="nw",
                    text=f"{friendlist[0][2][1]}",
                    fill="#CACACA",
                    font=("Motiva Sans Regular", 20 * -1)
                )
        if len(friendlist[0]) >= 4:
            canvas.create_text(
                86.0,
                531.0,
                anchor="nw",
                text=formatted_friend_name3,
                fill="#FFFFFF",
                font=("Motiva Sans Medium", 28 * -1)
            )

            entry_image_6 = PhotoImage(
                file=relative_to_assets("entry_6.png"))
            entry_bg_6 = canvas.create_image(
                61.5,
                560.5,
                image=entry_image_6
            )
            entry_6 = Entry(
                bd=0,
                bg="#66C0F4",
                fg="#000716",
                highlightthickness=0
            )
            if friendlist[0][3][2] is not None:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    562.0,
                    anchor="nw",
                    text=f"Playing {friendlist[0][3][2]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans Regular", 20 * -1)
                )
            else:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    562.0,
                    anchor="nw",
                    text=f"{friendlist[0][3][1]}",
                    fill="#CACACA",
                    font=("Motiva Sans Regular", 20 * -1)
                )
        if len(friendlist[0]) >= 5:

            canvas.create_text(
                86.0,
                624.0,
                anchor="nw",
                text=formatted_friend_name4,
                fill="#FFFFFF",
                font=("Motiva Sans Medium", 28 * -1)
            )

            entry_image_7 = PhotoImage(
                file=relative_to_assets("entry_7.png"))
            entry_bg_7 = canvas.create_image(
                61.5,
                651.5,
                image=entry_image_7
            )
            entry_7 = Entry(
                bd=0,
                bg="#66C0F4",
                fg="#000716",
                highlightthickness=0
            )
            if friendlist[0][4][2] is not None:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    654.0,
                    anchor="nw",
                    text=f"Playing {friendlist[0][4][2]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans Regular", 20 * -1)
                )
            else:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    654.0,
                    anchor="nw",
                    text=f"{friendlist[0][4][1]}",
                    fill="#CACACA",
                    font=("Motiva Sans Regular", 20 * -1)
                )
        if len(friendlist[0]) >= 6:

            canvas.create_text(
                86.0,
                715.0,
                anchor="nw",
                text=formatted_friend_name5,
                fill="#FFFFFF",
                font=("Motiva Sans Medium", 28 * -1)
            )

            entry_image_8 = PhotoImage(
                file=relative_to_assets("entry_8.png"))
            entry_bg_8 = canvas.create_image(
                61.5,
                742.5,
                image=entry_image_8
            )
            entry_8 = Entry(
                bd=0,
                bg="#66C0F4",
                fg="#000716",
                highlightthickness=0
            )
            if friendlist[0][5][2] is not None:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    746.0,
                    anchor="nw",
                    text=f"Playing {friendlist[0][5][2]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans Regular", 20 * -1)
                )
            else:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    746.0,
                    anchor="nw",
                    text=f"{friendlist[0][5][1]}",
                    fill="#CACACA",
                    font=("Motiva Sans Regular", 20 * -1)
                )
        if len(friendlist[0]) >= 7:
            canvas.create_text(
                86.0,
                806.0,
                anchor="nw",
                text=formatted_friend_name6,
                fill="#FFFFFF",
                font=("Motiva Sans Medium", 28 * -1)
            )

            entry_image_9 = PhotoImage(
                file=relative_to_assets("entry_9.png"))
            entry_bg_9 = canvas.create_image(
                61.5,
                833.5,
                image=entry_image_9
            )
            entry_9 = Entry(
                bd=0,
                bg="#66C0F4",
                fg="#000716",
                highlightthickness=0
            )
            if friendlist[0][6][2] is not None:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    837.0,
                    anchor="nw",
                    text=f"Playing {friendlist[0][6][2]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans Regular", 20 * -1)
                )
            else:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    837.0,
                    anchor="nw",
                    text=f"{friendlist[0][6][1]}",
                    fill="#CACACA",
                    font=("Motiva Sans Regular", 20 * -1)
                )
        if len(friendlist[0]) >= 8:

            canvas.create_text(
                86.0,
                897.0,
                anchor="nw",
                text=formatted_friend_name7,
                fill="#FFFFFF",
                font=("Motiva Sans Medium", 28 * -1)
            )

            entry_image_10 = PhotoImage(
                file=relative_to_assets("entry_10.png"))
            entry_bg_10 = canvas.create_image(
                61.5,
                924.5,
                image=entry_image_10
            )
            entry_10 = Entry(
                bd=0,
                bg="#66C0F4",
                fg="#000716",
                highlightthickness=0
            )
            if friendlist[0][7][2] is not None:
                canvas.create_text(
                    86.0,
                    928.0,
                    anchor="nw",
                    text=f"Playing {friendlist[0][7][2]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans Regular", 20 * -1)
                )
            else:
                canvas.create_text(
                    86.0,
                    # 270.0,
                    928.0,
                    anchor="nw",
                    text=f"{friendlist[0][7][1]}",
                    fill="#CACACA",
                    font=("Motiva Sans Regular", 20 * -1)
                )

        canvas.create_text(
            112.0,
            985.0,
            anchor="nw",
            text=f"Nog {friendlist[1]} andere vrienden online",
            fill="#C7D5E0",
            font=("Motiva Sans Medium", 20 * -1)
        )
        # If there are more then 8 people online display the remaining people here

    entry_image_11 = PhotoImage(
        file=relative_to_assets("entry_11.png"))
    entry_bg_11 = canvas.create_image(
        1201.0,
        391.0,
        image=entry_image_11
    )
    entry_11 = Entry(
        bd=0,
        bg="#2A475E",
        fg="#000716",
        highlightthickness=0
    )

    entry_image_12 = PhotoImage(
        file=relative_to_assets("entry_12.png"))
    entry_bg_12 = canvas.create_image(
        664.5,
        391.0,
        image=entry_image_12
    )
    entry_12 = Entry(
        bd=0,
        bg="#66C0F4",
        fg="#000716",
        highlightthickness=0
    )

    canvas.create_text(
        697.0,
        309.0,
        anchor="nw",
        text="Deze game heb je het meeste gespeeld",
        fill="#FAFAFA",
        font=("Motiva Sans Medium", 28 * -1)
    )
    # get the most played game

    mostplayedgamemyself = getmostplayedgamemyself(steamid64)
    if mostplayedgamemyself == "Het ophalen van de favoriete game is niet gelukt.":
        canvas.create_text(
            697.0,
            375.0,
            anchor="nw",
            text="Het ophalen van de favoriete game is niet gelukt.",
            fill="#FFFFFF",
            font=("Motiva Sans Bold", 30 * -1)
        )
        # create a nice message if it has failed (user lockdown)
    else:
        if len(mostplayedgamemyself) >= 1:
            try:
                canvas.create_text(
                    697.0,
                    370.0,
                    anchor="nw",
                    text=mostplayedgamemyself[0][0],
                    fill="#FFFFFF",
                    font=("Motiva Sans Bold", 48 * -1)
                )
                canvas.create_text(
                    697.0,
                    425.0,
                    anchor="nw",
                    text=f"{int(mostplayedgamemyself[0][1] / 60)} hours on record",
                    fill="#bbbbbb",
                    font=("Motiva Sans General", 24 * -1)
                )
            except:
                pass
            # If this still fails dont let the program crash

    entry_image_13 = PhotoImage(
        file=relative_to_assets("entry_13.png"))
    entry_bg_13 = canvas.create_image(
        1201.0,
        869.0,
        image=entry_image_13
    )
    entry_13 = Entry(
        bd=0,
        bg="#2A475E",
        fg="#000716",
        highlightthickness=0
    )

    entry_image_14 = PhotoImage(
        file=relative_to_assets("entry_14.png"))
    entry_bg_14 = canvas.create_image(
        664.5,
        869.0,
        image=entry_image_14
    )
    entry_14 = Entry(
        bd=0,
        bg="#66C0F4",
        fg="#000716",
        highlightthickness=0
    )

    canvas.create_text(
        697.0,
        787.0,
        anchor="nw",
        text="Misschien is deze game iets voor jou",
        fill="#FAFAFA",
        font=("Motiva Sans Medium", 28 * -1)
    )
    recommended_games = getrecommendedgames(steamid64)

    # If the game is too long shorten it and place ... after
    if len(recommended_games[0]) > 32:
        formatted_game_name_not = recommended_games[0]
        formattedgamename123 = formatted_game_name_not[:29] + "..."
    else:
        formattedgamename123 = recommended_games[0]

    canvas.create_text(
        697.0,
        851.0,
        anchor="nw",
        text=f"{formattedgamename123}",
        fill="#FFFFFF",
        font=("Motiva Sans Bold", 48 * -1)
    )

    entry_image_15 = PhotoImage(
        file=relative_to_assets("entry_15.png"))
    entry_bg_15 = canvas.create_image(
        1201.0,
        630.0,
        image=entry_image_15
    )
    entry_15 = Entry(
        bd=0,
        bg="#2A475E",
        fg="#000716",
        highlightthickness=0
    )
    entry_image_16 = PhotoImage(
        file=relative_to_assets("entry_16.png"))
    entry_bg_16 = canvas.create_image(
        664.5,
        630.0,
        image=entry_image_16
    )
    entry_16 = Entry(
        bd=0,
        bg="#66C0F4",
        fg="#000716",
        highlightthickness=0
    )

    canvas.create_text(
        697.0,
        548.0,
        anchor="nw",
        text="Deze genre is echt jouw favoriet",
        fill="#FAFAFA",
        font=("Motiva Sans Medium", 28 * -1)
    )

    genresai = meest_gespeelde_genres(steamid64)

    # display the favourite genre if exists
    if len(genresai) >= 1:
        canvas.create_text(
            697.0,
            605.0,
            anchor="nw",
            text=f"{genresai[0][0]}",
            fill="#FFFFFF",
            font=("Motiva Sans Bold", 48 * -1)
        )
        canvas.create_text(
            697.0,
            660.0,
            anchor="nw",
            text=f"{int(genresai[0][1] / 60)} hours on record",
            fill="#bbbbbb",
            font=("Motiva Sans General", 24 * -1)
        )
    else:
        canvas.create_text(
            697.0,
            605.0,
            anchor="nw",
            text=f"Er is geen speeltijd gevonden voor deze gebruiker \nCheck of de gebruiker zijn profiel op openbaar heeft",
            fill="#dadada",
            font=("Motiva Sans regular", 24 * -1)
        )

    image_path = avatarurl
    image1 = add_urlimage_to_canvas(canvas, image_path, x=1388, y=30, width=89, height=89)
    # create a profile picture

    # place all more info buttons
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: moreinfodashboard(),
        relief="flat"
    )
    button_1.place(
        x=1522.0,
        y=422.0,
        width=205.0,
        height=54.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: moreinfodashboard(),
        relief="flat"
    )
    button_2.place(
        x=1522.0,
        y=662.0,
        width=205.0,
        height=54.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: moreinfodashboard(),
        relief="flat"
    )
    button_3.place(
        x=1522.0,
        y=901.0,
        width=205.0,
        height=54.0
    )
    window.resizable(False, False)

    window.mainloop()
    friends_on_LED()
    close_pico()


# for testing purposes the window can also be run directly
# dashboardwindow("testuser", "https://avatars.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg", 1, "76561198343709779"  )
