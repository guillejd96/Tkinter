from tkinter import *
from tkinter import ttk
from enum import Enum
from googletrans import Translator

class Language(Enum):
    SPANISH = 'es'
    ENGLISH = 'en'
    FRENCH = 'fr'
    JAPANESE = 'ja'
    RUSSIAN = 'ru'
    GERMAN = 'de'
    PORTUGUESE = 'pt'
    ESPERANTO = 'eo'
    TELUGU = 'te'
    SAMOAN = 'sm'
    LAO = 'lo'
    AFRICAN = 'af'
    CEBUAN = 'ceb'
    

class Main(Tk):
    
    padding = {'padx': 5, 'pady': 10}
    
    def __init__(self):
        super().__init__()
        
        self.translator = Translator()
        
        self.title("My translator")
        
        self.resizable(False,False)
        
        #self.geometry("500x600")
        
        self.frm = Frame(self)
        self.frm.grid()
        
        self.f_frm = Frame(self.frm,width = 500,height = 200)
        self.f_frm.grid(column = 0,row = 0,columnspan = 3)
        
        self.l_frm = Frame(self.frm, width = 225,height = 300)
        self.l_frm.grid(column=0,row=1,**self.padding)
        
        self.c_frm = Frame(self.frm, width = 55,height = 300)
        self.c_frm.grid(column=1,row=1,**self.padding)
        
        self.r_frm = Frame(self.frm, width = 225,height = 300)
        self.r_frm.grid(column=2,row=1,**self.padding)
        
        self.d_frm = Frame(self.frm,width = 500,height = 100)
        self.d_frm.grid(column = 0,row = 2,columnspan = 3)
        
        self.text = Text(self.l_frm,width = 24, height = 22, font=('Arial' , 12))
        self.text.grid()
        
        self.btn_translate = Button(self.c_frm,text='Go',command = self.translate)
        self.btn_translate.grid(**self.padding)
        
        self.lbl = Label(self.r_frm,text='',font=('Arial',12),width = 24,wraplength=200,bg='gray',height = 22)
        self.lbl.grid(sticky='n')
        
        self.str_var_d = StringVar()
        self.combobox = ttk.Combobox(self.f_frm,textvariable = self.str_var_d)
        self.combobox['values'] = [str(e)[9:] for e in Language]
        self.combobox['state'] = 'readonly'
        self.combobox.grid(column=2,row=0,**self.padding)
        
        self.d_lbl = Label(self.d_frm,width = 30, font=('Arial',12))
        self.d_lbl.grid(**self.padding)
        
        self.geometry("500x500")
        
        self.mainloop()
        
    def set_d_lbl(self,s):
        self.d_lbl.configure(text = s)
        
    def translate(self):
        str_entry = str(self.text.get(1.0, "end-1c"))
        d = self.str_var_d.get()
        lan_d = 'en'
        for e in Language:
            if str(e)[9:] == d:
                lan_d = e.value
        if str_entry != '':
            trad = self.translator.translate(str_entry , dest = lan_d)
            self.lbl.configure(text = trad.__dict__()["text"])
#             print(trad.__dict__())
            t = 'Translated from '
            x = ''
            for e in Language:
                if trad.__dict__()['src'] == e.value:
                    x = str(e)[9:]
            if x == '':
                x = trad.__dict__()['src']
            if d == '':
                d = 'ENGLISH'
            t += x + ' to ' + d
            self.set_d_lbl(t)
        
Main()