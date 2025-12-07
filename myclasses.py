import tkinter as tk
import datetime
import re
from PIL import Image
import requests
from io import BytesIO

class Door:

    def __init__(self, canvas_width, canvas_height, day):
        ncol = 6
        self.day = day
        self.width = canvas_width / 12
        self.height = canvas_height / 10
        self.wspace = self.width * 3 / 7
        self.hspace = self.width * 1 / 6
        row = (day-1) // ncol
        col = (day-1) % ncol
        self.x = 2 * self.width + col * (self.width + self.wspace)
        self.y = 2 * self.height + row * (self.height + self.hspace)
        self.fill = "white"

    def content(self):
        return

    # getters
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_fill(self):
        return self.fill

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

def on_button_click(root, canvas, day, msg, w, h):

    def destroy_button():
        newbtn.destroy()
        button_border.destroy()
        frame.destroy()

    today = int(str(datetime.datetime.today()).split()[0].split('-')[-1])
    if day <= today:

        button_border = tk.Frame(root, highlightbackground="dark green",
                                 highlightthickness=20, bd=0)
        canvas.create_window(w/2,h/2,width=w/2+20,height=h/2+20,window=button_border)

       # --- create a frame that will hold text + scrollbar ---
        frame = tk.Frame(root, bg="white")
        # Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        # Scrollable text widget
        newtxt = tk.Text(
            frame,
            bg="white",
            fg="black",
            font=("Arial", 20),
            wrap="word",
        )
        newtxt.pack(side="left", fill="both", expand=True)
        # Connect scrollbar to text
        newtxt.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=newtxt.yview)
        # Insert the message
        newtxt.insert("1.0", "-"*int(w/50) + f"    DAY {day}    " + "-"*int(w/50) + "\n\n", "centered")
        newtxt.tag_configure("centered", justify="center")
        newtxt.insert("end", msg)
        # Make it behave like a label (non-editable)
        newtxt.config(state="disabled")
        # Put this whole frame onto the canvas
        canvas.create_window(
            w / 2,
            h / 2,
            width=w / 2,
            height=h / 2,
            window=frame
        )

        newbtn = tk.Button(
            root,
            text="x",  # or "×"
            font=("Arial", 30, "bold"),
            bg="white",
            fg="black",
            bd=0,
            command=destroy_button,
            highlightthickness=0
        )
        canvas.create_window(w*3/4-30,h*1/4+20,width=30,height=30,window=newbtn)

def get_messages(name):
    file_id = {
              'remik': '1qz_Qu0zH-mOAvnCV4Or83gPmCnJZbTl4K6bCO1L7wX0'}[name]
    export_url = f"https://docs.google.com/document/d/{file_id}/export?format=txt"
    data = requests.get(export_url).text
    pattern = r"===\s*(DAY \d+)\s*===\s*([\s\S]*?)(?====\s*DAY|\Z)"
    my_messages = {k: '' for k in range(1, 31)}
    for day, m in re.findall(pattern, data):
        my_messages[int(day.split()[1])] = m.rstrip().replace('\r', '')

    return my_messages

def get_background():
    file_id = '15zlYDEWMq2vP8CKIb-Z51DdZyjHfFxiV'
    export_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(export_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    return img


