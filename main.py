import tkinter as tk
from PIL import ImageTk
import datetime
import myclasses as cl
from functools import partial

my_messages = cl.get_messages('remik')

# Main program

root = tk.Tk()
root.title("Advent Calendar")

# Create canvas
canvas_width, canvas_height = root.winfo_screenwidth(), root.winfo_screenheight()
canvas = tk.Canvas(root,
                   bg="white",
                   width=canvas_width,
                   height=canvas_height)
canvas.pack(fill="both", expand=True)

# Load background image and make it transparent
# orig_img = Image.open("./images/background.jpg").convert("RGBA")
orig_img = cl.get_background()
img = orig_img.resize((canvas_width, canvas_height))

# Convert to Tkinter Photoimage and draw
tk_img = ImageTk.PhotoImage(img)
canvas.create_image(0, 0, image=tk_img, anchor="nw")
canvas.image = tk_img  # Must store reference on the canvas

# Draw a rectangle
today = int(str(datetime.datetime.today()).split()[0].split('-')[-1])
for day in range(1,31):
    if day <= today:
        btn_color = "light green"
        out_color = "dark green"
    else:
        btn_color = "red"
        out_color = "red"
    rec = cl.Door(canvas_width, canvas_height, day=day)
    x, y, w, h = rec.get_x(), rec.get_y(), rec.get_width(), rec.get_height()
    cl.round_rectangle(canvas, x, y, x+w, y+h,
                            fill=rec.get_fill(), outline=out_color, width=7)
    btn = tk.Button(root,
                    text=f"{day}",
                    command=partial(cl.on_button_click, root=root, canvas=canvas, day=day, msg=my_messages[day], w=canvas_width, h=canvas_height),
                    bg="white",
                    fg="black",
                    activebackground=btn_color,
                    activeforeground="black",
                    bd=0,
                    relief="raised",
                    font=("Ariel",24))
    canvas.create_window(x+w/2,y+h/2,width=w-7,height=h-7,window=btn)

root.mainloop()

