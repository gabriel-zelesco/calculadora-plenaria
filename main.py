from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder



# Loads widgets classes
from kv_files.inicioscreen import InicioScreen
from kv_files.calculadorascreen import CalculadoraScreen
from kv_files.resultadoscreen import ResultadoScreen
from kv_files.opcoesscreen import OpcoesScreen


# Loads multiple .kv files
Builder.load_file(filename='kv_files/inicioscreen.kv')
Builder.load_file(filename='kv_files/calculadorascreen.kv')
Builder.load_file(filename='kv_files/resultadoscreen.kv')
Builder.load_file(filename='kv_files/opcoesscreen.kv')
Builder.load_file(filename='kv_files/style.kv')


class Manager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return Manager()
    
if __name__ == '__main__':
    MainApp().run()