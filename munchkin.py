from tkinter import *
from tkinter import ttk
import ttkbootstrap as ttkb
from PIL import Image, ImageTk

class Juego(Tk):
    n_var=0
    n_jugadores=0
    jugadores = []
    jugadores_entry = []
    maxLevel=10
    
    def __init__(self):
        super().__init__()
        self.title('Munchkin')

        self.n_var = StringVar()
        
        padding = {'padx': 5, 'pady': 5}
        
        self.frm_sup = Frame(self)
        self.frm_sup.grid(column=0,row=0)
        
        self.img = PhotoImage(file='m.png')
        self.img = self.img.subsample(2,2)
        
        self.image = Label(self.frm_sup,image=self.img)
        self.image.grid()
        
        self.frm_inf = Frame(self)
        self.frm_inf.grid(column=0,row=1)
        
        self.lbl1 = ttkb.Label(self.frm_inf, text='Número de Jugadores:')
        self.lbl1.grid(column=0, row=1, **padding)

        self.nplayers_entry = ttkb.Entry(self.frm_inf, textvariable=self.n_var)
        self.nplayers_entry.grid(column=1, row=1, **padding)
        self.nplayers_entry.focus()

        self.button1 = ttkb.Button(self.frm_inf, text='Siguiente', command=self.create_rows)
        self.button1.grid(column=2, row=1, **padding)
        
    def clear(self):
        for widget in self.frm_inf.winfo_children():
            widget.destroy()
            
    def checkWinner(self):
        for j in self.jugadores:
            if j.getLevel()==self.maxLevel:
                return True,j
        return False
    
    def start(self):
        self.clear()
        size = (self.n_jugadores*20)+200
        size="404x"+str(int(size))
        self.geometry(size)
        i = 0
        
        padding = {'padx': 5, 'pady': 5}
        
        for jugador in self.jugadores:
            ttkb.Label(self.frm_inf,text=jugador.getName(),font="25").grid(column=0,row=i,**padding)
            ttkb.Label(self.frm_inf,text=jugador.getLevel(),font="25").grid(column=1,row=i,**padding)
            ttkb.Button(self.frm_inf,text="+",command=jugador.levelUp,width=5,bootstyle="success").grid(column=2,row=i,**padding)
            ttkb.Button(self.frm_inf,text="-",command=jugador.levelDown,width=5,bootstyle="danger").grid(column=3,row=i,**padding)
            i+=1
    def create_rows(self):
        self.n_jugadores = int(self.n_var.get())
        self.button1.destroy()
        self.lbl1.destroy()
        self.nplayers_entry.destroy()
        padding = {'padx': 5, 'pady': 5}
        size=(self.n_jugadores*40)+200
        size="404x"+str(int(size))
        self.geometry(size)
        for i in range(self.n_jugadores):
            t="Jugador "+str(i+1)
            ttkb.Label(self.frm_inf, text=t).grid(column=0, row=i+1, **padding)

            self.jugadores_entry.insert(i,ttkb.Entry(self.frm_inf)) 
            self.jugadores_entry[i].grid(column=1, row=i+1, **padding)
        
        button2 = ttkb.Button(self.frm_inf, text='Siguiente', command=self.create_players)
        button2.grid(column=1, row=self.n_jugadores+1)
    
    def create_players(self):
        for i in range(self.n_jugadores):
            name = self.jugadores_entry[i].get()
            self.jugadores.insert(i,Jugador(name))
        
        self.start()
        
class Jugador:
    nombre=""
    nivel=1
    global j
    
    def __init__(self,n):
        self.nombre=str(n)
        
    def levelUp(self):
        if self.nivel<10:
            self.nivel+=1
        j.start()
        
    def levelDown(self):
        if self.nivel>1:
            self.nivel-=1
        j.start()
        
    def getName(self):
        return self.nombre
    
    def getLevel(self):
        return self.nivel
            
j = Juego()
j.mainloop()
    