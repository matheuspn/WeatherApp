import kivy
from kivymd.app import MDApp
from kivy.config import Config
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen

from urllib.parse import quote

kivy.require('2.0.0') 

# getting the api key
with open("apikey.txt") as f:
    openweatherkey = f.read()

class MainScreen(MDScreen):

    show = ObjectProperty(None)
    image_icon : str 
    image_url : str 
    path = "images/description_img.png"
    countrys = list()

    with open("lists/country.list.txt", 'r' ,encoding='utf-8') as f:
        countrys = f.read().rsplit()

    global openweatherkey

    # get the response from api 
    def search_button(self, country, city):

        url = quote(f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={openweatherkey}",
                    safe= ':,/,=,&,?')
        UrlRequest(url,on_success=self.answer, on_error=self.urlfail, on_failure=self.urlfail)

    # the response of Urlrequest
    def answer(self, req, result):
        
        # print the current temperature in the screen
        self.show.text = str(result["main"]["temp"]) + ' °C'

        # print the min and the max temp in the info screen
        self.manager.ids.info.ids.min_temp.text = str(result["main"]["temp_min"]) + ' °C'
        self.manager.ids.info.ids.max_temp.text = str(result["main"]["temp_max"]) + ' °C'
        
        # get the description 
        self.manager.ids.info.ids.description.text = str(result["weather"][0]["description"])

        # get the code of icon description
        self.image_icon = str(result["weather"][0]["icon"])

        # set the image url
        self.image_url = quote(f"http://openweathermap.org/img/wn/{self.image_icon}@2x.png", safe= ':,/,=,&,?,@')

        self.get_image()

    # if Urlrequest fail
    def urlfail(self, req, error):
        print("Urlrequest don't working correctly", error)

    # get the image of icon description from api 
    def get_image(self):
        UrlRequest(self.image_url,on_success= self.answer_image, on_failure= self.urlfail, file_path=self.path)

    # reload the image of icon description
    def answer_image(self, req, result):
        self.manager.ids.info.ids.desc_image.reload()


class InfoScreen(MDScreen):
    pass


class ScreenManagement(ScreenManager):
    pass

class TempApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return ScreenManagement()

if __name__ == "__main__":
    TempApp().run()