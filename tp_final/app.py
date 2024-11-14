from interfaceDisplay import InterfaceDisplay
from tuner import Tuner
from time import sleep

# Instancia de tuner con frecuencia de sampling de 2KHz y 1024 muestras
tuner = Tuner(fs=2000, n=1024)
# Instancia de display (interfaz del tuner)
display = InterfaceDisplay()

# Arranca sampleo y muestra el dibujo en la interfaz
tuner.sampling_start()
display.draw_tuner_skeleton()

while True:
    # Espera a terminar el sampleo
    if(tuner.sampling_done()):
        # Obtiene la fundamental de la muestra
        note = tuner.get_fundamental()
        print("Nota fundamental: ", end="")
        print(note)
        print()
        # Veo cual es la nota mas cercana
        close_note = tuner.find_closest_note(note)
        print("La nota mas cercana es ", end="")
        print(tuner.find_closest_note(note))
        print("Con frecuencia ", end="")
        print(Tuner.NOTES[close_note])
        # Obtiene el rango del tuner para la nota de la guitarra
        screen_range = tuner.get_range(close_note)
        display.set_range(screen_range[0], screen_range[1])
        # Grafica la aguja segun la diferencia
        diffFrec = Tuner.NOTES[close_note] - note
        display.render_tuning_indicator(diffFrec, close_note)
        print()
        print()
        # Arranca un nuevo sampleo
        tuner.sampling_start()