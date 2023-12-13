import tkinter as tk

def fun():
    global count, text, lbl, root
    lbl.config(text=text + '.' * count)

    count += 1
    if count == 4:
        count = 0

    root.after(300, fun)

root = tk.Tk()

count = 0
text = 'Running'

lbl = tk.Label(root, text=text, font="Arial, 12")
lbl.place(x=102, y=70)

fun()

root.mainloop()