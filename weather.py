from tkinter import *
from tkinter import ttk
import requests,json,base64



class Main(Tk):
    
    padding = {'padx':5 , 'pady':5}
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "ee25b100273576f22a1749113d140a8c"
    icons = []
    
    def __init__(self):
        super().__init__()
        
        self.title('Weather application')
        
        self.frm = Frame(self)
        self.frm.grid(row = 0)
        
        self.entry = Entry(self.frm,width = 15)
        self.entry.grid(column = 0,row = 0, **self.padding)
        
        self.btn = Button(self.frm,text='Search',command = self.search)
        self.btn.grid(column = 1,row = 0, **self.padding)
        
        self.frm_search = Frame(self)
        self.frm_search.grid(column=0,row = 1,columnspan = 2)
        
        self.mainloop()
        
    def search(self):
        city = str(self.entry.get())
        if city != '':
            url = self.BASE_URL + "q=" + city + "&appid=" + self.API_KEY
            response = requests.get(url)
            code = response.status_code
            if code == 200:
                data = response.json()
                self.paintSearch(data)
            elif code == 404:
                self.paintCityNotFound()
            else:
                self.paintError(response.status_code,json.loads(response.content)['message'])
                
    def clearSearch(self):
        for widget in self.frm_search.winfo_children():
            widget.destroy()
            
    def paintError(self,code,content):
        self.clearSearch()
        t = 'Error ' + code + ': ' + content
        Label(self.frm_search,text = t,font = ('Arial',12,'bold')).grid(column=0,row=0,columnspan=2,**self.padding)
    
    def paintCityNotFound(self):
        self.clearSearch()
        t = 'Error 404: City not found'
        Label(self.frm_search,text = t,font = ('Arial',12,'bold')).grid(column=0,row=0,columnspan=2,**self.padding)
                
    def paintSearch(self,data):
        self.clearSearch()
            
        t = data['name'] + ' ('+ data['sys']['country'] +')'
        Label(self.frm_search,text = t,font = ('Arial',12,'bold')).grid(column = 0,row = 0,**self.padding)
        icon_id = data['weather'][0]['icon']
        url = 'http://openweathermap.org/img/wn/' + icon_id + '.png'
        response = requests.get(url)
        self.icons.append(PhotoImage(data = base64.encodebytes(response.raw.read())))
        self.lbl_icon = Label(self.frm_search,width = 50,height=50)
        self.lbl_icon.grid(column = 1,row = 0)
        self.lbl_icon.configure(image = self.icons[-1])
        
        Label(self.frm_search,text = "Temperatura:",font = ('Arial',12)).grid(column = 0,row = 1,**self.padding)
        temp = str(data['main']['temp'] - 273)[:5]
        lbl = temp + 'ºC'
        Label(self.frm_search,text = lbl,font = ('Arial',12)).grid(column=1,row=1,**self.padding)
        
        Label(self.frm_search,text = "Min - Max:",font = ('Arial',12)).grid(column = 0,row = 2,**self.padding)
        min_temp = str(data['main']['temp_min'] - 273)[:5]
        max_temp = str(data['main']['temp_max'] - 273)[:5]
        lbl = '[ ' + min_temp + 'ºC - ' + max_temp + 'ºC ]'
        Label(self.frm_search,text = lbl,font = ('Arial',12)).grid(column=1,row=2,**self.padding)
        
        Label(self.frm_search,text = 'Humedad:', font=('Arial',12)).grid(column=0,row=4,**self.padding)
        hum = data['main']['humidity']
        lbl = str(hum) + '%'
        Label(self.frm_search,text = lbl, font=('Arial',12)).grid(column=1,row=4,**self.padding)
        
        Label(self.frm_search,text = 'Viento:', font=('Arial',12)).grid(column=0,row=5,**self.padding)
        wind = data['wind']['speed']
        lbl = str(wind) + 'm/s'
        Label(self.frm_search,text = lbl, font=('Arial',12)).grid(column=1,row=5,**self.padding)        
Main()
