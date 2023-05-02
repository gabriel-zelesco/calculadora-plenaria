from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock


from utils.functions import load_data, save_data


from kivy.uix.label import Label


class CalculadoraScreen(Screen):
    box_nplaces = ObjectProperty()
    box_abstention = ObjectProperty()
    
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


### Boxes Nplaces
class BoxNplaces(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
   
    def add_n_places(self, n_places):
        self.election_data = load_data()
        self.election_data['n_seats'] = n_places
        self.remove_widget(self.ids.input_nplaces)
        box_cadeiras = BoxCadeiras(self.election_data['n_seats'])
        self.add_widget(box_cadeiras)
        self.ids['box_cadeiras'] = box_cadeiras
        save_data(self.election_data)
        
    def edit_n_places(self):
        self.remove_widget(self.ids.box_cadeiras)
        input_nplaces = BoxInputCadeiras()
        self.add_widget(input_nplaces)
        self.ids['input_nplaces'] = input_nplaces
   
        
class BoxCadeiras(BoxLayout):
    def __init__(self, n_places, **kwargs):
        super().__init__(**kwargs)
        self.ids.n_places.text = n_places

class BoxInputCadeiras(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = 'input_nplaces'

### Boxes Abstentions
class BoxAbstentions(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
   
    def add_abstentions(self, abstentions):
        self.election_data = load_data()
        self.election_data['abstention'] = abstentions
        self.remove_widget(self.ids.input_abstentions)
        box_abstencao = BoxOutputAbstencao(self.election_data['abstention'])
        self.add_widget(box_abstencao)
        self.ids['box_abstencao'] = box_abstencao
        save_data(self.election_data)
        
    def edit_abstentions(self):
        self.remove_widget(self.ids.box_abstencao)
        input_abstentions = BoxInputAbstencao()
        self.add_widget(input_abstentions)
        self.ids['input_abstentions'] = input_abstentions
   
        
class BoxOutputAbstencao(BoxLayout):
    def __init__(self, abstentions, **kwargs):
        super().__init__(**kwargs)
        self.ids.abstentions.text = abstentions

class BoxInputAbstencao(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = 'input_abstentions' 