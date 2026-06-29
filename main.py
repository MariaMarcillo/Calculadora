from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation

# ==========================================
# 1. LÓGICA DE LAS OPERACIONES MATEMÁTICAS
# ==========================================
class OperacionSumar:
    @staticmethod
    def ejecutar(a, b):
        return a + b

class OperacionRestar:
    @staticmethod
    def ejecutar(a, b):
        return a - b

class OperacionMultiplicar:
    @staticmethod
    def ejecutar(a, b):
        return a * b

class OperacionDividir:
    @staticmethod
    def ejecutar(a, b):
        if b == 0:
            return "Error"
        return a / b


# ==========================================
# 2. CONTROLADOR DE LA CALCULADORA
# ==========================================
class ControladorCalculadora:
    def __init__(self):
        self.num1 = ""
        self.op = None
        self.nuevo_numero = False

    def presionar_digito(self, texto_actual, digito):
        if texto_actual == "0" or self.nuevo_numero or texto_actual == "Error":
            self.nuevo_numero = False
            return digito
        else:
            return texto_actual + digito

    def presionar_operacion(self, texto_actual, operacion):
        self.num1 = texto_actual
        self.op = operacion
        self.nuevo_numero = True
        return texto_actual

    def presionar_c(self):
        self.num1 = ""
        self.op = None
        self.nuevo_numero = False
        return "0"

    def presionar_igual(self, texto_actual):
        if self.op is None or self.num1 == "":
            return texto_actual

        try:
            val1 = float(self.num1)
            val2 = float(texto_actual)
            resultado = 0

            if self.op == '+':
                resultado = OperacionSumar.ejecutar(val1, val2)
            elif self.op == '-':
                resultado = OperacionRestar.ejecutar(val1, val2)
            elif self.op == '*':
                resultado = OperacionMultiplicar.ejecutar(val1, val2)
            elif self.op == '/':
                resultado = OperacionDividir.ejecutar(val1, val2)

            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            self.op = None
            self.num1 = ""
            self.nuevo_numero = True
            return str(resultado)
            
        except Exception:
            self.op = None
            self.num1 = ""
            self.nuevo_numero = True
            return "Error"


# ==========================================
# 3. INTERFAZ GRÁFICA CON ESTILO PREMIUM
# ==========================================
class PantallaInicio(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Fondo premium oscuro moderno
        with self.canvas.before:
            Color(0.07, 0.07, 0.08, 1) 
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.actualizar_fondo, size=self.actualizar_fondo)
        
        self.logo = Label(
            text="Calculadora\ndel Yavirac",
            font_size=32,  
            font_name="Roboto", # Asegura compatibilidad sin archivos externos
            color=(0.95, 0.45, 0.55, 1), 
            bold=True,
            halign='center',
            line_height=1.3
        )
        self.add_widget(self.logo)
        self.on_enter = self.iniciar_animacion

    def actualizar_fondo(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def iniciar_animacion(self):
        # Transición fluida corregida para Android
        anim = Animation(font_size=38, duration=0.8) + Animation(font_size=32, duration=0.8)
        anim.bind(on_complete=self.cambiar_a_calculadora)
        anim.start(self.logo)

    def cambiar_a_calculadora(self, *args):
        self.manager.current = 'calculadora'


class BotonLindo(Button):
    def __init__(self, texto, color_fondo, color_texto=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.text = texto
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0) 
        self.font_size = 26 
        self.font_name = "Roboto" 
        self.bold = True
        self.color = color_texto
        
        self.color_base = color_fondo
        
        with self.canvas.before:
            self.color_canvas = Color(*self.color_base)
            # Botones circulares estilo moderno de celular (iOS/Android Premium)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[30])
            
        self.bind(pos=self.actualizar_geometria, size=self.actualizar_geometria)

    def actualizar_geometria(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_state(self, instance, value):
        if value == 'down':
            self.color_canvas.rgba = (self.color_base[0]*0.7, self.color_base[1]*0.7, self.color_base[2]*0.7, 1)
        else:
            self.color_canvas.rgba = self.color_base


class Calculadora(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 16
        self.spacing = 12
        
        self.controlador = ControladorCalculadora()
        
        with self.canvas.before:
            Color(0.07, 0.07, 0.08, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.actualizar_fondo, size=self.actualizar_fondo)

        # Pantalla flotante sin bordes visibles
        self.pantalla = TextInput(
            text='0',
            font_size=54, 
            font_name="Roboto", 
            halign='right',
            readonly=True,
            size_hint_y=0.28, 
            background_color=(0.07, 0.07, 0.08, 1), 
            foreground_color=(1, 1, 1, 1), 
            multiline=False,
            padding=[10, 40, 10, 10]
        )
        self.add_widget(self.pantalla)

        rejilla = GridLayout(cols=4, spacing=12)
        
        color_num = (0.21, 0.21, 0.23, 1)
        color_op = (0.85, 0.35, 0.45, 1)
        color_c = (0.65, 0.65, 0.68, 1)
        texto_oscuro = (0.07, 0.07, 0.08, 1)
        texto_blanco = (1, 1, 1, 1)

        botones = [
            ('7', color_num, 'num', '7', texto_blanco),
            ('8', color_num, 'num', '8', texto_blanco),
            ('9', color_num, 'num', '9', texto_blanco),
            ('+', color_op, 'op', '+', texto_blanco),
            
            ('4', color_num, 'num', '4', texto_blanco),
            ('5', color_num, 'num', '5', texto_blanco),
            ('6', color_num, 'num', '6', texto_blanco),
            ('-', color_op, 'op', '-', texto_blanco),
            
            ('1', color_num, 'num', '1', texto_blanco),
            ('2', color_num, 'num', '2', texto_blanco),
            ('3', color_num, 'num', '3', texto_blanco),
            ('x', color_op, 'op', '*', texto_blanco),
            
            ('C', color_c, 'c', 'C', texto_oscuro),
            ('0', color_num, 'num', '0', texto_blanco),
            ('=', color_op, 'igual', '=', texto_blanco),
            ('/', color_op, 'op', '/', texto_blanco)
        ]

        for texto, color, tipo, valor_logico, col_txt in botones:
            btn = BotonLindo(texto=texto, color_fondo=color, color_texto=col_txt)
            
            if tipo == 'num':
                btn.bind(on_press=lambda instance, v=valor_logico: self.pantalla_num(v))
            elif tipo == 'op':
                btn.bind(on_press=lambda instance, v=valor_logico: self.pantalla_op(v))
            elif tipo == 'c':
                btn.bind(on_press=lambda instance: self.pantalla_c())
            elif tipo == 'igual':
                btn.bind(on_press=lambda instance: self.pantalla_igual())
                
            rejilla.add_widget(btn)

        self.add_widget(rejilla)

    def actualizar_fondo(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def pantalla_num(self, digito):
        self.pantalla.text = self.controlador.presionar_digito(self.pantalla.text, digito)

    def pantalla_op(self, operacion):
        self.pantalla.text = self.controlador.presionar_operacion(self.pantalla.text, operacion)

    def pantalla_c(self):
        self.pantalla.text = self.controlador.presionar_c()

    def pantalla_igual(self):
        self.pantalla.text = self.controlador.presionar_igual(self.pantalla.text)


class PantallaCalculadora(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Calculadora())


class MainApp(App):
    def build(self):
        self.title = "Calculadora del Yavirac"
        sm = ScreenManager()
        sm.add_widget(PantallaInicio(name='inicio'))
        sm.add_widget(PantallaCalculadora(name='calculadora'))
        return sm

if __name__ == '__main__':
    MainApp().run()
