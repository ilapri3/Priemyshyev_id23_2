from tkinter import *
from tkinter import colorchooser
import math

size = 600
radius = 200
drawing_window = Tk()
canvas = Canvas(drawing_window, width=size, height=size)
canvas.pack()

main_circle = canvas.create_oval(300 - radius, 300 - radius, 300 + radius, 300 + radius, fill = 'red', outline = 'white')
mini_circle = canvas.create_oval(295, 95, 305, 105, fill = 'black')
direction = 0
speed = 10

def moveBall():
    global direction
    x_direction = 300 + math.cos(math.radians(direction)) * radius
    y_direction = 300 + math.sin(math.radians(direction)) * radius
    canvas.coords(mini_circle, x_direction - 5, y_direction - 5, x_direction + 5, y_direction + 5)
    direction += 1
    drawing_window.after(speed, moveBall)

moveBall()
drawing_window.mainloop()
