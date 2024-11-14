# Etapa 2

En este directorio está la implementación de la etapa 2 en un sistema embebidos, particularmente el RP2040.

## Archivos

* [ssd1306](ssd1306.py): tiene una biblioteca para poder hacer uso del display OLED para la interfaz.
* [interfaceDisplay](interfaceDisplay.py): implementación de una clase que se encarga de manejar la interfaz de afinador en el display.
* [tuner](tuner.py): implementación de una clase que se encarga de resolver el sampleo y procesamiento de la señal de audio. Implementado con FFT.
* [tuner_goertzel](tuner_goertzel.py): implementacion de una clase como la anterior pero que usa el algoritmo de Goertzel.
* [app](app.py): programa principal que corre en el microcontrolador.

## Hardware usado

* [RP2040-Zero](https://www.waveshare.com/wiki/RP2040-Zero)
* [Electret + MAX9814](https://www.adafruit.com/product/1713)
* [OLED 128x64](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)

## Conexiones

<div align="center">

| RP2040-Zero | Función | Componente | Pin |
| --- | --- | --- | --- |
| GPIO0 | I2C0 | SSD1306 | SDA |
| GPIO1 | I2C0 | SSD1306 | SCL |
| GPIO28 | ADC | MAX9814 | Out |

</div>

## Requisitos adicionales

El RP2040-Zero debe contar con un firmware especial de Micropython con el paquete [ulab](https://github.com/v923z/micropython-ulab).

También, debe tener la biblioteca para el OLED con el driver SSD1306 desarrollado en este [repositorio](https://github.com/makerportal/rpi-pico-ssd1306). El archivo se encuentra en este directorio también.