import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

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

# Example usage
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=200)
canvas.pack()

image_path = "https://avatars.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg"
image = add_urlimage_to_canvas(canvas, image_path, x=55, y=40, width=89, height=89)

root.mainloop()
