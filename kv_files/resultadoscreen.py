from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from utils.functions import load_data
from utils.dhontmethod import DhontMethod
from utils.largestremainder import LargestRemainder

class ResultadoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_enter(self, *args, **kwargs):
        self.ids.box_resultados.clear_widgets()
        self.ids.box_resultados.add_widget(BoxSumario())
        self.ids.box_resultados.add_widget(BoxResultado())
        #self.ids.box_resultados.add_widget(BtnRelatorio())        
        self.ids.box_resultados.add_widget(BoxReport())
        
    def show_report(self):
        self.ids.box_resultados.add_widget(BoxReport())
        print('teste')
    
        
class BoxSumario(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.election_data = load_data()
        self.poll = LargestRemainder()
        
        self.add_widget(Label(text='Participantes'))
        self.add_widget(Label(text=str(len(self.poll.parties))))
        self.add_widget(Label(text='Abstenções'))
        self.add_widget(Label(text=str(self.poll.abstention)))
        self.add_widget(Label(text='Abstenção como válido'))
        self.add_widget(Label(text=str(self.poll.abstention_as_valid)))
        self.add_widget(Label(text='Votos válidos'))
        self.add_widget(Label(text=str(self.poll.used_votes)))
        self.add_widget(Label(text='Cadeiras'))
        self.add_widget(Label(text=str(self.poll.n_seats)))
    

class BoxResultado(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        self.poll = LargestRemainder()
                
        for party in self.poll.parties:
            self.add_widget(Label(text=party))
            self.add_widget(Label(text=str(self.poll.votes[party])))
            self.add_widget(Label(text=str(self.poll.first_distribution[party])))
            self.add_widget(Label(text=str(self.poll.remaining_distribution[party])))
            self.add_widget(Label(text=str(self.poll.result[party])))
            
class BoxReport(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        self.dhont = DhontMethod()
                
        for round in self.dhont.rounds:
            winner = self.dhont.round_report[round]['winner']
            self.add_widget(RoundWinner(round, winner))
            self.add_widget(RoundReport(round))
                    

class RoundWinner(BoxLayout):
    def __init__(self, round, winner, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text=f'Round: {round}'))
        self.add_widget(Label(text=f'{winner}'))

class RoundReport(GridLayout):
    def __init__(self,round, **kwargs):
        super().__init__(**kwargs)
        self.election_data = load_data()
        self.dhont = DhontMethod()
        
        for party in self.dhont.parties:
            self.add_widget(Label(text=party))
            self.add_widget(Label(text=str(self.dhont.round_report[round]['votes'][party])))
            self.add_widget(Label(text=str(self.dhont.round_report[round]['seats'][party])))
            self.add_widget(Label(text=str(self.dhont.round_report[round]['tie'][party])))
            self.add_widget(Label(text=str(self.dhont.round_report[round]['limit'][party])))

        
        
        
        
             
       