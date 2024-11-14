from machine import Pin, ADC, Timer
from ulab import numpy as np

class Tuner():

    # Notas de la guitarra
    NOTES = {
        "e": 329.63,
        "B": 246.94,
        "G": 196.00,
        "D": 146.83,
        "A": 110.00,
        "E": 82.41
    }

    # Rango del afinador para cada nota
    NOTES_RANGE = {
       "e": [-41.3, 41.3],
       "B": [-25, 41.5],
       "G": [-25, 25],
       "D": [-18, 25],
       "A": [-14, 18],
       "E": [-14, 14]
    }

    def __init__(self, fs=1000, n=512, adc_pin=28):
        """Inicializa el tuner

        Parameters
        ----------
        fs : int
            Frecuencia de muestreo
        n : int
            Cantidad de muestras
        adc_pin : int
            GPIO a usar de entrada analogica
        """
        # Inicializo propiedades de la clase
        self._fs = fs
        self._n = n
        self._mic = ADC(Pin(adc_pin))

        # Array vacio para las muestras
        self._samples = []
        # Array con los valores de frecuencia que se van a usar
        self._freqs = np.linspace(0, self._fs/2, int(self._n / 2))
        # Booleano para indicar que se termino de muestrear
        self._sampling_done = False
        # Inicializo un Timer
        self._timer = Timer()

    def _sampling_cb(self, t):
        """Callback del Timer
        
        Parameters
        ----------
        t : Timer
            Timer que esta corriendo
        """
        # Tomo la muestra de tension
        self._samples.append(self._mic.read_u16())
        # Verifico el largo de la lista
        if len(self._samples) >= self._n:
            # Detengo el Timer
            t.deinit()
            # Aviso al programa principal
            self._sampling_done = True

    def sampling_done(self):
        """Informa si se termino el sampling o no

        Returns
        -------
        boolean
            True si termino el sampleo
        """
        return self._sampling_done
    
    def sampling_start(self):
        """Inicia el sampleo de audio
        """
        self._sampling_done = False
        self._samples = []
        self._timer.init(mode=Timer.PERIODIC, freq=self._fs, callback=self._sampling_cb)

    def get_fundamental(self):
        """Obtiene la frecuencia fundamental de la muestra de audio

        Returns
        -------
        float
            Frecuencia fundamental en Hz
        """
        # Hago la FFT con la cantidad de muestras solicidatas
        fft_real, fft_img = np.fft.fft(np.array(self._samples[:self._n:]))
        # Paso a lista, me quedo con la mitad util y calculo el valor absoluto
        fft_real = abs(fft_real).tolist()[:256:]
        # Limpio el valor de continua
        fft_real[0] = 0
        # Encuentro el maximo (fundamental)
        max_amp = max(fft_real)
        # Consigo el indice de la fundamental
        max_index = fft_real.index(max_amp)
        # Devuelvo el valor
        return self._freqs[max_index]
    
    def find_closest_note(self, fundamental):
        """Encuentra la nota de la guitarra mas cercana a la frecuencia indicada

        Parameters
        ----------
        fundamental : float
            Frecuencia fundamental medida

        Returns
        -------
        float
            Frecuencia mas cercana
        """
        # Encuentra la nota cuya frecuencia es la más cercana a la medida
        closest_note = min(Tuner.NOTES, key=lambda note: abs(Tuner.NOTES[note] - fundamental))
        return closest_note

    def get_range(self, note):
        """Obtiene el rango de frecuencias para la interfaz en una frecuencia de guitarra

        Parameters
        ----------
        note : str
            Nota de guitarra buscada
        """
        return Tuner.NOTES_RANGE[note]