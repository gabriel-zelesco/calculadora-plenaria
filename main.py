from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Electoral Calculator'))
        self.add_widget(PartyGrid())
        
        
class PartyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(PartyGrid, self).__init__(**kwargs)
        self.cols = 4
        self.row = InputParty()
        self.add_widget(Label(text='Party Name'))
        self.add_widget(Label(text='Party Name'))
        self.add_widget(Label(text='Party Name'))

    
class InputParty(Widget):
    def __init__(self, **kwargs):
        super(InputParty, self).__init__(**kwargs)
        self.add_widget(Label(text='Party Name'))



class ElectoralCalculatorApp(App):
    def build(self):
        return PartyGrid()

if __name__ == '__main__':
    ElectoralCalculatorApp().run()
