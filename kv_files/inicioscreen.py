from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

text = '''
Lorem ipsum dolor sit amet, \n consectetur adipiscing elit.\n 
Nullam euismod, nisl eget \n aliquam ultricies,\\
quam odio aliquet nunc, \n eget aliquam diam diam eget nisl.'''




class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
        
    def _finish_init(self, dt):
        pass
    
    def on_enter(self, *args):
        super().on_enter(*args)
        self.add_widget(BoxInicio())

class BoxInicio(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.ids)
