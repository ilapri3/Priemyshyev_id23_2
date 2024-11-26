from tkinter import *
import time
import random

class Cabbage():
    def __init__(self, x, y, value):
        #создаем отдельные капусты по координатам x и y на огороде
        self.x = x
        self.y = y
        self.value = value # задаем величину капусты


class Cabbages():
    def __init__(self, volume):
        self.n = 0 
        self.volume = volume
        self.cabbages = []

    def checker(self, x, y, value): #делаем проверку на то, чтобы наши капусты не наростали друг на друга
        for exist_cabbage in self.cabbages: # проходимся по уже созданным капустам
            if ((x - exist_cabbage.x) ** 2 + (y - exist_cabbage.y) ** 2) ** (1/2) < (value + exist_cabbage.value): # сравниваем расстояние между центрами
                return True # пересекается
    
    # данная функция служит для первоначальной генерации капусты на огороде, до поедания одной из капуст
    def generate(self, n, herd):
        self.n = n # храним общее количество кустов, которое будет задано для создания
        count = 0 # счетчик для отслеживания количества созданной капусты
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
            else: # проверка на то, чтобы капусты не пересекались между собой
                self.cabbages.append(Cabbage(x, y, value))
                count += 1
    
    # данная функция служит для дальнейшего добавления капусты, после того, как стадо съело одну капусту
    def append(self, herd):
        while True: # цикл до тех пор, пока на огороде не появится новая капуста
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
        self.cabbages.append(Cabbage(x, y, value)) # если все удовлетворяет, то создаем объект и доваляем в массив, в котором есть все капусты


class Herd(): # описываем поведение стада
    def __init__(self, speed, endurance, eating, fertility):
        self.speed = speed # задаем параметр скорости передживения стада
        self.endurance = endurance # задаем параметр живучести стада
        self.eating = eating # задаем параметр скорости поедания капусты стадом
        self.fertility = fertility # задаем параметр плодовитости стада

        self.x = random.randint(30, 770) # начальные координаты стада
        self.y = random.randint(30, 770)
        self.volume = 10 # размер стада, который изменяется с поеданием капусты
        
        self.cord_x = 0
        self.cord_y = 0 # целевые координаты, к которым будет двигаться стадо, для поедания капусты
        self.alive = 1
        self.eatingflag = 0 # состояние поедания капусты в данный момент времени

    def move_herd(self, x, y): # передвижение стада к капустам
        self.cord_x = x
        self.cord_y = y
        if self.volume >= 1: # сокращение численности стада, когда стадо не питается
            self.volume = self.volume - (1 / self.endurance) - (1/self.speed**self.speed) # чем выше выносливость, тем меньше сокращение стада и наоборот
        elif self.alive == 0 and len(herds) == 1:
            raise SystemExit
        else:
            self.alive = 0  # завершение выполнения программы


    def eat_cabbage(self, cabbages, exist_cabbage): # процесс поедания капусты стадом
        if exist_cabbage.value > 0: # проврерка, съедена капуста или нет
            exist_cabbage.value = exist_cabbage.value - self.eating # уменьшение размера капусты, в процессе поедания со скоростью поедания стада
            
            if exist_cabbage.value <= 0: # условие, если капуста была съедена
                cabbages.cabbages.remove(exist_cabbage) # удаляем данную капусту из списка всех капуст 
                cabbages.append(self) # и сразу же добавляем новую капусту в огород
            const = 1.35
            self.volume = self.volume + (exist_cabbage.value * self.fertility * const) #увеличение размера стада после поедания капусты, в зависимости от количества съеденного и плодовитости

    def find_nearest(self): #  отвечает за движение козы к заданной точке. Если расстояние до точки меньше, чем скорость, то коза останавливается и начинает есть кустик.
        if self.x != self.cord_x or self.y != self.cord_y: # проверка, достигло ли стадо капусты
            # вычисляем разницу значений координат, чтобы определить направление и расстояние для движения по вектору 
            distance = ((self.cord_x - self.x) ** 2 + (self.cord_y - self.y) ** 2) ** (1/2) #вычисление вектора по Пифагору
            if distance <= self.speed: # проверка, достаточно ли близко коза к капусте, чтобы ее есть
                self.x = self.cord_x
                self.y = self.cord_y # обновляем координаты козы, на текущие координаты
                self.eatingflag = 1
            else:
                # если расстояние до цели большое, коза будет двигаться быстрее, если расстояние маленькое — медленнее.
                self.x = self.x + (self.cord_x - self.x) * (self.speed / distance)
                self.y = self.y + (self.cord_y - self.y) * (self.speed / distance)
                self.eatingflag = 0

def findNearestCabbage(herd, cabbages): # определение ближайшей капусты, которую стадо должно съесть
    min = size # минимальное расстояние между стадом и капустой
    for exist_cabbage in cabbages.cabbages: # перебираем каждый кочан капусты
        if ((((herd.x - exist_cabbage.x) ** 2 + (herd.y - exist_cabbage.y) ** 2) ** (1/2)) < min) and (exist_cabbage.value > 0): # если расстояние до куста меньше, чем минимальное расстояние и если капуста существует
            min = ((herd.x - exist_cabbage.x) ** 2 + (herd.y - exist_cabbage.y) ** 2) ** (1/2)
            nearest = exist_cabbage # обновляем минимальное расстояние и ближайщую капусту
    return nearest # возвращаем ближайщую капусту, которая находится на минимальном расстоянии

def drawing(canvas, herd, cabbages):
    canvas.delete('all') #каждый раз удаляем весь холст и рисуем заново, чтобы не было наложения элементов при рисовании
    for exist_cabbage in cabbages.cabbages:

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

# создаем основое окно огорода
size = 800
base = Tk()
canvas = Canvas(base, width = size, height = size)
canvas.pack()

cabbages = Cabbages(size)
herds = []
herd = Herd(speed = 8, endurance = 8, eating = 1, fertility = 0.05) # задание основных параметров для стада 
herds.append(herd)
cabbages.generate(17, herd)



for _ in iter(int, 1):
    for herd in herds:
        if herd == 0:
            herds.remove(herd)
            continue
        nearest_Cabbage = findNearestCabbage(herd, cabbages)
        cabbage_cord_x, cabbage_cord_y = nearest_Cabbage.x, nearest_Cabbage.y
        herd.move_herd(cabbage_cord_x, cabbage_cord_y)
        herd.find_nearest()
    
        herd_cord_x, herd_cord_y = herd.x, herd.y
        if herd_cord_x == cabbage_cord_x and herd_cord_y == cabbage_cord_y: # если стадо достигает капусты, то начинается процесс поедания
            herd.eat_cabbage(cabbages, nearest_Cabbage)
    
        drawing(canvas, herd, cabbages)
    
        time.sleep(0.04) #устанвливаем задержку между итерациями цикла, чтобы избежать быстрого исполнения программы.

base.mainloop()
