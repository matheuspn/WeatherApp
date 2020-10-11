import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest

import json
import requests


kivy.require('1.11.1') 

# Setting size to resizable 
Config.set('graphics', 'resizable', 1) 
Config.set('graphics', 'width', '300') 
Config.set('graphics', 'height', '400') 

with open("apikey.txt") as f:
    openweatherkey = f.read()

def weather(response):
    print("OK")
    weatherdict = json.loads(response)
    with open("testefile.txt", "a") as f:
        for key, value in weatherdict.items():
            f.write('{}: {}'.format(key, value))
    print(weatherdict["weather"])

def falha(req, erro):
    print(erro)

class TempGrid(GridLayout):

    global openweatherkey

    def button_press(self, country, city):
        response = requests.post(f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={openweatherkey}")
        print("B")
        print("Resposta : ",response.text)
        weather(response.text)
        


class TempApp(App):
    def build(self):
        return TempGrid()

if __name__ == "__main__":
    TempApp().run()