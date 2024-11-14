from time import sleep

from machine import Pin, ADC, Timer
from ulab import numpy as np

class Goertzel():

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

    # Implementación de Goertzel para una frecuencia específica
    def goertzel(self, samples, target_freq, sample_rate):
        N = len(samples)
        k = int(0.5 + (N * target_freq) / sample_rate)  # Índice de la frecuencia objetivo
        omega = (2.0 * np.pi * k) / N
        coeff = 2.0 * np.cos(omega)

        s_prev = 0.0
        s_prev2 = 0.0

        # Algoritmo de recurrencia de Goertzel
        for sample in samples:
            s = sample + coeff * s_prev - s_prev2
            s_prev2 = s_prev
            s_prev = s

        # Calcular magnitud de la frecuencia objetivo
        power = s_prev2 ** 2 + s_prev ** 2 - coeff * s_prev * s_prev2
        return power

    # Detectar la frecuencia dominante en un rango cercano a la frecuencia objetivo
    def detect_frequency(self, data, sample_rate, target_freq, freq_range=60):
        max_power = 0
        detected_freq = target_freq
        print("target_freq: ", end="")
        print(target_freq)


        # Probar frecuencias en el rango [target_freq - freq_range, target_freq + freq_range]
        for f in np.arange(target_freq - freq_range, target_freq + freq_range, 0.1):
            power = self.goertzel(data, f, sample_rate)
            if power > max_power:
                max_power = power
                detected_freq = f

        return detected_freq

    def get_fundamental(self):
        """Obtiene la frecuencia fundamental de la muestra de audio

        Returns
        -------
        float
            Frecuencia fundamental en Hz
        """
        # Aplico Goertzel a todas las NOTAS
        difs = [self.detect_frequency(self._samples, self._fs, freq) for freq in Goertzel.NOTES.values()]
        print("difs: ", end="")
        print(difs)
        # Encuentro la nota mas cercana
        notes_list = list(Goertzel.NOTES.keys())
        closest_note = min(Goertzel.NOTES, key=lambda note: abs(Goertzel.NOTES[note] - difs[notes_list.index(note)]))
        return difs[notes_list.index(closest_note)]

    
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
        closest_note = min(Goertzel.NOTES, key=lambda note: abs(Goertzel.NOTES[note] - fundamental))
        return closest_note

    def get_range(self, note):
        """Obtiene el rango de frecuencias para la interfaz en una frecuencia de guitarra

        Parameters
        ----------
        note : str
            Nota de guitarra buscada
        """
        return Goertzel.NOTES_RANGE[note]