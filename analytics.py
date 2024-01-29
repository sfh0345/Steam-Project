def analytics(name, avatarurl, status, steamid64):
    from pathlib import Path
    from analyticsophalen import analyticsmulticore
    import tkinter as tk
    from PIL import Image, ImageTk
    from io import BytesIO
    from getnewgame import getrecommendedgames
    import requests
    import datetime
    from getmostplayedgenres import meest_gespeelde_genres
    from sys import platform
    from getmostplayedgameself import getmostplayedgamemyself
    from Playtime_voorspelling import voorspel_playtime
    try:
        from dashboard import dashboardwindow
    except:
        pass

    # from tkinter import *
    # Explicit imports to satisfy Flake8
    from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


    OUTPUT_PATH2 = Path(__file__).parent
    ASSETS_PATH2 = OUTPUT_PATH2 / Path("assets/frame2/")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH2 / Path(path)

    def add_image_to_canvas(canvas, image_path, x, y, width, height):
        # Load the image and resize it
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height))

        # Create a PhotoImage object from the resized image
        tk_image = ImageTk.PhotoImage(resized_image)

        # Create an image item at the specified coordinates
        canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
        return tk_image

    def add_urlimage_to_canvas(canvas, image_path, x, y, width, height):
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

    if platform == "linux" or platform == "linux2":
        pass
    elif platform == "darwin":
        pass
    elif platform == "win32":
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(True)

    window = Tk()

    window.geometry("1920x1080")
    window.configure(bg = "#FFFFFF")
    window.title("Steam | Analytics dashboard")

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 1080,
        width = 1920,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        1920.0,
        1080.0,
        fill="#102431",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        232.0,
        341.0,
        image=entry_image_1
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("frame2/entry_3.png"))
    entry_bg_3 = canvas.create_image(
        436.5,
        822.5,
        image=entry_image_3
    )

    entry_image_30 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_9 = canvas.create_image(
        641.0,
        341.0,
        image=entry_image_30
    )

    entry_image_20 = PhotoImage(
        file=relative_to_assets("frame2/entry_7.png"))
    entry_bg_2 = canvas.create_image(
        315.0,
        705.0,
        image=entry_image_20
    )

    text_widget = Text(
        bd=0,
        bg="#33333D",
        fg="#FFFFFF",
        highlightthickness=0,
        wrap="word",  # zorg ervoor dat de woorden binnen de box blijven
        padx=7,  # padding op de box zodat de text niet buiten de box komt
        pady=10,  # padding op de box zodat de text niet butien de box komt
        font=("Motiva Sans Bold", 12),  # pas het font aan naar rubik
    )
    text_widget.place(
        x=77.0,
        y=681.0,
        width=476.0,
        height=48.0
    )

    canvas.create_text(
        67.0,
        614.0,
        anchor="nw",
        text="Expected playtime in hours",
        fill="#FFFFFF",
        font=("Motiva Sans Bold", 25 * -1)
    )

    canvas.create_text(
        67.0,
        641.5,
        anchor="nw",
        text="with linair regression",
        fill="#AAAAAA",
        font=("Motiva Sans regular", 20 * -1)

    )

    def searchlinair(entry):
        global lijstrecentenzoekopdrachten
        global entry_image_8888
        global entry_image_9999
        global entry_image_10000
        global entry_image_11
        global entry_image_12
        global entry_image_13

        if entry.strip() == "":
            text_widget.delete("1.0", "end")
        else:
            text_widget.delete("1.0", "end")

            gamename = entry
            voorspelde_uren = voorspel_playtime(gamename)
            gamename1 = gamename

            if len(gamename1) > 35:
                formatted_game_name1234 = gamename1[:32] + "..."
            else:
                formatted_game_name1234 = gamename1

            lijstrecentenzoekopdrachten = lijstrecentenzoekopdrachten[:2]
            lijstrecentenzoekopdrachten = [[formatted_game_name1234, voorspelde_uren]] + lijstrecentenzoekopdrachten

            # print(lijstrecentenzoekopdrachten)

            entry_image_8888 = PhotoImage(
                file=relative_to_assets("frame2/entry_8.png"))
            entry_bg_8888 = canvas.create_image(
                436.0,
                815.5,
                image=entry_image_8888
            )

            entry_image_9999 = PhotoImage(
                file=relative_to_assets("frame2/entry_9.png"))
            entry_bg_9999 = canvas.create_image(
                436.0,
                901.5,
                image=entry_image_9999
            )

            entry_image_10000 = PhotoImage(
                file=relative_to_assets("frame2/entry_10.png"))
            entry_bg_10000 = canvas.create_image(
                436.0,
                987.5,
                image=entry_image_10000
            )

            if lijstrecentenzoekopdrachten[0][1] == "--":
                text1 = canvas.create_text(
                    84.0,
                    796.0,
                    anchor="nw",
                    text=f"{lijstrecentenzoekopdrachten[0][0]}",
                    fill="#AAAAAA",
                    font=("Motiva Sans SemiBold", 29 * -1)
                )
                entry_image_11 = PhotoImage(
                    file=relative_to_assets("frame2/entry_11.png"))
                entry_bg_11 = canvas.create_image(
                    698.0,
                    816.0,
                    image=entry_image_11
                )
                text11 = canvas.create_text(
                    696.0,
                    814.0,
                    anchor="center",
                    text=f"{lijstrecentenzoekopdrachten[0][1]}",
                    fill="#FFFFFF",
                    justify="center",
                    font=("Motiva Sans SemiBold", 24 * -1)
                )
            else:
                text1 = canvas.create_text(
                    84.0,
                    796.0,
                    anchor="nw",
                    text=f"{lijstrecentenzoekopdrachten[0][0]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans SemiBold", 29 * -1)
                )
                entry_image_11 = PhotoImage(
                    file=relative_to_assets("frame2/entry_11.png"))
                entry_bg_11 = canvas.create_image(
                    698.0,
                    816.0,
                    image=entry_image_11
                )
                text11 = canvas.create_text(
                    696.0,
                    814.0,
                    anchor="center",
                    text=f"{lijstrecentenzoekopdrachten[0][1]}",
                    fill="#FFFFFF",
                    justify="center",
                    font=("Motiva Sans SemiBold", 24 * -1)
                )


            if lijstrecentenzoekopdrachten[1][1] == "--":
                text21 = canvas.create_text(
                    84.0,
                    882.0,
                    anchor="nw",
                    text=f"{lijstrecentenzoekopdrachten[1][0]}",
                    fill="#AAAAAA",
                    font=("Motiva Sans SemiBold", 29 * -1)
                )
                entry_image_12 = PhotoImage(
                    file=relative_to_assets("frame2/entry_12.png"))
                entry_bg_12 = canvas.create_image(
                    698.0,
                    902.0,
                    image=entry_image_12
                )

                text22 = canvas.create_text(
                    696.0,
                    900.0,
                    anchor="center",
                    text=f"{lijstrecentenzoekopdrachten[1][1]}",
                    fill="#FFFFFF",
                    justify="center",
                    font=("Motiva Sans SemiBold", 24 * -1)
                )
            else:
                text21 = canvas.create_text(
                    84.0,
                    882.0,
                    anchor="nw",
                    text=f"{lijstrecentenzoekopdrachten[1][0]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans SemiBold", 29 * -1)
                )
                entry_image_12 = PhotoImage(
                    file=relative_to_assets("frame2/entry_12.png"))
                entry_bg_12 = canvas.create_image(
                    698.0,
                    902.0,
                    image=entry_image_12
                )
                text22 = canvas.create_text(
                    696.0,
                    900.0,
                    anchor="center",
                    text=f"{lijstrecentenzoekopdrachten[1][1]}",
                    fill="#FFFFFF",
                    justify="center",
                    font=("Motiva Sans SemiBold", 24 * -1)
                )

            if lijstrecentenzoekopdrachten[2][1] == "--":
                text31 = canvas.create_text(
                    84.0,
                    968.0,
                    anchor="nw",
                    text=f"{lijstrecentenzoekopdrachten[2][0]}",
                    fill="#AAAAAA",
                    font=("Motiva Sans SemiBold", 29 * -1)
                )
                entry_image_13 = PhotoImage(
                    file=relative_to_assets("frame2/entry_13.png"))
                entry_bg_13 = canvas.create_image(
                    698.0,
                    988.0,
                    image=entry_image_13
                )

                text32 = canvas.create_text(
                    696.0,
                    986.0,
                    anchor="center",
                    text=f"{lijstrecentenzoekopdrachten[2][1]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans SemiBold", 24 * -1)
                )
            else:
                text31 = canvas.create_text(
                    84.0,
                    968.0,
                    anchor="nw",
                    text=f"{lijstrecentenzoekopdrachten[2][0]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans SemiBold", 29 * -1)
                )
                entry_image_13 = PhotoImage(
                    file=relative_to_assets("frame2/entry_13.png"))
                entry_bg_13 = canvas.create_image(
                    698.0,
                    988.0,
                    image=entry_image_13
                )

                text32 = canvas.create_text(
                    696.0,
                    986.0,
                    anchor="center",
                    text=f"{lijstrecentenzoekopdrachten[2][1]}",
                    fill="#FFFFFF",
                    font=("Motiva Sans SemiBold", 24 * -1)
                )






    button_image_2 = PhotoImage(
        file=relative_to_assets("frame2/button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: searchlinair(text_widget.get("1.0", tk.END).strip()),
        relief="flat"
    )
    button_2.place(
        x=575.0,
        y=681.0,
        width=230.0,
        height=50.0
    )

    entry_image_8 = PhotoImage(
        file=relative_to_assets("frame2/entry_8.png"))
    entry_bg_8 = canvas.create_image(
        436.0,
        815.5,
        image=entry_image_8
    )


    entry_image_9 = PhotoImage(
        file=relative_to_assets("frame2/entry_9.png"))
    entry_bg_9 = canvas.create_image(
        436.0,
        901.5,
        image=entry_image_9
    )


    entry_image_10 = PhotoImage(
        file=relative_to_assets("frame2/entry_10.png"))
    entry_bg_10 = canvas.create_image(
        436.0,
        987.5,
        image=entry_image_10
    )

    canvas.create_text(
        67.0,
        744.0,
        anchor="nw",
        text="Suggested games",
        fill="#FFFFFF",
        font=("Motiva Sans SemiBold", 20 * -1)
    )

    def mostplayedgamesself():
        global entry_image_11
        global entry_image_12
        global entry_image_13
        global lijstrecentenzoekopdrachten
        global text_var

        mostplayedgamesself = getmostplayedgamemyself(steamid64)
        if mostplayedgamesself == "Het ophalen van de favoriete game is niet gelukt." or len(mostplayedgamesself) < 1:

            canvas.create_text(
                84.0,
                792.0,
                anchor="nw",
                text=f"Er konden geen suggested games worden opgehaald",
                fill="#ffffff",
                font=("Motiva Sans SemiBold", 25 * -1)

            )

            canvas.create_text(
                84.0,
                816.0,
                anchor="nw",
                text=f"Check of het profiel op openbaar staat",
                fill="#aaaaaa",
                font=("Motiva Sans regular", 19 * -1)

            )

        else:

            lengtemostplayed = len(mostplayedgamesself)

            if len(mostplayedgamesself) >= 1:
                if len(mostplayedgamesself[0][0]) > 35:
                    formatted_game_name_not = mostplayedgamesself[0][0]
                    formatted_game_name01 = formatted_game_name_not[:32] + "..."
                else:
                    formatted_game_name01 = mostplayedgamesself[0][0]

            if len(mostplayedgamesself) >= 2:
                if len(mostplayedgamesself[1][0]) > 35:
                    formatted_game_name_not = mostplayedgamesself[1][0]
                    formatted_game_name11 = formatted_game_name_not[:32] + "..."
                else:
                    formatted_game_name11 = mostplayedgamesself[1][0]

            if len(mostplayedgamesself) >= 3:
                if len(mostplayedgamesself[2][0]) > 35:
                    formatted_game_name_not = mostplayedgamesself[2][0]
                    formatted_game_name21 = formatted_game_name_not[:32] + "..."
                else:
                    formatted_game_name21 = mostplayedgamesself[2][0]


            lengtemostplayedgames = len(mostplayedgamesself)

            if lengtemostplayedgames < 3:
                lengtemostplayedgames1 = lengtemostplayedgames
            else:
                lengtemostplayedgames1 = 3

            lijstrecentenzoekopdrachten = []

            for i in range(lengtemostplayedgames1):
                if i == 0:
                    gamename = formatted_game_name01
                if i == 1:
                    gamename = formatted_game_name11
                if i == 2:
                    gamename = formatted_game_name21

                lijstrecentenzoekopdrachten.append([gamename, voorspel_playtime(gamename)])

            if len(mostplayedgamesself) >= 1:

                if lijstrecentenzoekopdrachten[0][1] == "--":
                    text1 = canvas.create_text(
                        84.0,
                        796.0,
                        anchor="nw",
                        text=f"{lijstrecentenzoekopdrachten[0][0]}",
                        fill="#AAAAAA",
                        font=("Motiva Sans SemiBold", 29 * -1)
                    )
                    entry_image_11 = PhotoImage(
                        file=relative_to_assets("frame2/entry_11.png"))
                    entry_bg_11 = canvas.create_image(
                        698.0,
                        816.0,
                        image=entry_image_11
                    )
                    text11 = canvas.create_text(
                        696.0,
                        814.0,
                        anchor="center",
                        text=f"{lijstrecentenzoekopdrachten[0][1]}",
                        fill="#FFFFFF",
                        justify="center",
                        font=("Motiva Sans SemiBold", 24 * -1)
                    )
                else:
                    text1 = canvas.create_text(
                        84.0,
                        796.0,
                        anchor="nw",
                        text=f"{lijstrecentenzoekopdrachten[0][0]}",
                        fill="#FFFFFF",
                        font=("Motiva Sans SemiBold", 29 * -1)
                    )
                    entry_image_11 = PhotoImage(
                        file=relative_to_assets("frame2/entry_11.png"))
                    entry_bg_11 = canvas.create_image(
                        698.0,
                        816.0,
                        image=entry_image_11
                    )
                    text11 = canvas.create_text(
                        696.0,
                        814.0,
                        anchor="center",
                        text=f"{lijstrecentenzoekopdrachten[0][1]}",
                        fill="#FFFFFF",
                        justify="center",
                        font=("Motiva Sans SemiBold", 24 * -1)
                    )


            if len(mostplayedgamesself) >= 2:
                if lijstrecentenzoekopdrachten[1][1] == "--":
                    text21 = canvas.create_text(
                        84.0,
                        882.0,
                        anchor="nw",
                        text=f"{lijstrecentenzoekopdrachten[1][0]}",
                        fill="#AAAAAA",
                        font=("Motiva Sans SemiBold", 29 * -1)
                    )
                    entry_image_12 = PhotoImage(
                        file=relative_to_assets("frame2/entry_12.png"))
                    entry_bg_12 = canvas.create_image(
                        698.0,
                        902.0,
                        image=entry_image_12
                    )

                    text22 = canvas.create_text(
                        696.0,
                        900.0,
                        anchor="center",
                        text=f"{lijstrecentenzoekopdrachten[1][1]}",
                        fill="#FFFFFF",
                        justify="center",
                        font=("Motiva Sans SemiBold", 24 * -1)
                    )
                else:
                    text21 = canvas.create_text(
                        84.0,
                        882.0,
                        anchor="nw",
                        text=f"{lijstrecentenzoekopdrachten[1][0]}",
                        fill="#FFFFFF",
                        font=("Motiva Sans SemiBold", 29 * -1)
                    )
                    entry_image_12 = PhotoImage(
                        file=relative_to_assets("frame2/entry_12.png"))
                    entry_bg_12 = canvas.create_image(
                        698.0,
                        902.0,
                        image=entry_image_12
                    )
                    text22 = canvas.create_text(
                        696.0,
                        900.0,
                        anchor="center",
                        text=f"{lijstrecentenzoekopdrachten[1][1]}",
                        fill="#FFFFFF",
                        justify="center",
                        font=("Motiva Sans SemiBold", 24 * -1)
                    )

            if len(mostplayedgamesself) >= 3:
                if lijstrecentenzoekopdrachten[2][1] == "--":
                    text31 = canvas.create_text(
                        84.0,
                        968.0,
                        anchor="nw",
                        text=f"{lijstrecentenzoekopdrachten[2][0]}",
                        fill="#AAAAAA",
                        font=("Motiva Sans SemiBold", 29 * -1)
                    )
                    entry_image_13 = PhotoImage(
                        file=relative_to_assets("frame2/entry_13.png"))
                    entry_bg_13 = canvas.create_image(
                        698.0,
                        988.0,
                        image=entry_image_13
                    )

                    text32 = canvas.create_text(
                        696.0,
                        986.0,
                        anchor="center",
                        text=f"{lijstrecentenzoekopdrachten[2][1]}",
                        fill="#FFFFFF",
                        font=("Motiva Sans SemiBold", 24 * -1)
                    )
                else:
                    text31 = canvas.create_text(
                        84.0,
                        968.0,
                        anchor="nw",
                        text=f"{lijstrecentenzoekopdrachten[2][0]}",
                        fill="#FFFFFF",
                        font=("Motiva Sans SemiBold", 29 * -1)
                    )
                    entry_image_13 = PhotoImage(
                        file=relative_to_assets("frame2/entry_13.png"))
                    entry_bg_13 = canvas.create_image(
                        698.0,
                        988.0,
                        image=entry_image_13
                    )

                    text32 = canvas.create_text(
                        696.0,
                        986.0,
                        anchor="center",
                        text=f"{lijstrecentenzoekopdrachten[2][1]}",
                        fill="#FFFFFF",
                        font=("Motiva Sans SemiBold", 24 * -1)
                    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        1050.0,
        341.0,
        image=entry_image_5
    )

    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        1050.0,
        822.5,
        image=entry_image_6
    )

    entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        1570.0,
        582.0,
        image=entry_image_7
    )

    canvas.create_text(
        1500.0,
        20.0,
        anchor="nw",
        text=name,
        fill="#FFFFFF",
        font=("Motiva Sans Medium", 40 * -1)

    )
    def backbutton():
        window.destroy()
        dashboardwindow(name, avatarurl, status, steamid64)


    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: backbutton(),
        relief="flat"
    )
    button_1.place(
        x=-15.0,
        y=403.0,
        width=54.0,
        height=357.0
    )
    if status == 1:
        canvas.create_text(
            1500.0,
            70.0,
            anchor="nw",
            text="Online",
            fill="#FFFFFF",
            font=("Motiva Sans Regular", 24 * -1)
        )
    elif status == 0:
        canvas.create_text(
            1500.0,
            70.0,
            anchor="nw",
            text="Offline",
            fill="#CACACA",
            font=("Motiva Sans Regular", 24 * -1)
        )
    elif status == 3:
        canvas.create_text(
            1500.0,
            70.0,
            anchor="nw",
            text="Afwezig",
            fill="#CACACA",
            font=("Motiva Sans Regular", 24 * -1)
        )
    else:
        canvas.create_text(
            1497.0,
            70.0,
            anchor="nw",
            text="Kan status niet ophalen",
            fill="#CACACA",
            font=("Motiva Sans Regular", 24 * -1)
        )

    image_path = avatarurl
    image1 = add_urlimage_to_canvas(canvas, image_path, x=1388, y=17, width=89, height=89)

    image_path = "assets\logo_steam.png"
    image = add_image_to_canvas(canvas, image_path, x=52, y=20, width=267, height=77)

    image_item = canvas.create_image(52, 20, anchor=tk.NW, image=image)

    def mostplayeddef():
        # mostplayed games
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")
        global entry_image_8
        entry_image_8 = PhotoImage(
            file=f"analytics/mostplayed_{steamid64}_{date}.png")
        entry_bg_7 = canvas.create_image(
            1570.0,
            582.0,
            image=entry_image_8
        )

    def mostplayedpiedef():
        # mostplayed games
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")
        global entry_image_88
        entry_image_88 = PhotoImage(
            file=f"analytics/piechart_{steamid64}_{date}.png")
        entry_bg_7 = canvas.create_image(
            232.0,
            341.0,
            image=entry_image_88
        )


    def multiplayerpiedef():
        # mostplayed games
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")
        global entry_image_888
        entry_image_888 = PhotoImage(
            file=f"analytics/singleplayerormultiplayer_{steamid64}_{date}.png")
        entry_bg_7 = canvas.create_image(
            641.0,
            341.0,
            image=entry_image_888
        )

    def recommendedgamesdef():
        recommendedgames = getrecommendedgames(steamid64)
        global entry_image_9
        global entry_image_10

        entry_image_9 = PhotoImage(
            file=relative_to_assets("entry_9.png"))
        entry_bg_9 = canvas.create_image(
            1050.0,
            822.5,
            image=entry_image_9
        )

        entry_image_10 = PhotoImage(
            file=relative_to_assets("entry_10.png"))
        entry_bg_10 = canvas.create_image(
            869.5,
            700.5,
            image=entry_image_10
        )
        if len(recommendedgames[0]) > 28:
            formatted_game_name_not = recommendedgames[0]
            formatted_game_name0 = formatted_game_name_not[:26] + "..."
        else:
            formatted_game_name0 = recommendedgames[0]

        if len(recommendedgames[1]) > 28:
            formatted_game_name_not = recommendedgames[1]
            formatted_game_name1 = formatted_game_name_not[:26] + "..."
        else:
            formatted_game_name1 = recommendedgames[1]

        if len(recommendedgames[2]) > 28:
            formatted_game_name_not = recommendedgames[2]
            formatted_game_name2 = formatted_game_name_not[:26] + "..."
        else:
            formatted_game_name2 = recommendedgames[2]

        if len(recommendedgames[3]) > 28:
            formatted_game_name_not = recommendedgames[3]
            formatted_game_name3 = formatted_game_name_not[:26] + "..."
        else:
            formatted_game_name3 = recommendedgames[3]

        if len(recommendedgames[4]) > 28:
            formatted_game_name_not = recommendedgames[4]
            formatted_game_name4 = formatted_game_name_not[:26] + "..."
        else:
            formatted_game_name4 = recommendedgames[4]

        canvas.create_text(
            890.0,
            687.0,
            anchor="nw",
            text=formatted_game_name0,
            fill="#FFFFFF",
            font = ("Motiva Sans Regular", 25 * -1)

        )
        entry_image_11 = PhotoImage(
            file=relative_to_assets("entry_10.png"))
        entry_bg_11 = canvas.create_image(
            869.5,
            775.5,
            image=entry_image_10
        )
        canvas.create_text(
            890.0,
            762.0,
            anchor="nw",
            text=formatted_game_name1,
            fill="#FFFFFF",
            font=("Motiva Sans Regular", 25 * -1)

        )
        entry_image_12 = PhotoImage(
            file=relative_to_assets("entry_10.png"))
        entry_bg_12 = canvas.create_image(
            869.5,
            850.5,
            image=entry_image_10
        )
        canvas.create_text(
            890.0,
            837.0,
            anchor="nw",
            text=formatted_game_name2,
            fill="#FFFFFF",
            font=("Motiva Sans Regular", 25 * -1)

        )
        entry_image_13 = PhotoImage(
            file=relative_to_assets("entry_10.png"))
        entry_bg_13 = canvas.create_image(
            869.5,
            925.5,
            image=entry_image_10
        )
        canvas.create_text(
            890.0,
            912.0,
            anchor="nw",
            text=formatted_game_name3,
            fill="#FFFFFF",
            font=("Motiva Sans Regular", 25 * -1)

        )
        entry_image_14 = PhotoImage(
            file=relative_to_assets("entry_10.png"))
        entry_bg_14 = canvas.create_image(
            869.5,
            1000.5,
            image=entry_image_10
        )
        canvas.create_text(
            890.0,
            987.0,
            anchor="nw",
            text=formatted_game_name4,
            fill="#FFFFFF",
            font=("Motiva Sans Regular", 25 * -1)

        )

        canvas.create_text(
            880.0,
            612.0,
            anchor="nw",
            text="Top 5 recommended games.",
            fill="#FFFFFF",
            font=("Motiva Sans Bold", 25 * -1)

        )
        canvas.create_text(
            880.0,
            637.5,
            anchor="nw",
            text="In the last 2 weeks",
            fill="#AAAAAA",
            font=("Motiva Sans regular", 20 * -1)

        )

    def mostplayedgenres():
        global entry_image_20
        global entry_image_21
        global entry_image_10

        getgenres = meest_gespeelde_genres(steamid64)
        if len(getgenres) < 5:
            entry_image_20 = PhotoImage(
                file=relative_to_assets("entry_9.png"))
            entry_bg_9 = canvas.create_image(
                1050.0,
                341.0,
                image=entry_image_20
            )

            entry_image_21 = PhotoImage(
                file=relative_to_assets("entry_10.png"))
            entry_bg_10 = canvas.create_image(
                869.5,
                219,
                image=entry_image_21
            )
            canvas.create_text(
                880.0,
                135.5,
                anchor="nw",
                text="Top 5 played genres.",
                fill="#FFFFFF",
                font=("Motiva Sans Bold", 25 * -1)

            )
            canvas.create_text(
                890.0,
                193.5,
                anchor="nw",
                text=f"Er kon geen informatie worden \nopgehaald voor deze gebruiker",
                fill="#FAFAFA",
                font=("Motiva Sans Regular", 20 * -1)

            )

        else:

            entry_image_20 = PhotoImage(
                file=relative_to_assets("entry_9.png"))
            entry_bg_9 = canvas.create_image(
                1050.0,
                341.0,
                image=entry_image_20
            )

            entry_image_21 = PhotoImage(
                file=relative_to_assets("entry_10.png"))
            entry_bg_10 = canvas.create_image(
                869.5,
                219,
                image=entry_image_21
            )

            canvas.create_text(
                890.0,
                205.5,
                anchor="nw",
                text=f"{getgenres[0][0]} [{int(getgenres[0][1] / 60)} hours]",
                fill="#FFFFFF",
                font = ("Motiva Sans Regular", 25 * -1)

            )
            entry_image_22 = PhotoImage(
                file=relative_to_assets("entry_10.png"))
            entry_bg_11 = canvas.create_image(
                869.5,
                294,
                image=entry_image_10
            )
            canvas.create_text(
                890.0,
                280.5,
                anchor="nw",
                text=f"{getgenres[1][0]} [{int(getgenres[1][1] / 60)} hours]",
                fill="#FFFFFF",
                font=("Motiva Sans Regular", 25 * -1)

            )
            entry_image_23 = PhotoImage(
                file=relative_to_assets("entry_10.png"))
            entry_bg_12 = canvas.create_image(
                869.5,
                369.0,
                image=entry_image_10
            )
            canvas.create_text(
                890.0,
                355.5,
                anchor="nw",
                text=f"{getgenres[2][0]} [{int(getgenres[2][1] / 60)} hours]",
                fill="#FFFFFF",
                font=("Motiva Sans Regular", 25 * -1)

            )
            entry_image_24 = PhotoImage(
                file=relative_to_assets("entry_10.png"))
            entry_bg_13 = canvas.create_image(
                869.5,
                444,
                image=entry_image_10
            )
            canvas.create_text(
                890.0,
                430.5,
                anchor="nw",
                text=f"{getgenres[3][0]} [{int(getgenres[3][1] / 60)} hours]",
                fill="#FFFFFF",
                font=("Motiva Sans Regular", 25 * -1)

            )

            entry_image_25 = PhotoImage(
                file=relative_to_assets("entry_10.png"))
            entry_bg_14 = canvas.create_image(
                869.5,
                519.0,
                image=entry_image_10
            )
            canvas.create_text(
                890.0,
                505.5,
                anchor="nw",
                text=f"{getgenres[4][0]} [{int(getgenres[4][1] / 60)} hours]",
                fill="#FFFFFF",
                font=("Motiva Sans Regular", 25 * -1)

            )

            canvas.create_text(
                880.0,
                130.5,
                anchor="nw",
                text="Top 5 played genres.",
                fill="#FFFFFF",
                font=("Motiva Sans Bold", 25 * -1)

            )
            canvas.create_text(
                880.0,
                157.5,
                anchor="nw",
                text="Played genres in hours",
                fill="#AAAAAA",
                font=("Motiva Sans regular", 20 * -1)

            )

    window.after(800, recommendedgamesdef)
    window.after(850, mostplayedgamesself)
    window.after(825, mostplayedgenres)

    def analyticsmulticore1234():
        analyticsmulticore(steamid64)

    window.after(50, analyticsmulticore1234)
    window.after(1100, mostplayeddef)
    window.after(1200, mostplayedpiedef)
    window.after(1300, multiplayerpiedef)

    window.resizable(False, False)
    window.mainloop()


# analytics("testuser", "https://avatars.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg", 1, "76561199022018738")