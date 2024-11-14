from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# All below code to be moved to interfaceDisplay.py class
class InterfaceDisplay():

    def __init__(self, min_value=-100, max_value=100):
        """Inicializa lo necesario para la interfaz

        Parameters
        ----------
        min_value : int
            Valor minimo de frecuencia
        max_value : int
            Valor maximo de frecuencia
        """
        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=600000)
        self.oled = SSD1306_I2C(128, 64, self.i2c)
        self.min_value = min_value
        self.max_value = max_value

    def draw_tuner_skeleton(self, show=True):
        """Dibuja la interfaz basica del tuner

        Parameters
        ----------
        show : boolean
            Decide si solo queda en memoria o si dibuja
        
        """
        self.oled.fill(0)
        self.oled.text('Afinador', 33, 0)
        self.oled.hline(10, 30, 108, 1)
        self.oled.vline(64, 20, 20, 1)
        self.oled.text('-', 4, 40)
        self.oled.text('OK', 60, 40)
        self.oled.text('+', 120, 40)
        if show:
            self.oled.show()


    def render_tuning_indicator(self, value, text):
        """Muestra en indicador de afinacion

        Parameters
        ----------
        value : float
            Frecuencia a mostrar
        text : str
            Texto a mostrar (nota)
        """
        self.draw_tuner_skeleton(False)
        # Ensure value is within the range
        value = max(self.min_value, min(self.max_value, value))
        # Ajusto de acuerdo al rango
        if value < 0:
            value = -100 * value / self.min_value
        else:
            value = 100 * value / self.max_value

        # Map the value to the display range
        x_pos = 64 + int(value * 0.54)  # 0.54 is a scaling factor for 100 to 54 pixels
        self.oled.vline(x_pos, 20, 20, 1)  # Draw the needle

        # Mini lineas para el indicador parte de abajo
        self.oled.vline(x_pos - 1, 40, 5, 1)
        self.oled.vline(x_pos, 40, 5, 1)
        self.oled.vline(x_pos + 1, 40, 5, 1)

        # Mini lineas para el indicador parte de arriba
        self.oled.vline(x_pos - 1, 15, 5, 1)
        self.oled.vline(x_pos, 15, 5, 1)
        self.oled.vline(x_pos + 1, 15, 5, 1)

        # Imprimir text centrado horizontalmente a altura 50
        self.oled.text(text, 40, 50, 1)
        self.oled.show()


    def set_range(self, min_value, max_value):
        """Cambia el rango de trabajo del tuner

        Parameters
        ----------
        min_value : int
            Minimo valor de frecuencia
        max_value : int
            Maximo valor de frecuencia
        """
        self.min_value = min_value
        self.max_value = max_value