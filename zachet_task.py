from tkinter import *
import random
from tkinter import ttk

class Elevator:
    def __init__(self):
        self.floors = 5
        self.power = 1000
        self.weight = 500
        self.elevator_position = 0
        self.speed = 0
        self.is_moving = 0

    def floors(self, value):
        self.floors = int(value)

    def power(self, value):
        self.power = int(float(value))

    def start(self):
        if self.is_moving == 0:
            weight = int(weight_spinbox.get())
            if weight > 0:
                self.speed = self.power / weight
                if self.elevator_position < (self.floors - 1):
                    self.move_elevator(1)  
                else:
                    self.move_elevator(-1)  

    def move_elevator(self, direction):
        if direction == 1 and self.elevator_position < (self.floors - 1):
            new_position = (self.elevator_position + 1) * (400 / self.floors)
            for _ in range(int(400 / (self.speed / 10))): 
                canvas.move(elevator, 0, -1 * self.speed / 10)
                base.update()
                base.after(10)  
            
            self.elevator_position += 1
            
            if self.elevator_position < (self.floors - 1):
                base.after(1000)  
            
            if self.is_moving == 0:
                self.move_elevator(direction)

    def update_elevator(self):
        canvas.coords(elevator, 50, 350, 150, 400)
        self.elevator_position = 0


base = Tk()

canvas = Canvas(base, width=200, height=400,)
canvas.grid(columnspan=2, row=4)

elevator = canvas.create_rectangle(50, 350, 150, 400, fill='white')

simulator = Elevator()

Label(base, text="Количество этажей:").grid(column=0, row=0)
floor_spinbox = ttk.Spinbox(base, from_=1, to=15, command=lambda: simulator.floors(floor_spinbox.get()))
floor_spinbox.grid(column=1, row=0)
floor_spinbox.set(simulator.floors)

Label(base, text="Мощность мотора:").grid(column=0, row=1)
power_spinbox = ttk.Spinbox(base, from_=100, to=5000, increment = 50, command=lambda value: simulator.power(power_spinbox.get()))
power_spinbox.grid(column=1, row=1)
power_spinbox.set(simulator.power)

Label(base, text="Вес груза:").grid(column=0, row=2)
weight_spinbox = ttk.Spinbox(base, from_=100, to=2000, increment = 50)
weight_spinbox.grid(column=1, row=2)
weight_spinbox.set(simulator.weight)

start_button = ttk.Button(base, text="Старт", command=simulator.start)
start_button.grid(column=0, row=3)

update_button = ttk.Button(base, text="Сброс", command=simulator.update_elevator)
update_button.grid(column=1, row=3)

base.mainloop()
