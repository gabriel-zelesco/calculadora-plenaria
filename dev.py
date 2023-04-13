import json

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import NoTransition
from kivy.uix.actionbar import ActionBar
from kivy.core.window import Window
from kivy.clock import Clock

from utils.dhontmethod import DhontMethod


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

class Entrada(Screen):
    pass

class NavBar(ActionBar):
    pass

class AvisoPop(Popup):
    pass

class QuadroChapas(BoxLayout):
    pass
   
class NovaChapa(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()   

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


class Inicio(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
    
    def on_pre_enter(self, *args):
        self.atualiza_quadro()
        
           
    def atualiza_quadro(self):
        self.election_data = load_data()
        self.ids.quadro_chapas.clear_widgets()
        for chapa in self.election_data:
            self.ids.quadro_chapas.add_widget(
                QuadroChapas(text_chapa=chapa,
                             text_votos=self.election_data[chapa]))
            
    def on_pre_leave(self, *args):
        self.ids.quadro_chapas.clear_widgets()




class QuadroChapas(BoxLayout):
    def __init__(self, text_chapa='', text_votos='', **kwargs):
        super().__init__(**kwargs)
        self.ids.label_chapa.text = text_chapa
        self.ids.label_votos.text = text_votos



class Resultados(Screen):
    pass



class QuadroResultado(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        self.n_seats = 10
        self.poll= DhontMethod(self.election_data, self.n_seats)
        self.result = self.poll.results
        
        
        #self.text = ''
        #for call in self.poll.report:
        #    self.ids.quadro_resultado.add_widget(ResultadoRodada(text=f'Round {call}: {self.poll.order[call-1]}'))
            
        '''
        self.text = ''
        for call in self.poll.report:
            self.text += f'Round {call}: {self.poll.order[call-1]} \n'
            for party in self.poll.report[call][self.poll.order[call-1]]:
                self.text += f"""\n
                \t{party}[{self.poll.cumulative_order[call][party]}]: \
                {self.poll.report[call][self.poll.order[call-1]][party]:.2f} \
                {self.poll.tie[call][party]} \
                {self.poll.limit_check[call][party]}"""
        '''
        #self.add_widget(Label(text=self.text))
        print(self.ids)
        #print (self.poll.report)

class ResultadoRodada(BoxLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        #self.ids.label_call.text = self.text

      
class CalculadoraApp(App):
    def build(self):
        return Gerenciador()
    
    
if __name__ == "__main__":
    CalculadoraApp().run()