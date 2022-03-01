from tkinter import *
from enum import Enum
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Color(Enum):
    GRAY="#73776e"
    GREEN="#3ed12e"
    YELLOW="#e1e829"
    WHITE="white"
    
class Palabra(Enum):
    Paces="PACES",
    Nacer="NACER",
    Vacio="VACIO",
    Zafio="ZAFIO",
    Boxer="BOXER",
    Busto="BUSTO",
    Burro="BURRO",
    Burla="BURLA",
    Bufon="BUFON",
    Bufet="BUFET",
    Bueno="BUENO",
    Bucal="BUCAL",
    Bingo="BINGO",
    Codex="CODEX",
    Cenit="CENIT",
    Comic="COMIC",
    Caliz="CALIZ",
    Conos="CONOS",
    Debil="DEBIL",
    Dulce="DULCE",
    Dogma="DOGMA",
    Drama="DRAMA",
    Fosil="FOSIL",
    Femur="FEMUR",
    Fumar="FUMAR",
    Freno="FRENO",
    Guiso="GUISO",
    Guapo="GUAPO",
    Gusto="GUSTO",
    Grumo="GRUMO",
    Hurto="HURTO",
    Huevo="HUEVO",
    Hotel="HOTEL",
    Justo="JUSTO",
    Jugar="JUGAR",
    Jarra="JARRA",
    Kioto="KIOTO",
    Karma="KARMA",
    Lemur="LEMUR",
    Lunar="LUNAR",
    Movil="MOVIL",
    Multa="MULTA",
    Morir="MORIR",
    Novel="NOVEL",
    Natal="NATAL",
    Pauta="PAUTA",
    Pausa="PAUSA",
    Patan="PATAN",
    Rimel="RIMEL",
    Regla="REGLA",
    Surco="SURCO",
    Solar="SOLAR",
    Tunel="TUNEL",
    Trufa="TRUFA",
    Tiara="TIARA",
    Tarta="TARTA",
    Video="VIDEO",
    Voraz="VORAZ",
    Vimos="VIMOS",
    Valle="VALLE",
    Zanco="ZANCO",
    Zanja="ZANJA",
    Donde="DONDE",
    Letra="LETRA",
    Color="COLOR",
    Plato="PLATO",
    Perro="PERRO",
    Dedos="DEDOS",
    Angel="ANGEL",
    Ataud="ATAUD",
    Posar="POSAR",
    Cupon="CUPON",
    Himno="HIMNO",
    Arena="ARENA",
    Coser="COSER",
    Anyejo="AÑEJO",
    Amiga="AMIGA",
    Calle="CALLE",
    Caida="CAIDA",
    Cisne="CISNE",
    Fresa="FRESA",
    Disco="DISCO",
    Libro="LIBRO",
    Silla="SILLA",
    Lapiz="LAPIZ",
    Danza="DANZA",
    Vuela="VUELA",
    Apodo="APODO",
    Etapa="ETAPA",
    Hielo="HIELO",
    Cielo="CIELO",
    Sonar="SONAR",
    Suenya="SUEÑA",
    Marca="MARCA",
    Mutar="MUTAR"

class Letras():
    
    fondo = "#d3d6cf"
    
    def __init__(self,parent):
        self.letras = []
        for i in range(97,123):
            if i==111:
                lbl = Label(parent,text="Ñ",font=('Arial',17,'bold'))
                lbl.configure(bg=self.fondo)
                self.letras.append(lbl)
                lbl.pack(side=LEFT)
            
            l = str(chr(i)).upper()
            lbl = Label(parent,text=l,font=('Arial',17,'bold'))
            lbl.configure(bg=self.fondo)
            self.letras.append(lbl)
            lbl.pack(side=LEFT)
        
    def setLetra(self,l,c):
        if l=="Ñ":
            self.letras[14].configure(bg=c.value)
        elif ord(l)>ord('N'):
            i = ord(l)-65
            self.letras[i+1].configure(bg=c.value)
        else:
            i = ord(l)-65
            self.letras[i].configure(bg=c.value)
    
class Cuadro():
    frm=""
    lbl=""
    letra=""
    estado=Color.WHITE
    grid=""
    fondo = "#d3d6cf"
    
    def __init__(self,parent,l,e,pos):
        self.frm = Frame(parent,width=50,height=50,highlightbackground="black", highlightthickness=1)
        self.frm.grid(row=0,column=pos,padx=15)
        self.lbl = Label(self.frm)
        self.lbl.pack(padx=10,pady=10)
    
    def __init__(self,parent,col,ro):
        self.frm = Frame(parent,width=50,height=50,highlightbackground="black", highlightthickness=1)
        self.frm.grid(row=ro,column=col,padx=10,pady=5)
        self.lbl = Label(self.frm,font=30,bg=Color.WHITE.value,width=2)
        self.lbl.pack(expand=YES,padx=10,pady=10)
        self.setEstado(Color.WHITE)
        self.grid=ro
    
    def setCuadro(self,l,c):
        self.letra=l
        self.estado=c
        self.lbl.configure(text=self.letra,font=30,bg=self.estado.value)
        self.frm.configure(bg=self.estado.value)
        
    def setEstado(self,e):
        self.estado=e
        self.frm.configure(bg=self.estado.value)
    
class Grid():
    
    def __init__(self,parent,row):
        self.parent=parent
        self.row=row
        self.cuadros = []
        for i in range(5):
            self.cuadros.append(Cuadro(self.parent,i,self.row))
            
    def setGrid(self,pos,l,c):
        self.cuadros[pos].setCuadro(l.upper(),c)
        return self
    
    def restart(self):
        self.cuadros= []
        for i in range(5):
            self.cuadros.append(Cuadro(self.parent,i,self.row))
    
    
class Wordl(Tk):
    
    frm_sup="" # Entry y boton de Probar
    frm_med="" # Cuadrados con las palabras escogidas
    frm_inf="" # Ristra del estado de cada letra
    word_entry=""
    guess_button=""
    palabra=""
    intento=0
    maxIntentos=5
    game=0
    ganadas=0
    
    grids = []
    
    def __init__(self,f):
        super().__init__()
        self.fondo=f
        t = "My Wordle ("+str(self.ganadas)+"/"+str(self.game)+")"
        self.title(t)
        
        self.geometry("600x430")
        
        print("100 palabras añadidas")
        
        self.palabra = self.nextPalabra()
        
        #Frame superior
        self.frm_sup = Frame(self,width=350,height=50)
        self.frm_sup.configure(bg=self.fondo)
        self.frm_sup.pack(side=TOP,pady=10)
        
        self.word_entry = Entry(self.frm_sup)
        self.word_entry.configure(bg=self.fondo)
        self.word_entry.grid(row=0,column=0,padx=10)
        
        self.guess_button = Button(self.frm_sup,command=self.check,text="Guess")
        self.guess_button.configure(bg=self.fondo)
        self.guess_button.grid(row=0,column=1,padx=10)
        
        #self.guess_button.focus()
        
        #Frame intermedio
        self.frm_med = Frame(self,width=550,height=350)
        self.frm_med.configure(bg=self.fondo)
        self.frm_med.pack(side=TOP,pady=5)
        
        self.grids.append(Grid(self.frm_med,0))
        self.grids.append(Grid(self.frm_med,1))
        self.grids.append(Grid(self.frm_med,2))
        self.grids.append(Grid(self.frm_med,3))
        self.grids.append(Grid(self.frm_med,4))
        self.grids.append(Grid(self.frm_med,5))
        
        #Frame inferior
        self.frm_inf = Frame(self,width=550,bg=self.fondo)
        self.frm_inf.pack(side=TOP)
        
        self.ltrs = Letras(self.frm_inf)
        
    def start(self):
        self.mainloop()
        
    def restart(self):
        self.geometry("600x430")
        
        for w in self.frm_med.winfo_children():
            w.destroy()
        for w in self.frm_inf.winfo_children():
            w.destroy()
            
        self.palabra=self.nextPalabra()
        
        self.intento = 0
        
        self.word_entry = ttk.Entry(self.frm_sup)
        self.word_entry.grid(row=0,column=0,padx=10)
        
        self.guess_button = ttk.Button(self.frm_sup,command=self.check,text="Guess",bootstyle="secondary")
        self.guess_button.grid(row=0,column=1,padx=10)
        
        for grid in self.grids:
            grid.restart()
        
        self.ltrs = Letras(self.frm_inf)
    
    def nextPalabra(self):
        p = str(random.choice(list(Palabra)))
        p = p[p.rfind(".")+1:]
        print("La palabra es",p)
        return p
        
    def paint(self,guess,i):
        x=0
        winner=True
        g = self.grids[i]
        for c in guess:
            if c.lower()==self.palabra[x].lower():
                g.setGrid(x,c,Color.GREEN)
                self.ltrs.setLetra(c.upper(),Color.GREEN)
            elif c.lower() in self.palabra.lower():
                g.setGrid(x,c,Color.YELLOW)
                self.ltrs.setLetra(c.upper(),Color.YELLOW)
                winner=False
            else:
                g.setGrid(x,c,Color.GRAY)
                self.ltrs.setLetra(c.upper(),Color.GRAY)
                winner=False
            x+=1
        return winner
    
    def win(self):
        self.ganadas+=1
        self.game+=1
        t = "My Wordle ("+str(self.ganadas)+"/"+str(self.game)+")"
        self.title(t)
        for widget in self.frm_sup.winfo_children():
            widget.destroy()
        for widget in self.frm_inf.winfo_children():
            widget.destroy()
            
        self.geometry("600x500")    
        t = str(self.intento+1)+"/6"
        Label(self.frm_inf,text=t,font=("Arial",15,'bold')).pack()
        if self.intento+1==1:
            t = "IN-CRE-Í-BLE"
        if self.intento+1==2:
            t = "Wow! Lo adivinaste muy rápido!"
        if self.intento+1==3:
            t = "Muy bien! Eres bueno"
        if self.intento+1==4:
            t = "Lo conseguiste!"
        if self.intento+1==5:
            t = "Por los pelos!"
        if self.intento+1==6:
            t = "Uuy!! En el último intento!!"
        Label(self.frm_inf,text=t,font=("Arial",15,'bold')).pack()
        ttk.Button(self.frm_inf,text="Volver a jugar",command=self.restart,bootstyle="secondary").pack()
            
    def lose(self):
        self.game+=1
        t = "My Wordle ("+str(self.ganadas)+"/"+str(self.game)+")"
        self.title(t)
        for widget in self.frm_sup.winfo_children():
            widget.destroy()
        for widget in self.frm_inf.winfo_children():
            widget.destroy()
            
        self.geometry("600x500")    
        t = "X/6"
        Label(self.frm_inf,text=t,font=("Arial",15,'bold')).pack()
        t = "Suerte en la próxima! La palabra era " + self.palabra.upper()
        Label(self.frm_inf,text=t,font=("Arial",15,'bold')).pack()
        ttk.Button(self.frm_inf,text="Volver a jugar",command=self.restart,bootstyle="secondary").pack()
        
    def check(self):
        guess = str(self.word_entry.get())
        for i in range(len(guess)):
            self.word_entry.delete(0)
        if len(guess)!=5:
            print("")
        else:
            if self.intento < self.maxIntentos:
                res = self.paint(guess,self.intento)
                if res==True:
                    self.win()
                else:
                    self.intento+=1
            else:
                res = self.paint(guess,self.intento)
                if res:
                    self.win()
                else:
                    self.lose()
                
w = Wordl("#d3d6cf")
w['bg']="#d3d6cf"
w.start()