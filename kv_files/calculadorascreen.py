from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

from utils.functions import load_data, save_data
from utils.pollsresult import PollsResult


class CalculadoraScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        Clock.schedule_once(self._finish_init)
    
    def _finish_init(self, dt):
        pass
    
    def on_enter(self, *args, **kwargs):
        self.election_data = load_data()
        self.ids.box_chapas.clear_widgets()
        self.build_box_chapas()

               
    def build_box_chapas(self):
        for key in self.election_data['votes']:
            value = self.election_data['votes'][key]
            self.ids.box_chapas.add_widget(ChapaInscrita(key, value))
        self.ids.box_chapas.add_widget(BoxTotalizacao())
    
    def add_chapa(self, nome, votos):
        self.nome_chapa = nome
        self.votos_chapa = votos
        self.election_data['votes'][self.nome_chapa] = self.votos_chapa
        save_data(self.election_data)
        
    def add_abstention(self, abstention):
        self.abstention = abstention
        self.election_data['abstention'] = self.abstention
        save_data(self.election_data)
        
    def add_nplaces(self, nplaces):
        self.nplaces = nplaces
        self.election_data['nplaces'] = self.nplaces
        save_data(self.election_data)
        
    def error(self, error):
        popup = PopupError()
        popup.open()

class PopupError(Popup):
    pass
    
    
class ChapaInscrita(BoxLayout):
    def __init__(self, nome, votos, **kwargs):
        super().__init__(**kwargs)
        self.ids.nome_chapa.text = nome
        self.ids.votos_chapa.text = votos
        
    def remove_chapa(self):
        self.election_data = load_data()
        self.parent.remove_widget(self)
        key = self.ids.nome_chapa.text
        self.election_data['votes'].pop(key)
        save_data(self.election_data)

class BoxTotalizacao(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        self.poll = PollsResult()
        self.valid = self.poll.used_votes
        self.ids.total.text = str(self.valid)
        

### Boxes Nplaces
class BoxNplaces(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_enter()
    
    def on_enter(self):
        self.election_data = load_data()
        self.build_box_cadeiras()
    
    def build_box_cadeiras(self):
        try:
            self.ids.box_cadeiras.clear_widgets()
        except:
            pass
        box_cadeiras = BoxCadeiras(self.election_data['n_seats'])
        self.add_widget(box_cadeiras)
        self.ids['box_cadeiras'] = box_cadeiras
        
    def edit_nplaces(self):        
        self.remove_widget(self.ids.box_cadeiras)
        input_nplaces = BoxInputCadeiras()
        self.add_widget(input_nplaces)
        self.ids['input_cadeiras'] = input_nplaces
        
    def add_nplaces(self, nplaces):
        self.election_data = load_data()
        self.election_data['n_seats'] = nplaces
        save_data(self.election_data)
        self.remove_widget(self.ids.input_cadeiras)
        self.on_enter()
   
   
class BoxCadeiras(BoxLayout):
    def __init__(self, n_places, **kwargs):
        super().__init__(**kwargs)
        self.ids.n_places.text = n_places
        self.id = 'box_cadeiras'

class BoxInputCadeiras(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = 'input_nplaces'
        

### Boxes Abstentions
class BoxAbstentions(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_enter()
    
    def on_enter(self):
        self.election_data = load_data()
        self.build_box_abstencoes()
    
    def build_box_abstencoes(self):
        try:
            self.ids.box_abstencoes.clear_widgets()
        except:
            pass
        box_abstencoes = BoxAbstencao(self.election_data['abstention'])
        self.add_widget(box_abstencoes)
        self.ids['box_abstencoes'] = box_abstencoes
        
    def edit_abstentions(self):        
        self.remove_widget(self.ids.box_abstencoes)
        input_abstentions = BoxInputAbstencoes()
        self.add_widget(input_abstentions)
        self.ids['input_abstentions'] = input_abstentions
        
    def add_abstentions(self, abstencoes):
        self.election_data = load_data()
        self.election_data['abstention'] = abstencoes
        save_data(self.election_data)
        self.remove_widget(self.ids.input_abstentions)
        self.on_enter()
   
   
class BoxAbstencao(BoxLayout):
    def __init__(self, abstentions, **kwargs):
        super().__init__(**kwargs)
        self.ids.abstencoes.text = abstentions
        self.id = 'box_abstencoes'

class BoxInputAbstencoes(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = 'input_abstentions'