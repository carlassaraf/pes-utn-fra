from interfaceDisplay import InterfaceDisplay
from tuner import Tuner
from time import sleep

tuner = Tuner(n=1024)
display = InterfaceDisplay(min_value=-150, max_value=150)

tuner.sampling_start()
display.draw_tuner_skeleton()

while True:

    if(tuner.sampling_done()):

        note = tuner.get_fundamental()
        print("Nota fundamental: ", end="")
        print(note)
        print()

        closest_note = tuner.find_closest_note(note)
        print("La nota mas cercana es ", end="")
        print(closest_note)
        print("Con frecuencia ", end="")
        print(Tuner.NOTES[closest_note])
        diffFrec = Tuner.NOTES[closest_note] - note

        display.render_tuning_indicator(diffFrec, closest_note)
        print()
        print()
        sleep(.25)
        tuner.sampling_start()
