import tkinter as tk
from tkinter import filedialog, Text
import os

configured = False

if os.path.isfile('config.py'):
    configured = True

if configured == False:
    root = tk.Tk()
    items = []
    root.title('Configuring')

    canvas = tk.Canvas(root, height=700, width=800, bg="#008080")
    canvas.pack()

    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def addToFile():
        item = e.get()
        item = str(item)
        items.append(item)
        for widget in frame.winfo_children():
            widget.destroy()
        for i in range(0, len(items)):
            label = tk.Label(frame, text=items[i], bg="#C0C0C0")
            label.pack()
        if len(items) > 2:
            root.destroy()

    label = tk.Label(
        text="Enter 3 Email Addresses that you would like to send emails to using this voice assistant:")
    label.pack()

    e = tk.Entry(root, width=50)
    e.pack()

    add = tk.Button(root, text="Click", padx=10, pady=5, fg="white",
                    bg="#C0C0C0", font=('helvetica', 9), command=addToFile)
    add.pack()

    root.mainloop()

with open('config.py', 'w') as f:
    f.write("main_email_address = ")
    f.write('"')
    f.write(items[0])
    f.write('"')
    f.write("\n")
    f.write("email_address2 = ")
    f.write('"')
    f.write(items[1])
    f.write('"')
    f.write("\n")
    f.write("email_address3 = ")
    f.write('"')
    f.write(items[2])
    f.write('"')
