import json

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

# Funtions
def load_data():
    try:
        with open('data.json', 'r') as data:
            election_data = json.load(data)
    except:
        election_data = {}
    return election_data

# Classes
class Gerenciador(ScreenManager):
    pass

class AvisoPop(Popup):
    pass
   
class NovaChapa(Popup):
    election_data = load_data()
    
    def on_pre_open(self):
        load_data()

    def save_data(self):
        with open('data.json', 'w') as data:
            json.dump(self.election_data, data)
                    
    def adicionar_chapa(self):
        nome_chapa = self.ids.nome_chapa.text
        valor_chapa = self.ids.valor_chapa.text
        self.election_data[nome_chapa] = valor_chapa
        self.ids.nome_chapa.text = ''
        self.ids.valor_chapa.text = ''
        AvisoPop().open()
        self.save_data()
    '''
    def aviso_pop(self):
        box = BoxLayout(orientation='vertical')
        pop = Popup(title='Aviso',
                      content=Label(text='Chapa adicionada com sucesso!'),
                      size_hint=(None, None),
                      size=(250, 200))
        aviso.open()
    '''

class Inicio(Screen):
    def on_pre_open(self):
        self.load_data()
            

class CalculadoraApp(App):
    def build(self):
        return Gerenciador()
    
    
if __name__ == "__main__":
    CalculadoraApp().run()