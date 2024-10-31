from tuner import Tuner
from time import sleep

tuner = Tuner(n=1024)

tuner.sampling_start()

while True:

    if(tuner.sampling_done()):

        note = tuner.get_fundamental()
        print("Nota fundamental: ", end="")
        print(note)
        print()

        print("La nota mas cercana es ", end="")
        print(tuner.find_closest_note(note))
        print("Con frecuencia ", end="")
        print(Tuner.NOTES[tuner.find_closest_note(note)])
        print()
        print()
        sleep(.25)
        tuner.sampling_start()
