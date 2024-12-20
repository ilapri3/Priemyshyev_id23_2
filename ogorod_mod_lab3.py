from tkinter import *
import time
import random
from tkinter import ttk

class Cabbage():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.occuped = 0


class Cabbages():
    def __init__(self, volume):
        self.n = 0 
        self.volume = volume
        self.cabbages = []

    def checker(self, x, y, value):
        for exist_cabbage in self.cabbages:
            if ((x - exist_cabbage.x) ** 2 + (y - exist_cabbage.y) ** 2) ** (1/2) < (value + exist_cabbage.value): 
                return True
    
    def generate(self, n):
        self.n = n 
        count = 0
        while count < n:
            limit = 5
            scalar = 1.5
            herd_size = 10
            value = random.randint(limit, herd_size * scalar)
            border = 30
            x = random.randint(border, self.volume - border)
            y = random.randint(border, self.volume - border)
            if self.checker(x, y, value):
                pass
            else:
                self.cabbages.append(Cabbage(x, y, value))
                count += 1
    
    def append(self, herd):
        while True:
            limit = 5
            scalar = 1.5
            herd_size = 10
            value = random.randint(limit, herd_size * scalar)
            border = 30
            x = random.randint(border, self.volume - border)
            y = random.randint(border, self.volume - border)
            if self.checker(x, y, value):
                pass
            else: 
                break
        self.cabbages.append(Cabbage(x, y, value))

    def add_click_cabbage(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.cabbages.append(Cabbage(x, y, value))


class Herd(): 
    def __init__(self, speed, endurance, eating, fertility):
        self.speed = speed 
        self.endurance = endurance
        self.eating = eating 
        self.fertility = fertility 

        self.x = random.randint(30, 770) 
        self.y = random.randint(30, 770)
        self.volume = 10 
        
        self.cord_x = 0
        self.cord_y = 0 

        self.eatingflag = 0 
        self.alive = 1
    
    def change(self, speed=None, endurance=None, eating=None, fertility=None):
        if speed is not None:
            self.speed = speed
        if endurance is not None:
            self.endurance = endurance
        if eating is not None:
            self.eating = eating
        if fertility is not None:
            self.fertility = fertility

    def move_herd(self, x, y):
        self.cord_x = x
        self.cord_y = y
        
        if self.volume >= 1:
            self.volume = self.volume - (1 / (self.speed + self.endurance))
        elif self.alive == 0 and len(herds) == 1:
            print('Стадо вымерло')
            raise SystemExit
        else:
            self.alive = 0


    def eat_cabbage(self, cabbages, exist_cabbage):
        if exist_cabbage.value > 0:

            exist_cabbage.value = exist_cabbage.value - self.eating
                
            if exist_cabbage.value <= 0:
                cabbages.cabbages.remove(exist_cabbage)
                cabbages.append(self)
            const = 1.35
            self.volume = self.volume + (exist_cabbage.value * self.fertility * const)


    def moving_nearest(self):
        if self.alive == 1: 
            if self.x != self.cord_x or self.y != self.cord_y:
                distance = ((self.cord_x - self.x) ** 2 + (self.cord_y - self.y) ** 2) ** (1/2) 
                if distance <= self.speed:
                    self.x = self.cord_x
                    self.y = self.cord_y 
                    self.eatingflag = 1

                else:
                    self.x = self.x + (self.cord_x - self.x) * (self.speed / distance)
                    self.y = self.y + (self.cord_y - self.y) * (self.speed / distance)
                    self.eatingflag = 0


def findNearestCabbage(herd, cabbages):
    nearest = 0
    min = size 
    for exist_cabbage in cabbages.cabbages: 
        if ((((herd.x - exist_cabbage.x) ** 2 + (herd.y - exist_cabbage.y) ** 2) ** (1/2)) < min) and (exist_cabbage.value > 0):
            min = ((herd.x - exist_cabbage.x) ** 2 + (herd.y - exist_cabbage.y) ** 2) ** (1/2)
            nearest = exist_cabbage
    return nearest 


def drawing(canvas, herds, cabbages):
    canvas.delete('all') 
    for exist_cabbage in cabbages.cabbages:
        for herd in herds:
            if herd.alive == 1:
                drawing_cord_x = exist_cabbage.x
                drawing_cord_y = exist_cabbage.y
                value = exist_cabbage.value 
                canvas.create_oval(drawing_cord_x - value, drawing_cord_y - value, drawing_cord_x + value, drawing_cord_y + value, fill='green')
    
    for herd in herds:
        if herd.alive == 1:
            if herd.eatingflag == 1:

                drawing_herd_x = herd.x
                drawing_herd_y = herd.y
                value = herd.volume
                canvas.create_arc(drawing_herd_x - value, drawing_herd_y - value, drawing_herd_x + value, drawing_herd_y + value, start = 90, extent = 180, fill = 'blue')
                
            else:

                drawing_herd_x = herd.x
                drawing_herd_y = herd.y
                value = herd.volume
                canvas.create_oval(drawing_herd_x - value, drawing_herd_y - value, drawing_herd_x + value, drawing_herd_y + value, fill = 'blue')

    base.update()

def on_click(event):
    x_mouse = event.x
    y_mouse = event.y

    enterme_new_window = Toplevel(base)
    enterme_new_window.title('Окно для ввода величины капусты')
    enterme_new_window.geometry('250x100+1+1')
    enterme_label = ttk.Label(enterme_new_window, text = 'Величина добавляемой капусты')
    enterme_label.place(x = 1, y = 25)
    enterme_val = ttk.Entry(enterme_new_window)
    enterme_val.place(x = 1, y = 1, width = 30)

    def cabbage_value():
        radius = enterme_val.get()
        value = int(radius)
        # print(x_mouse, y_mouse, value)
        cabbages.add_click_cabbage(x_mouse, y_mouse, value)
        enterme_new_window.destroy()

    confirm_button_for_add_cabbage = ttk.Button(enterme_new_window, text = 'Accept', command = cabbage_value)
    confirm_button_for_add_cabbage.place(x = 31, y = 1)

    window_for_herd = Toplevel(base)
    window_for_herd.geometry('300x125+1+160')
    window_for_herd.title('Окно для установки новых параметров для новго стада')
    window_for_herd_label_1 = ttk.Label(window_for_herd, text = ' - Характеристика скорости')
    window_for_herd_label_1.place(x = 42, y = 1)

    window_for_herd_label_2 = ttk.Label(window_for_herd, text = ' - Характеристика выносливости')
    window_for_herd_label_2.place(x = 42, y = 25)

    window_for_herd_label_3 = ttk.Label(window_for_herd, text = ' - Характеристика скорости поедания')
    window_for_herd_label_3.place(x = 42, y = 49)

    window_for_herd_label_4 = ttk.Label(window_for_herd, text = ' - Характеристика плодовитости')
    window_for_herd_label_4.place(x = 42, y = 73)

    def changes():
        global new_speed, new_endurance, new_eating, new_fertility
        new_speed = int(speed.get())
        new_endurance = int(endurance.get())
        new_eating = int(eating.get())
        new_fertility = float(fertility.get())
        

        # if herds:
        #     herds[-1].change(new_speed, new_endurance, new_eating, new_fertility)
    
    def create_new_herd():
        new_herd = Herd(speed = new_speed, endurance = new_endurance, eating = new_eating, fertility = new_fertility)
        herds.append(new_herd)
        window_for_herd.destroy()

    speed_spinbox = StringVar(value = 5)
    speed = Spinbox(window_for_herd, from_ = 1.0, to = 100.0, textvariable = speed_spinbox, state = "readonly", command = changes)
    speed.place(x = 1, y = 1, width = 40)

    endurance_spinbox = StringVar(value = 8)
    endurance = Spinbox(window_for_herd, from_ = 1.0, to = 100.0, textvariable = endurance_spinbox, state = "readonly", command = changes)
    endurance.place(x = 1, y = 25, width = 40)

    eating_spinbox = StringVar(value = 1)
    eating = Spinbox(window_for_herd, from_ = 1.0, to = 100.0, textvariable = eating_spinbox, state = "readonly", command = changes)
    eating.place(x = 1, y = 49, width = 40)

    fertility_spinbox = StringVar(value = 0.05)
    fertility = Spinbox(window_for_herd, from_ = 0.01, to = 1.0, increment = 0.01, textvariable = fertility_spinbox, state = "readonly", command = changes)
    fertility.place(x = 1, y = 73, width = 55)

    confirm_button_for_herd = ttk.Button(window_for_herd, text = 'Create herd', command = create_new_herd)
    confirm_button_for_herd.place(x = 1, y = 97)
#-----
def change_click(event):
        x_mouse = event.x
        y_mouse = event.y
        window_for_herd_change = Toplevel(base)
        window_for_herd_change.geometry('300x170+1+325')
        window_for_herd_change.title('Окно для установки новых параметров для новго стада')
        window_for_herd_change_label_1 = ttk.Label(window_for_herd_change, text = ' - Характеристика скорости')
        window_for_herd_change_label_1.place(x = 42, y = 1)

        window_for_herd_change_label_2 = ttk.Label(window_for_herd_change, text = ' - Характеристика выносливости')
        window_for_herd_change_label_2.place(x = 42, y = 25)

        window_for_herd_change_label_3 = ttk.Label(window_for_herd_change, text = ' - Характеристика скорости поедания')
        window_for_herd_change_label_3.place(x = 42, y = 49)

        window_for_herd_change_label_4 = ttk.Label(window_for_herd_change, text = ' - Характеристика плодовитости')
        window_for_herd_change_label_4.place(x = 42, y = 73)

        def changes_any():
            global change_new_speed, change_new_endurance, change_new_eating, change_new_fertility
            change_new_speed = int(speed_change.get())
            change_new_endurance = int(endurance_change.get())
            change_new_eating = int(eating_change.get())
            change_new_fertility = float(fertility_change.get())
            
            
            if herds:
                herds[val].change(change_new_speed, change_new_endurance, change_new_eating, change_new_fertility)
            

        speed_spinbox_cange = StringVar(value = 5)
        speed_change = Spinbox(window_for_herd_change, from_ = 1.0, to = 100.0, textvariable = speed_spinbox_cange, state = "readonly", command = changes_any)
        speed_change.place(x = 1, y = 1, width = 40)

        endurance_spinbox_change = StringVar(value = 8)
        endurance_change = Spinbox(window_for_herd_change, from_ = 1.0, to = 100.0, textvariable = endurance_spinbox_change, state = "readonly", command = changes_any)
        endurance_change.place(x = 1, y = 25, width = 40)

        eating_spinbox_change = StringVar(value = 1)
        eating_change = Spinbox(window_for_herd_change, from_ = 1.0, to = 100.0, textvariable = eating_spinbox_change, state = "readonly", command = changes_any)
        eating_change.place(x = 1, y = 49, width = 40)

        fertility_spinbox_change = StringVar(value = 0.05)
        fertility_change = Spinbox(window_for_herd_change, from_ = 0.01, to = 1.0, increment = 0.01, textvariable = fertility_spinbox_change, state = "readonly", command = changes_any)
        fertility_change.place(x = 1, y = 73, width = 55)

        list_herds = []

        for herd in range(len(herds)):
            list_herds.append(herd)

        def selector(a):
            global val
            a = 1
            val = int(choose_box.get())
            return a

        choose_box = ttk.Combobox(window_for_herd_change, values = list_herds)
        choose_box.place(x = 1, y = 97)
        choose_box.bind("<<ComboboxSelected>>", selector)

stop = 0
def pause():
    global stop
    stop +=1


# -------------
size = 800
base = Tk()
base.config(bg = 'brown')
canvas = Canvas(base, width = size, height = size)
canvas.pack()
canvas.bind('<Button-1>', on_click)
canvas.bind('<Button-2>', change_click)
stop_button = ttk.Button(base, text = 'Пауза', command = pause)
stop_button.place(x = 710, y = 1)


cabbages = Cabbages(size)
herds = []
herd = Herd(speed = 5, endurance = 8, eating = 1, fertility = 0.05) 
herds.append(herd)
cabbages.generate(10)

def inf_cycle():
    if stop % 2 == 0:
        if len(herds) != 0:
            for herd in herds:
                if herd.alive == 1:
                    nearest_Cabbage = findNearestCabbage(herd, cabbages)
                    cabbage_cord_x, cabbage_cord_y = nearest_Cabbage.x, nearest_Cabbage.y
                    herd.move_herd(cabbage_cord_x, cabbage_cord_y)
                    herd.moving_nearest()

                    herd_cord_x, herd_cord_y = herd.x, herd.y
                    if herd_cord_x == cabbage_cord_x and herd_cord_y == cabbage_cord_y:
                        herd.eat_cabbage(cabbages, nearest_Cabbage)
                else:
                    herds.remove(herd)
            
            drawing(canvas, herds, cabbages)
        else:
            print('Стада вымерли')
            raise SystemExit
            
    base.after(30, inf_cycle)

inf_cycle()
base.mainloop()
