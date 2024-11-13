from tkinter import *
import random
import time

class Cabbage:
    def __init__(self, x, y, value):
        #создаем отдельные капусты по координатам x и y на огороде
        self.x = x
        self.y = y
        self.value = value #задаем объем капусты


class Cabbages:
    def __init__(self, size):
        self.n = 0 # количество добавляемых капуст на огород
        self.size = size
        self.cabbages = [] #храним все капусты в огороде

    def check_overlap(self, x, y, value): #делаем проверку на то, чтобы наши капусты не наростали друг на друга
        for cabbage in self.cabbages: # проходимся по уже созданным капустам
            distance = ((x - cabbage.x) ** 2 + (y - cabbage.y) ** 2) ** 0.5 # высчитываем расстояние между новой капустой и текущей капустой, вычисление по Пифагору
            if distance < (value + cabbage.value): # сравниваем расстояние между центрами
                return True # пересекается
        return False
    
    # данная функция служит для первоначальной генерации капусты на огороде, до поедания одной из капуст
    def generateCabbage(self, n, goat):
        self.n = n # храним общее количество кустов, которое будет задано для создания
        count = 0 # счетчик для отслеживания количества созданной капусты
        while count < n:
            # задаем координаты для капусты, чтобы она генерировалась от края поля на 50 единиц, чтобы капуста была полноостью видима на огороде
            x = random.randint(50, self.size - 50)
            y = random.randint(50, self.size - 50)
            value = random.randint(5, goat.size * 2)  # задаем размер капусты от 5 до двойного размера стада, чтобы капуста не была слишком огромной
            if not self.check_overlap(x, y, value): # проверка на то, чтобы капусты не пересекались между собой
                self.cabbages.append(Cabbage(x, y, value))
                count += 1
    
    # данная функция служит для дальнейшего доваления капусты, после того, как стадо съело одну капусту
    def appendCabbage(self, goat):
        while True: # цикл до тех пор, пока на огороде не появится новая капуста
            # задание случайного места для капусты
            x = random.randint(50, self.size - 50)
            y = random.randint(50, self.size - 50)
            value = random.randint(5, goat.firstSize * 2)
            if not self.check_overlap(x, y, value): 
                break
        self.cabbages.append(Cabbage(x, y, value)) # если все удовлетворяет, то создаем объект и доваляем в массив, в котором есть все капусты


class Goat: # описываем поведение стада
    def __init__(self, speed, endurance, eating, fertility):
        self.speed = speed # задаем параметр скорости передживения стада
        self.endurance = endurance # задаем параметр живучести стада
        self.eating = eating # задаем параметр скорости поедания капусты стадом
        self.fertility = fertility # задаем параметр плодовитости стада
        self.x = 0 # начальные координаты стада
        self.y = 0
        self.firstSize = 10 #задаем начальный размер для стада, от которого мы делаем расчеты
        self.size = 10 # размер стада, который изменяется с поеданием капусты
        self.moveX = 0
        self.moveY = 0 # целевые координаты, к которым будет двигаться стадо, для поедания капусты
        self.eatingRightNow = False # состояние поедания капусты в данный момент времени

    def move(self, x, y): # передвижение стада к капустам
        self.moveX = x
        self.moveY = y
        if self.size >= 1: # сокращение численности стада, когда стадо не питается
            self.size -= 1 / self.endurance # чем выше выносливость, тем меньше сокращение стада и наоборот
        else:
            print('Стадо вымерло')
            raise SystemExit  # завершение выполнения программы


    def eat(self, cabbages, cabbage): # процесс поедания капусты стадом
        if cabbage.value > 0: # проврерка, съедена капуста или нет
            cabbage.value -= self.eating # уменьшение размера капусты, в процессе поедания со скоростью поедания стада
            if cabbage.value <= 0: # условие, если капуста была съедена
                cabbages.cabbages.remove(cabbage) # удаляем данную капусту из списка всех капуст 
                cabbages.appendCabbage(self) # и сразу же добавляем новую капусту в огород
            self.size += cabbage.value * self.fertility #увеличение размера стада после поедания капусты, в зависимости от количества съеденного и плодовитости

    def updatePosition(self): #  отвечает за движение козы к заданной точке. Если расстояние до точки меньше, чем скорость, то коза останавливается и начинает есть кустик.
        if self.x != self.moveX or self.y != self.moveY: # проверка, достигло ли стадо капусты
            # вычисляем разницу значений координат, чтобы определить направление и расстояние для движения по вектору 
            dx = self.moveX - self.x 
            dy = self.moveY - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5 #вычисление вектора по Пифагору
            if distance <= self.speed: # проверка, достаточно ли близко коза к капусте, чтобы ее есть
                self.x = self.moveX
                self.y = self.moveY # обновляем координаты козы, на текущие координаты
                self.eatingRightNow = True
            else:
                # если расстояние до цели большое, коза будет двигаться быстрее, если расстояние маленькое — медленнее.
                self.x += dx * self.speed / distance
                self.y += dy * self.speed / distance
                self.eatingRightNow = False

def findNearestCabbage(goat, cabbages): # определение ближайшей капусты, которую стадо должно съесть
    nearest = None # переменная для хранения ближайшей капусты
    min = 600 # минимальное расстояние между стадом и капустой
    for cabbage in cabbages.cabbages: # перебираем каждый кочан капусты
        distance = ((goat.x - cabbage.x) ** 2 + (goat.y - cabbage.y) ** 2) ** 0.5 # вычисляем расстояние от капусты до стада по Пифагору
        if distance < min and cabbage.value > 0: # если расстояние до куста меньше, чем минимальное расстояние и если капуста существует
            min = distance
            nearest = cabbage # обновляем минимальное расстояние и ближайщую капусту 
    return nearest # возвращаем ближайщую капусту, которая находится на минимальном расстоянии

def update(canvas, goat, cabbages):
    canvas.delete("all") #каждый раз удаляем весь холст и рисуем заново, чтобы не было наложения элементов при рисовании
    for cabbage in cabbages.cabbages: # определение места для капусты и рисование их зеленым цветом
        canvas.create_oval(cabbage.x - cabbage.value, cabbage.y - cabbage.value,
                           cabbage.x + cabbage.value, cabbage.y + cabbage.value, fill='green')
        
    if goat.eatingRightNow: # при поедании капусты стадом рисуем два полукруга, один из которых серый, а другой - зеленый.
        canvas.create_arc(goat.x - goat.size, goat.y - goat.size,
                           goat.x + goat.size, goat.y + goat.size, start=90, extent=180, fill='blue')
    else:
        canvas.create_oval(goat.x - goat.size, goat.y - goat.size,
                       goat.x + goat.size, goat.y + goat.size, fill='blue') # если же не происходит процесса поедания, то стадо заполняется полностью серым цветом
    
    root.update()

# создаем основое окно огорода
size = 600
root = Tk()
canvas = Canvas(root, width = size, height = size) # холст для рисования размером 600 на 600
canvas.pack()

goat = Goat(speed = 8, endurance = 8, eating = 1, fertility = 0.05) # задание основных параметров для стада 
cabbages = Cabbages(size) 
cabbages.generateCabbage(17, goat)

while True: # создаем бесконечный цикл, в котором стадо ищет ближайщую капусту и направляется к ней, чтобы съесть
    nearestCabbage = findNearestCabbage(goat, cabbages)
    goat.move(nearestCabbage.x, nearestCabbage.y)
    goat.updatePosition()

    if goat.x == nearestCabbage.x and goat.y == nearestCabbage.y: # если стадо достигает капусты, то начинается процесс поедания
        goat.eat(cabbages, nearestCabbage)

    update(canvas, goat, cabbages) # обновление холста

    time.sleep(0.07) #устанвливаем задержку между итерациями цикла, чтобы избежать быстрого исполнения программы.