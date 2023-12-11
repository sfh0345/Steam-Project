def analytics(name, avatarurl, status, steamid64):
    import time
    from pathlib import Path
    from analyticsophalen import analyticsmulticore
    import tkinter as tk
    from PIL import Image, ImageTk
    from io import BytesIO
    import requests
    import datetime

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
    window.title("Steam | Analytics")



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

    def analyticsmulticore1234():
        analyticsmulticore(steamid64)

    window.after(1500, mostplayeddef)
    window.after(1000, analyticsmulticore1234)


    window.resizable(False, False)
    window.mainloop()


analytics("testuser", "https://avatars.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg", 1, "76561199022018738"  )


