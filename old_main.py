import json

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

from utils.dhontmethod import DhontMethod

# Funtions
def check_data(json_data):
    if 'abstention' not in json_data:
        json_data['abstention'] = "0"
    return json_data

def check_n_places(json_n_places):
    if 'n_places' not in json_n_places:
        json_n_places['n_places'] = "1"
        return json_n_places
    elif json_n_places['n_places'] == "0":
        json_n_places['n_places'] = "1"
    return json_n_places

def load_data(file_path='data.json'):
    try:
        with open(file_path, 'r') as data:
            election_data = json.load(data)
    except:
        election_data = {}        
        
    election_data = check_data(election_data)   
    return election_data

def save_data(data_dic, file_path='data.json'):        
    with open(file_path, 'w') as data:
        json.dump(data_dic, data)
        

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
        
    def _finish_init(self, dt):
        pass
    
    def on_enter(self, *args):
        self.ids.box_chapas.clear_widgets()
        self.election_data = load_data()
        self.build_quadro_chapas()
        
    
    def build_quadro_chapas(self):
        for i in self.election_data:
            self.ids.box_chapas.add_widget(ChapaInscrita(i, self.election_data[i]))

    def add_chapa(self, nome, votos):
        self.nome_chapa = nome
        self.votos_chapa = votos
        self.election_data[self.nome_chapa] = self.votos_chapa
        save_data(self.election_data)
        
    def reset_quadro(self):
        self.election_data = load_data()
        self.ids.box_nplaces.clear_widgets()
        

class OpcoesScreen(Screen):
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
        self.election_data.pop(key)
        save_data(self.election_data)
            

class BoxNplaces(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_n_places(self, n_places):
        self.n_places = n_places
        self.remove_widget(self.ids.input_nplaces)
        box_cadeiras = BoxCadeiras(self.n_places)
        self.add_widget(box_cadeiras)
        self.ids['box_cadeiras'] = box_cadeiras
        save_data({'n_places': self.n_places}, 'n_places.json')
        
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
        

class BoxNovaChapa(BoxLayout):
    pass


class ResultadoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        self.n_places = self._get_n_places()
        #Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        pass
    
    def _get_n_places(self):
        self.n_places = load_data('n_places.json')
        self.n_places = check_n_places(self.n_places)
        return self.n_places
    
    def on_enter(self, *args):
        self.ids.box_resultados.clear_widgets()
        self.ids.box_resultados.add_widget(BoxResultadoSimples())
        self.ids.box_resultados.add_widget(BoxResultadoCompleto())


class BoxResultadoSimples(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        self.n_places = self._get_n_places()
        self.poll = DhontMethod(self.election_data, self.n_places, largest_remainder=True)
        self.results = self.poll.results
        
        for i in self.results:
            self.add_widget(Label(text=i))
            self.add_widget(Label(text=str(self.results[i])))
            
    def _get_n_places(self):
        self.n_places = load_data('n_places.json')
        self.n_places = check_n_places(self.n_places)
        return self.n_places
        

class BoxResultadoCompleto(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        self.n_places = self._get_n_places()
        self.poll = DhontMethod(self.election_data, self.n_places, largest_remainder=True)
        self.report = self.poll.report
        self.tie = self.poll.tie
        self.limit_check = self.poll.limit_check
        self.order = self.poll.order
        self.cumulative_order = self.poll.cumulative_order
        
        for call in self.report:
            self.add_widget(Label(text=f'Round: {call}'))
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            
            for party in self.report[call][self.order[call-1]]:
                self.add_widget(Label(text=f'{party}[{self.cumulative_order[call][party]}]:'))
                self.add_widget(Label(text=f'{self.report[call][self.order[call-1]][party]:.2f}'))
                self.add_widget(Label(text=f'{self.tie[call][party]} '))
                self.add_widget(Label(text=f'{self.limit_check[call][party]}'))
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            
    def _get_n_places(self):
        self.n_places = load_data('n_places.json')
        self.n_places = check_n_places(self.n_places)
        return self.n_places
                
                
class CalculatorApp(App):
    def build(self):
        return Manager()
    
if __name__ == '__main__':
    CalculatorApp().run()
    