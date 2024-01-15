def analytics(name, avatarurl, status, steamid64):
    from pathlib import Path
    from analyticsophalen import analyticsmulticore
    import tkinter as tk
    from PIL import Image, ImageTk
    from io import BytesIO
    from getnewgame import getrecommendedgames
    import requests
    import datetime
    from dashboard import dashboardwindow

    from sys import platform

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

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        232.0,
        822.5,
        image=entry_image_2
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        641.0,
        341.0,
        image=entry_image_3
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        641.0,
        822.5,
        image=entry_image_4
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
            622.0,
            anchor="nw",
            text="Top 5 recommended games.",
            fill="#FFFFFF",
            font=("Motiva Sans Bold", 25 * -1)

        )


    def analyticsmulticore1234():
        analyticsmulticore(steamid64)

    window.after(1200, mostplayeddef)
    window.after(1000, recommendedgamesdef)

    window.after(50, analyticsmulticore1234)

    window.resizable(False, False)
    window.mainloop()


# analytics("testuser", "https://avatars.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg", 1, "76561199022018738"  )


