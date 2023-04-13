import json

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# Funtions
def load_data():
    try:
        with open('data.json', 'r') as data:
            election_data = json.load(data)
    except:
        election_data = {}
    return election_data

def finish_init():
    pass

# Classes
class Manager(ScreenManager):
    pass

class InicioScreen(Screen):
    pass

class CalculadoraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        Clock.schedule_once(self._finish_init)
        self.mostra_quadro_chapas()
        
    def _finish_init(self, dt):
        print(self.ids)
        
    def mostra_quadro_chapas(self):
        for i in self.election_data:
            self.ids.box_chapas.add_widget(ChapaInscrita(i, self.election_data[i]))

class ResultadoScreen(Screen):
    pass

class OpcoesScreen(Screen):
    pass
        
class ChapaInscrita(BoxLayout):
    def __init__(self, nome, votos, **kwargs):
        super().__init__(**kwargs)
        print(self.ids)
        self.ids.nome_chapa.text = nome
        self.ids.votos_chapa.text = votos

class BoxNovaChapa(BoxLayout):
    pass

class CalculatorApp(App):
    def build(self):
        return Manager()
    
if __name__ == '__main__':
    CalculatorApp().run()