# Hamming_Python_Arduino
Trabajo para el curso de Comunicacion de Datos en el ciclo 2023-1 en la Universidad de Lima.

Trabajo realizado en conjunto por:
Marcelo Landa
Giancarlo Pinedo
Sebastian Garcia
Alessander Mejia

Este proyecto consiste en la implementación del código Hamming para la detección y corrección de errores en la transmisión de bits, utilizando Python.

Se desarrolló una interfaz gráfica en Python utilizando la biblioteca Tkinter, la cual permite al usuario ingresar 7 bits (0 o 1) para calcular el código Hamming correspondiente. Una vez calculado, el código se muestra en la interfaz gráfica y se transmite a través de Pyserial al Arduino.

El Arduino, a su vez, controla 11 LEDs que se encienden dependiendo de si el bit transmitido fue un 1 o un 0. Posteriormente, este Arduino envía los datos a otro Arduino a través de comunicación I2C, el cual también controla un conjunto de LEDs.

Finalmente, el segundo Arduino transmite el código Hamming recibido de vuelta a Python mediante Pyserial. En caso de detectar errores, Python corrige el código y lo muestra en la interfaz gráfica. Además, se incluye un botón de "refresh" para volver a recibir los datos del Arduino.
