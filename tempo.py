import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty

import json
import requests
from urllib.parse import quote


kivy.require('1.11.1') 

# Setting size to resizable 
Config.set('graphics', 'resizable', 1) 
Config.set('graphics', 'width', '300') 
Config.set('graphics', 'height', '400') 

# getting the api key
with open("apikey.txt") as f:
    openweatherkey = f.read()

class TempGrid(GridLayout):

    show = ObjectProperty(None)

    global openweatherkey

    def button_press(self, country, city):

        url = quote(f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={openweatherkey}",
                    safe= ':,/,=,&,?')
        print(url)
        UrlRequest(url,on_success=self.answer, on_error=self.urlfail)

    # the response of Urlrequest
    def answer(self, req, result):

        # for test purpose
        with open("testefile.txt", "a") as f:
            for key, value in result.items():
                f.write(f'{key}: {value} ')
            f.write('\n')
        print(result, "\n")
        print(result["weather"], "\n")
        print("Urlrequest working correctly!")
        print(result["main"]["temp"])

        # print the current temperature in the screen
        self.show.text = str(result["main"]["temp"]) + ' °C'

    # if Urlrequest fail
    def urlfail(self, req, error):
        print("Urlrequest don't working correctly", error)

class TempApp(App):
    def build(self):
        return TempGrid()

if __name__ == "__main__":
    TempApp().run()