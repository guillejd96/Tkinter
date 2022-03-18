from tkinter import *
from tkinter import ttk
from enum import Enum
import random
import math
from matplotlib.patches import Circle
from datetime import datetime

class Simulation_State(Enum):
    INIC='INIC',
    STOP='STOP',
    PLAY='PLAY'
    
class Ant_State(Enum):
    STOP=0,
    SEARCH=1,
    EAT=2

def getRandomCoordinate():
    return (int(random.random()*650)%650),(int(random.random()*650)%650)

def getRandomDirection():
    return int(random.random()*10),int(random.random()*10)

def getRandomCoordinateIn(x,y):
    circ = Circle((x+25, y+25), radius = 10)
    fx = 1
    if random.random() < 0.5:
        fx=-1
    fy = 1
    if random.random() < 0.5:
        fy=-1
    sx = random.random() * 5
    sy = random.random() * 5
    rx = x + 25 + int(sx * fx)
    ry = y + 25 + int(sy * fy)
    while circ.contains_point([rx,ry])==False:
        fx = 1
        if random.random() < 0.5:
            fx=-1
        fy = 1
        if random.random() < 0.5:
            fy=-1
        sx = random.random() * 5
        sy = random.random() * 5
        rx = x + int(sx * fx)
        ry = y + int(sy * fy)
    return rx, ry

def distBetween(x1,y1,x2,y2):
    return int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))

class Nest():
    
    def __init__(self,parent,x,y):
        self.parent=parent
        self.x=x
        self.y=y
        
        self.nest = self.parent.create_oval(x,y,x+50,y+50,fill='brown')
        
class Food():
    
    def __init__(self,parent):
        
        self.parent = parent
        self.x,self.y = getRandomCoordinate()
        
        self.food = self.parent.create_polygon(
                         (self.x-3),(self.y-3),
                         (self.x+3),(self.y-3),
                         (self.x+3),(self.y+3),
                         (self.x-3),(self.y+3),
                         fill = "green")
        
class Ant():
    
    def __init__(self,p,nx,ny,n):
        self.parent = p
        
        self.nestx = nx
        self.nesty = ny
        
        self.selected = False
        
        self.comida = 0
        
        self.name = n
        
        self.speed = 1 + random.random()
        
        self.distance = 10
        
        self.x , self.y = getRandomCoordinateIn(nx,ny)
        
        self.ant = self.parent.create_polygon(
                         (self.x-2+random.random()),(self.y-2+random.random()),
                         (self.x+2+random.random()),(self.y-2+random.random()),
                         (self.x+2+random.random()),(self.y+2+random.random()),
                         (self.x-2+random.random()),(self.y+2+random.random()),
                         tag=self.name)
        
        if self.name == "":
            self.name = str(self.ant - 2)
        
        self.dirx = -1
        self.diry = -1
        
        self.state = Ant_State.STOP
        
        self.modified = False
        
    def setState(self,s):
        self.state = s
            
    def gotoDirection(self):
        if self.state == Ant_State.SEARCH:
            if self.dirx==-1 and self.diry==-1:
                self.selectDirection()
            b = self.goto(self.dirx,self.diry)
            if b:
                self.removeDirection()
            return b
        else:
            return False
        
    def selectDirection(self):
        self.dirx , self.diry = getRandomCoordinate()
        
    def removeDirection(self):
        self.dirx = -1
        self.diry = -1
    
    def select(self):
        self.selected = True
        self.parent.itemconfig(self.ant,fill="gray")
        
    def deselect(self):
        self.selected = False
        self.parent.itemconfig(self.ant,fill="black")
    
    def moveup(self):
        self.parent.move(self.ant,0,self.speed)
        self.parent.update()
        self.y+=self.speed
        
    def movedown(self):
        self.parent.move(self.ant,0,self.speed*(-1))
        self.parent.update()
        self.y-=self.speed
        
    def moveleft(self):
        self.parent.move(self.ant,self.speed,0)
        self.parent.update()
        self.x += self.speed
        
    def moveright(self):
        self.parent.move(self.ant,self.speed*(-1),0)
        self.parent.update()
        self.x -= self.speed
        
    def moveupleft(self):
        self.parent.move(self.ant,self.speed,self.speed)
        self.parent.update()
        self.y+=self.speed
        self.x+=self.speed
        
    def moveupright(self):
        self.parent.move(self.ant,self.speed*(-1),self.speed)
        self.parent.update()
        self.y+=self.speed
        self.x-=self.speed
        
    def movedownleft(self):
        self.parent.move(self.ant,self.speed,self.speed*(-1))
        self.parent.update()
        self.y-=self.speed
        self.x+=self.speed
        
    def movedownright(self):
        self.parent.move(self.ant,self.speed*(-1),self.speed*(-1))
        self.parent.update()
        self.y-=self.speed
        self.x-=self.speed
    
    def getFastestWay(self,x,y):
        r = 0
        d = 1000
        if distBetween(self.x+self.speed,self.y,x,y)<d:
            r = 1
            d = distBetween(self.x+self.speed,self.y,x,y)
        if distBetween(self.x-self.speed,self.y,x,y)<d:
            r = 2
            d = distBetween(self.x-self.speed,self.y,x,y)
        if distBetween(self.x,self.y+self.speed,x,y)<d:
            r = 3
            d = distBetween(self.x,self.y+self.speed,x,y)
        if distBetween(self.x,self.y-self.speed,x,y) < d:
            r = 4
            d = distBetween(self.x,self.y-self.speed,x,y)
        if distBetween(self.x+self.speed,self.y+self.speed,x,y) < d:
            r = 5
            d = distBetween(self.x+self.speed,self.y+self.speed,x,y)
        if distBetween(self.x-self.speed,self.y+self.speed,x,y) < d:
            r = 6
            d = distBetween(self.x-self.speed,self.y+self.speed,x,y)
        if distBetween(self.x+self.speed,self.y-self.speed,x,y) < d:
            r = 7
            d = distBetween(self.x+self.speed,self.y-self.speed,x,y)
        if distBetween(self.x-self.speed,self.y-self.speed,x,y) < d:
            r = 8
            d = distBetween(self.x-self.speed,self.y-self.speed,x,y)
        return r
    
    def eat(self):
        self.setState(Ant_State.EAT)
        
        self.comida += 1
        self.speed *= 1.5
        self.distance *= 1.5
        
        self.setState(Ant_State.SEARCH)
        
        self.modified = True
        
    def goEat(self,x,y):
        if distBetween(self.x,self.y,x,y) > 3:
            d = self.getFastestWay(x,y)
            if d == 1:
                self.moveleft()
            elif d == 2:
                self.moveright()
            elif d == 3:
                self.moveup()
            elif d == 4:
                self.movedown()
            elif d == 5:
                self.moveupleft()
            elif d == 6:
                self.moveupright()
            elif d == 7:
                self.movedownleft()
            elif d == 8:
                self.movedownright()
            else:
                print("Error")
            for i in range(100000):
                k=0
                k+=1
            return False
        return True

    def goto(self,x,y):
        if distBetween(self.x,self.y,x,y) > self.distance:
            d = self.getFastestWay(x,y)
            if d == 1:
                self.moveleft()
            elif d == 2:
                self.moveright()
            elif d == 3:
                self.moveup()
            elif d == 4:
                self.movedown()
            elif d == 5:
                self.moveupleft()
            elif d == 6:
                self.moveupright()
            elif d == 7:
                self.movedownleft()
            elif d == 8:
                self.movedownright()
            else:
                print("Error")
            for i in range(100000):
                k=0
                k+=1
            return False
        return True

class Main(Tk):
    
    def __init__(self):
        super().__init__()
        
        self.state = Simulation_State.INIC
        
        self.title("[ El Hormiguero ] [ 00:00:00 ] [ STATE = " + str(self.state) + " ]")
        
        self.geometry("700x700")
        
        self.check_ants = {}
        
        self.canvas = Canvas(self, bg="#b5651d",width=700,height=700)
        
        self.x_nest , self.y_nest = getRandomCoordinate()
        self.x_nest+=25
        self.y_nest+=25
        
        self.nest = Nest(self.canvas,self.x_nest,self.y_nest)
        
        self.console_msgs = []
        
        self.console_msgs.append('>> Nest at [' + str(self.nest.x) + ',' + str(self.nest.y) + ']')
        
        self.ants = []
        
        self.foods = []
        
        self.foods.append(Food(self.canvas))
        
        self.console_msgs.append('>> Food at [' + str(self.foods[0].x) + ',' + str(self.foods[0].y) + ']')
        
        self.canvas.pack()
        
        self.canvas.bind('<Button-1>',self.canvas_clic)
        self.canvas.bind('<Button-3>',self.canvas_goto)
        self.canvas.bind('<Button-2>',self.newDefaultAnt)
        
        padding = {'padx': 5, 'pady': 5}
        
        self.menubar = Menu(self)
        self.bar_menu_1 = Menu(self.menubar, tearoff=0)
        
        self.bar_menu_1.add_command(label="Start", command=self.start)
        self.bar_menu_1.add_command(label="Stop", command=self.stop)
        self.bar_menu_1.add_command(label="Restart", command=self.restart)
        self.bar_menu_1.add_separator()
        self.bar_menu_1.add_command(label="Exit", command=self.destroy)
        self.menubar.add_cascade(label="Simulation", menu=self.bar_menu_1)
        
        self.bar_menu_2 = Menu(self.menubar, tearoff=0)
        self.bar_menu_2.add_command(label="New", command=self.newAnt)
        self.menubar.add_cascade(label="Edit", menu=self.bar_menu_2)
        
        self.bar_menu_3 = Menu(self.menubar, tearoff=0)
        self.bar_menu_3.add_command(label="Ants State", command=self.showAntState)
        self.bar_menu_3.add_command(label="Console", command=self.showConsole)
        self.menubar.add_cascade(label="Show", menu=self.bar_menu_3)
        
        self.bar_menu_4 = Menu(self.menubar, tearoff=0)
        self.bar_menu_4.add_command(label="Go to", command=self.newMovement)
        self.bar_menu_4.add_command(label="Return to nest", command=self.returnNest)
        self.menubar.add_cascade(label="Move", menu=self.bar_menu_4)
        
        self.console_var = StringVar(value = self.console_msgs)
        
        self.config(menu = self.menubar)
        
        self.log_state = False
        
        self.console_state = False
        
        self.mainloop()
        
    def showConsole(self):
        
        self.console = Tk()
        
        self.console.title("Console")
        
        self.list_box_console = Listbox(self.console, listvariable = self.console_msgs,height = 20,width = 50,bg='black',fg='white',font='bold')
        
        self.list_box_console.grid(row = 0,column = 0,sticky='nwes')
        
        self.console_scrollbar = ttk.Scrollbar(self.console,orient = 'vertical',command = self.list_box_console.yview)
        
        self.list_box_console['yscrollcommand'] = self.console_scrollbar.set
        
        for msg in self.console_msgs:
            self.list_box_console.insert('end',msg)
        
        self.console_state = True
        
    def updateAntState(self):
        if self.log_state:
            i = 0
            for ant in self.ants:
                if ant.modified == True and self.log_ants[i][0]==ant.name:
                    self.log_ants[i][2].configure(text = ant.comida)
                    self.log_ants[i][3].configure(text = str(ant.speed)[:4])
                    self.log_ants[i][4].configure(text = ant.distance)
                    ant.modified = False
                i += 1
        
    def showAntState(self):
        
        self.log = Tk()
        
        padding = {'padx': 5, 'pady': 5}
        
        self.log_state = True
        
        self.log.title("Ants state")
        
        self.log_state_frm = Frame(self.log)
        self.log_state_frm['bg'] = 'black'
        self.log_state_frm.grid(column=0,row=0)
        Label(self.log_state_frm,text = "Name",font='bold',fg = 'white',bg='black').grid(column = 0,row = 0,**padding)
        Label(self.log_state_frm,text = "Food",font='bold',fg = 'white',bg='black').grid(column = 1,row = 0,**padding)
        Label(self.log_state_frm,text = "Speed",font='bold',fg = 'white',bg='black').grid(column = 2,row = 0,**padding)
        Label(self.log_state_frm,text = "Distance",font='bold',fg = 'white',bg='black').grid(column = 3,row = 0,**padding)
        i = 1
        self.log_ants = []
        for ant in self.ants:
            aux = []
            aux.append(ant.name)
            l = Label(self.log_state_frm,text = ant.name,font='bold',fg = 'white',bg='black')
            l.grid(column = 0,row = i,**padding)
            aux.append(l)
            l = Label(self.log_state_frm,text = ant.comida,fg = 'white',bg='black',font='bold')
            l.grid(column = 1,row = i,**padding)
            aux.append(l)
            l = Label(self.log_state_frm,text = str(ant.speed)[:5],fg = 'white',bg='black',font='bold')
            l.grid(column = 2,row = i,**padding)
            aux.append(l)
            l = Label(self.log_state_frm,text = ant.distance,fg = 'white',bg='black',font='bold')
            l.grid(column = 3,row = i,**padding)
            aux.append(l)
            self.log_ants.append(aux)
            i += 1
        
    def restart(self):
        self.state = Simulation_State.INIC
        for ant in self.ants:
            self.canvas.delete(ant.ant)
        self.ants = []
        self.addToConsole('>> Simulation restarted')
        
    def checkEaten(self):
        if len(self.foods)==0:
            self.foods.append(Food(self.canvas))
        else:
            for ant in self.ants:
                if len(self.foods) > 0:
                    cat_x = abs(ant.x - self.foods[0].x)
                    cat_y = abs(ant.y - self.foods[0].y)
                    hip = int(math.sqrt( cat_x**2 + cat_y**2 ))
                    if hip <= ant.distance:
                        ant.setState(Ant_State.EAT)
                        while not ant.goEat(self.foods[0].x,self.foods[0].y):
                            pass
                        f = ant.comida
                        s = ant.speed
                        d = ant.distance
                        ant.eat()
                        t = '>> ' + ant.name + ' found food!!'
                        self.addToConsole(t)
                        t = '>>>> Food: ' + str(f) + ' -> ' + str(ant.comida)
                        self.addToConsole(t)
                        t = '>>>> Speed: ' + str(s) + ' -> ' + str(ant.speed)[:4]
                        self.addToConsole(t)
                        t = '>>>> Distance: ' + str(d) + ' -> ' + str(ant.distance)
                        self.addToConsole(t)
                        ant.setState(Ant_State.SEARCH)
                        self.canvas.delete(self.foods[0].food)
                        self.foods = []
                        
    def stop(self):
        self.state = Simulation_State.STOP
        self.addToConsole('>> Simulation stopped')
        
    def newDefaultAnt(self,event):
        n = len(self.ants)+1
        self.create("Ant-"+str(n))
        
    def canvas_goto(self,event):
        move = []
        for ant in self.ants:
            if ant.selected:
                move.append(ant)
        while self.moveJust(move,event.x,event.y)==False:
            self.checkEaten()
            pass
        
    def canvas_clic(self,event):
        b_selected = False
        for ant in self.ants:
            if abs(ant.x-event.x)<4 and abs(ant.y-event.y)<4:
                if ant.selected:
                    ant.deselect()
                else:
                    ant.select()
                b_selected = True
        if not b_selected:
            for ant in self.ants:
                ant.selected = False
                self.canvas.itemconfig(ant.ant,fill="black")
        
    def newMovement(self):
        if len(self.ants)>0:
            self.new_movement = Tk()
            self.new_movement.title("New movement")
            i=0
            for ant in self.ants:
                cb = ttk.Checkbutton(self.new_movement,text = ant.name)
                cb.grid(column=0,row=i)
                cb.state(['!selected'])
                self.check_ants[str(ant.name)] = cb
                i+=1
            self.lbl_x_menu = Label(self.new_movement,text="X:")
            self.lbl_x_menu.grid(column=1,row=1)
            self.entry_x_menu = Entry(self.new_movement,width=5)
            self.entry_x_menu.grid(column=2,row=1)
            self.lbl_y_menu = Label(self.new_movement,text="Y:")
            self.lbl_y_menu.grid(column=1,row=2)
            self.entry_y_menu = Entry(self.new_movement,width=5)
            self.entry_y_menu.grid(column=2,row=2)
            self.btn_go_menu = Button(self.new_movement,text="Go",command=self.move)
            self.btn_go_menu.grid(column=1,row=5,columnspan=2)
        
    def newAnt(self):
        self.new_ant = Tk()
        self.new_ant.title("New ant")
        self.new_ant_frm = Frame(self.new_ant)
        self.new_ant_frm.grid(column=0,row=0)
        self.entry_name_menu = Entry(self.new_ant_frm)
        self.entry_name_menu.grid(column=0,row=0,columnspan=4)
        self.btn_ant_menu = Button(self.new_ant_frm,text="Create",command=self.create)
        self.btn_ant_menu.grid(column=4,row=0)
        
    def create(self,e=None,name=''):
        if name != '':
            name = str(self.entry_name_menu.get())
            self.entry_name_menu.delete(0,END) 
        self.ants.append(Ant(self.canvas,self.nest.x,self.nest.y,name))
        t = '>> ' + self.ants[-1].name + ' at [' + str(self.ants[-1].x) + ',' + str(self.ants[-1].y) + ']'
        self.addToConsole(t)
        
    def returnNest(self):
        while not self.moveNest():
            self.checkEaten()
            pass
        
    def addToConsole(self,s):
        if self.console_state:
            self.list_box_console.insert('end',s)
        else:
            self.console_msgs.append(s)
        
    def start(self):
        self.state = Simulation_State.PLAY
        self.addToConsole('>> Simulation started')
        for ant in self.ants:
            ant.setState(Ant_State.SEARCH)
        st = datetime.now()
        while True:
            if self.state == Simulation_State.STOP:
                for ant in self.ants:
                    ant.setState(Ant_State.STOP)
                break
            elif self.state == Simulation_State.PLAY:
                while True:
                    if self.state == Simulation_State.PLAY:
                        self.moveAll()
                        diff = (datetime.now() - st)
                        t = "[ El hormiguero ] [ "+ str(diff)[:7] + " ] [ STATE = PLAY ]"
                        self.title(t)
                        self.checkEaten()
                        pass
                    else:
                        break
            else:
                break
        
    def move(self):
        for n,cb in self.check_ants.items():
            st = ''
            if len(list(cb.state()))>0:
                lst = list(cb.state())
                st = lst[0]
                if st=='focus' and len(lst)>1:
                    st = lst[1]
                elif st == 'focus' and len(lst)<2:
                    st = ''
            if st=='selected' or st=='alternate':
                x = self.entry_x_menu.get()
                if x=='':
                    x=0
                else:
                    x = int(x)
                y = self.entry_y_menu.get()
                if y=='':
                    y = 0
                else:
                    y = int(y)
                while self.moveJust(n,x,y)==False:
                    self.checkEaten()
                    pass
        
    def moveJust(self,ants,x,y):
        b = True
        for a in ants:
            if not a.goto(x,y):
                b = False
        return b
    
    def moveNest(self):
        b = True
        for ant in self.ants:
            if not ant.goto(self.nest.x+25,self.nest.y+25):
                b = False
        return b
    
    def moveAll(self):
        b = True
        for ant in self.ants:
            if not ant.gotoDirection():
                b = False
        self.updateAntState()
        return b

m = Main()