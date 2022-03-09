from tkinter import *
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from enum import Enum
import random
import numpy

class Pregunta():
    def __init__(self,q,r,s):
        self.pregunta = q
        self.respuestas = r
        self.sol = s
        self.str_sol = self.respuestas[s]
        
    def check(self,arg):
        if arg[0].cget('bg')=="#4c4c7f" and self.str_sol==arg[0].cget('text'):
            return True,0
        if arg[1].cget('bg')=="#4c4c7f" and self.str_sol==arg[1].cget('text'):
            return True,1
        if arg[2].cget('bg')=="#4c4c7f" and self.str_sol==arg[2].cget('text'):
            return True,2
        if arg[3].cget('bg')=="#4c4c7f" and self.str_sol==arg[3].cget('text'):
            return True,3
        i = 0
        for lbl in arg:
            if arg[i].cget('text')==self.str_sol:
                return False,i
            else:
                i+=1

class Main(Tk):
    
    preguntas = 0
    
    def __init__(self,p):
        super().__init__()
        
        self.lst_preguntas = p
        
        self.lst_usadas = []
        
        self.prev_Q = ""
        
        self.title("¿Quién quiere ser millonario?")
        
        self.geometry("400x500")
        
        self.init()
        
        self.mainloop()
        
    def init(self):
        for i in self.winfo_children():
            i.destroy()
            
        self.frm = Frame(self).grid()
        self['bg']="#202060"
        
        self.img = PhotoImage(file='mill.png')
        self.img = self.img.subsample(2,2)
        self.lbl = Label(self.frm,image = self.img,bg="#202060")
        self.lbl.place(anchor="c", relx=.5, rely=.25)
        
        self.btn = Button(self.frm,text="Empezar",command=self.start)
        self.btn.place(anchor="c", relx=.5, rely=.55)
        
    def start(self):
        for i in self.winfo_children():
            i.destroy()
            
        t = "Pregunta: "+str(self.preguntas+1)
        self.lbl_info1 = Label(self.frm,text=t,font=("Arial 13 bold"), bg="#202060",fg="white").place(anchor="c", relx=.5, rely=.05)
        
        self.frm_ask = LabelFrame(self.frm,height=450,width=375,bg="#202060")
        self.frm_ask.place(anchor="c", relx=.5, rely=.525)
        
        self.insertQuestion()
        
    def nextQuestion(self):
        if len(self.lst_usadas) == len(self.lst_preguntas):
            return "1"
        q = random.choice(list(self.lst_preguntas))
        while q in self.lst_usadas:
            q = random.choice(list(self.lst_preguntas))
        self.prev_Q = q.pregunta
        return q
        
    def insertQuestion(self):
        q = self.nextQuestion()
        if q=="1":
            self.win()
            return
        self.lst_usadas.append(q)
        size = len(q.pregunta)
        t = q.pregunta
        if size>42:
            t = self.editQuestion(t)
        lbl = Label(self.frm_ask,text = t,bg="#202060",fg="white",font='bold')
        lbl.place(anchor='c',relx=.5,rely=.1)
        
        resp = q.respuestas
        random.shuffle(resp)
        
        self.opt1 = Label(self.frm_ask,text = resp[0], fg="white", font= ('bold'),bg="#202060", width = 35)
        self.opt1.place(anchor='c',relx=0.5,rely=0.25)
        self.opt1.bind('<Button-1>', lambda e: self.select(0))
        self.opt2 = Label(self.frm_ask,text = resp[1], fg="white", font= ('bold'),bg="#202060", width = 35)
        self.opt2.place(anchor='c',relx=0.5,rely=0.4)
        self.opt2.bind('<Button-1>', lambda e: self.select(1))
        self.opt3 = Label(self.frm_ask,text = resp[2], fg="white", font= ('bold'),bg="#202060", width = 35)
        self.opt3.place(anchor='c',relx=0.5,rely=0.55)
        self.opt3.bind('<Button-1>', lambda e: self.select(2))
        self.opt4 = Label(self.frm_ask,text = resp[3], fg="white", font= ('bold'),bg="#202060", width = 35)
        self.opt4.place(anchor='c',relx=0.5,rely=0.7)
        self.opt4.bind('<Button-1>', lambda e: self.select(3))
        
        arg = [self.opt1,self.opt2,self.opt3,self.opt4]
        
        self.game_btn = Button(self.frm_ask,text="Contestar",command = lambda: self.check(q,resp,arg))
        self.game_btn.place(anchor='c',relx=0.5,rely=0.875)
        
    def editQuestion(self,t):
        res = ""
        i = 0
        jump = False
        for c in t:
            if i > ( (len(t) / 2) - 5) and i < ( (len(t) / 2 ) + 5):
                if not jump and c==" ":
                    res+="\n"
                    jump = True
                else:
                    res+=str(c)
            else:
                res+=str(c)
            i+=1
        return res
    
    def check(self,q,resp,arg):
        b , p = q.check(arg)
        if b:
            self.preguntas+=1
            self.paintSolution(p)
        else:
            self.paintError(p)
            
    def paintSolution(self,p):
        if p==0:
            self.opt1.configure(bg="#68BB59")
        if p==1:
            self.opt2.configure(bg="#68BB59")
        if p==2:
            self.opt3.configure(bg="#68BB59")
        if p==3:
            self.opt4.configure(bg="#68BB59")
        self.game_btn.configure(text = "Continuar")
        self.game_btn.configure(command = self.start)
        
    def paintError(self,p):
        if self.opt1.cget("bg")=="#4c4c7f":
            self.opt1.configure(bg="#ff1f17")
        if self.opt2.cget("bg")=="#4c4c7f":
            self.opt2.configure(bg="#ff1f17")
        if self.opt2.cget("bg")=="#4c4c7f":
            self.opt2.configure(bg="#ff1f17")
        if self.opt3.cget("bg")=="#4c4c7f":
            self.opt3.configure(bg="#ff1f17")
        if p==0:
            self.opt1.configure(bg="#68BB59")
        if p==1:
            self.opt2.configure(bg="#68BB59")
        if p==2:
            self.opt3.configure(bg="#68BB59")
        if p==3:
            self.opt4.configure(bg="#68BB59")
        self.game_btn.configure(text = "Continuar")
        self.game_btn.configure(command = self.lose)
            
    def win(self):
        for i in self.winfo_children():
            i.destroy()
            
        t = "Felicidades! Has acertado " + str(self.preguntas) + " preguntas"
        
        self.img = PhotoImage(file='mill.png')
        self.img = self.img.subsample(2,2)
        self.lbl = Label(self.frm,image = self.img,bg="#202060")
        self.lbl.place(anchor="c", relx=.5, rely=.25)
        
        Label(self.frm,text = t, font=('bold'),bg="#202060",fg="white").place(anchor="c", relx=.5, rely=.525)
        
        t = "¡¡¡¡ Acabas de ganar 1.000.000 € !!!!"
        
        Label(self.frm,text = t, font=('bold'),bg="#202060",fg="white").place(anchor="c", relx=.5, rely=.625)
            
    def lose(self):
        for i in self.winfo_children():
            i.destroy()
            
        t = "Felicidades! Has acertado " + str(self.preguntas) + " preguntas"
        
        self.preguntas = 0
            
        self.img = PhotoImage(file='mill.png')
        self.img = self.img.subsample(2,2)
        self.lbl = Label(self.frm,image = self.img,bg="#202060")
        self.lbl.place(anchor="c", relx=.5, rely=.25)
        
        Label(self.frm,text = t, font=('bold'),bg="#202060",fg="white").place(anchor="c", relx=.5, rely=.525)
        
        Button(self.frm,text="Reiniciar",command=self.init).place(anchor="c", relx=.5, rely=.65)
        
    def select(self,i):
        if i==0:
            self.opt1.configure(bg="#4c4c7f")
            self.opt2.configure(bg="#202060")
            self.opt3.configure(bg="#202060")
            self.opt4.configure(bg="#202060")
        if i==1:
            self.opt1.configure(bg="#202060")
            self.opt2.configure(bg="#4c4c7f")
            self.opt3.configure(bg="#202060")
            self.opt4.configure(bg="#202060")
        if i==2:
            self.opt1.configure(bg="#202060")
            self.opt2.configure(bg="#202060")
            self.opt3.configure(bg="#4c4c7f")
            self.opt4.configure(bg="#202060")
        if i==3:
            self.opt1.configure(bg="#202060")
            self.opt2.configure(bg="#202060")
            self.opt3.configure(bg="#202060")
            self.opt4.configure(bg="#4c4c7f")
 
prs = []
        
r = ["Neptuno","Urano","Saturno","Tierra"]    
p = Pregunta("¿Cuál de estos planetas está más cercano al sol?",r,3)

prs.append(p)

r = ["Thor","Capitán América","Iron Man","Wolverine"]
p = Pregunta("¿Qué trilogía de las películas basadas en los cómics de Marvel recaudó más dinero en taquilla?",r,2)

prs.append(p)

r = ["Tirso","Talión","Vareta","Mástil"]
p = Pregunta("La vara que suele llevar como cetro el Dios de la mitología romana Baco se llama:",r,0)

prs.append(p)

r = ["O. Pacífico","O. Índico","O. Antártico","O. Atlántico"]
p = Pregunta("¿Cuál es el océano más grande del mundo?",r,0)

prs.append(p)

r = ["Talmud","Torá","Kojiki","Corán"]
p = Pregunta("¿Como se llama el libro sagrado de la cultura Islámica?",r,3)

prs.append(p)

r = ["Enfermedad de Addison","Progeria de Hutchinson-Gilford","Esclerosis Lateral Amiotrófica","Síndrome de Marfan"]
p = Pregunta("¿Qué enfermedad tenía el legendario astrofísico Stephen Hawking?",r,2)

prs.append(p)

r = ["Sufragio","Adagio","Naufragio","Prestigio"]
p = Pregunta("El sistema electoral para determinar las personas que ocuparan cargos publicos:",r,0)

prs.append(p)

r = ["Irritable","Hambrienta","Furiosa","Asustada"]
p = Pregunta("Una persona famelica esta:",r,1)

prs.append(p)

r = ["Cejas","Pupilas","Párpados","Anteojos"]
p = Pregunta("Son las membranas movibles cubiertas de piel que resguardan los ojos:",r,2)

prs.append(p)

r = ["Calcio","Pigmentación","Vitamina A","Oxígeno"]
p = Pregunta("El albinismo se presenta por la carencia de:",r,1)

prs.append(p)

r = ["Dinammómetro","Micrómetro","Oleómetro","Holómetro"]
p = Pregunta("¿Cual de estos instrumentos mide la densidad de los aceites?",r,2)

prs.append(p)

r = ["Escuchado","Contado","Dicho","Aprendido"]
p = Pregunta("Complete el siguiente trabalenguas: 'Me han dicho que has dicho un dicho, un dicho que he..'",r,2)

prs.append(p)

r = ["El amor","La esperanza","El odio","La envidida"]
p = Pregunta("Según el refran, ¿quien es ciego?",r,0)

prs.append(p)

r = ["Serigrafía","Epigrafía","Holografía","Topografía"]
p = Pregunta("Técnica que describe y representa detalladamente la superficie de un terreno:",r,3)

prs.append(p)


Main(prs)