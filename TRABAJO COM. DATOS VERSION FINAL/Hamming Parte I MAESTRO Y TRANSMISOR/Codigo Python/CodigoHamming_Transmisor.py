#PILLOW PERMITE LA MANIPULACION DE IMAGENES e IMAGETK PERMITE MOSTRAR IMAGENES EN GRAFICAS UTILIZANDO TKINTER
import tkinter as tk
from PIL import ImageTk, Image
import time
import serial

#FUNCION XOR PARA EL CALCULO DE PARIDADES
def XOR(a, b):
    if a == 1 and b == 1:
        return 0
    elif a == 0 and b == 0:
        return 0
    else:
        return 1

#CALCULO DE LA 1ERA PARIDAD
def primeraParidad(codigoHamming):
    paridad1 = XOR(codigoHamming[8], codigoHamming[10])
    paridad1 = XOR(codigoHamming[6], paridad1)
    paridad1 = XOR(codigoHamming[4], paridad1)
    paridad1 = XOR(codigoHamming[2], paridad1)
    codigoHamming[0] = paridad1

#CALCULO DE LA 2DA PARIDAD
def segundaParidad(codigoHamming):
    paridad2 = XOR(codigoHamming[9], codigoHamming[10])
    paridad2 = XOR(codigoHamming[6], paridad2)
    paridad2 = XOR(codigoHamming[5], paridad2)
    paridad2 = XOR(codigoHamming[2], paridad2)
    codigoHamming[1] = paridad2

#CALCULO DE LA 3ERA PARIDAD
def terceraParidad(codigoHamming):
    paridad3 = XOR(codigoHamming[5], codigoHamming[6])
    paridad3 = XOR(codigoHamming[4], paridad3)
    codigoHamming[3] = paridad3

#CALCULO DE LA 4TA PARIDAD
def cuartaParidad(codigoHamming):
    paridad4 = XOR(codigoHamming[9], codigoHamming[10])
    paridad4 = XOR(codigoHamming[8], paridad4)
    codigoHamming[7] = paridad4


#COMUNICACION SERIAL PYTHON ARDUINO PARA EL ENVIO DE DATOS
dev = serial.Serial('COM16',9600)

#PROGRAMA PRINCIPAL EN ESTE SE CALCULA EL CODIGO HAMMING
def calcularCodigoHamming():
    codigoHamming = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    datosRecibidos = []
    for i in range(7):
        dato = input_entries[i].get()
        if dato not in ('0', '1'):
            etiquetaError.configure(text="Error en el ingreso de los datos", fg="red", font=("Arial", 8, "bold"))
            return
        datosRecibidos.append(int(dato))
    etiquetaError.configure(text="")
    
    #SE COLOCAN LOS DATOS EN SU POSICION RESPECTIVA PARA EL CODIGO HAMMING
    codigoHamming[2] = datosRecibidos[0]
    codigoHamming[4] = datosRecibidos[1]
    codigoHamming[5] = datosRecibidos[2]
    codigoHamming[6] = datosRecibidos[3]
    codigoHamming[8] = datosRecibidos[4]
    codigoHamming[9] = datosRecibidos[5]
    codigoHamming[10] = datosRecibidos[6]

    #SE CALCULAN LAS 4 PARIDADES
    primeraParidad(codigoHamming)
    segundaParidad(codigoHamming)
    terceraParidad(codigoHamming)
    cuartaParidad(codigoHamming)

    #SE CREAR UN STRING CON EL CODIGO HAMMING PARA MOSTRAR EN LA INTERFAZ
    hamming_code = "   ".join(map(str, codigoHamming))
    hamming_code_label.configure(text=hamming_code, fg="black")
    
    #CONVERTIR A STRING EL CODIGO HAMMING PARA ENVIARLO
    hammingString = ', '.join(map(str, codigoHamming))
    hammingString = hammingString +","
    dev.write(hammingString.encode())
    print("CODIGO HAMMING GENERADO ENVIADO")
    print(hammingString)   

#CREAR VENTANA PRINCIPAL
window = tk.Tk()
window.title("Transmisor Codigo Hamming")
window.geometry("500x500")


#CARGAR LA IMAGEN Y PONERLA EN LA PARTE SUPERIOR
image_path = "C:/Users/redes/Downloads/Hamming Parte I (INTERFAZ, COMUNICACION SERIAL y I2C)/Codigo Python/LogoUlima.png"
image = Image.open(image_path)
image = image.resize((200, 200))
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(window, image=photo)
image_label.pack()


#CREAR CONTENEDOR PARA AGRUPAR WIDGETS,CON UN TAMAÑO DE 20 PIXELES ARRIBA Y ABAJO
container = tk.Frame(window)
container.pack(pady=20)


#ETIQUETA PARA INDICAR EL INGRESO DE LOS DATOS
input_label = tk.Label(container, text="Ingresar los Datos:", font=("Arial", 12, "bold"))
input_label.pack()


#CREAR LAS ETIQUETAS Y LAS ENTRADAS DE LOS DATOS
frame = tk.Frame(container)
frame.pack(pady=10)
input_entries = []
for i in range(7):
    entry = tk.Entry(frame, width=5)
    entry.pack(side="left", padx=5)
    input_entries.append(entry)


#CREACION DE ETIQUETA ERROR
etiquetaError = tk.Label(window, text="", fg="red", font=("Arial", 12, "bold"))
etiquetaError.pack()


#BOTON PARA GENERAR CODIGO HAMMING Y ENVIAR LOS DATOS POR COMUNICACION SERIAL
calculate_button = tk.Button(window, text="Generar Codigo Hamming", command=calcularCodigoHamming)
calculate_button.pack(pady=10)


#MOSTRAR MENSAJE CODIGO HAMMING GENERADO
hamming_label = tk.Label(window, text="Codigo Hamming Generado:", font=("Arial", 12, "bold"))
hamming_label.pack(pady=5)


#CREACION DE ETIQUETA PARA MOSTRAR EL CODIGO HAMMING
hamming_code_label = tk.Label(window, text="", font=("Arial", 14))
hamming_code_label.pack()

#CERRAR VENTANA
def cerrar():
	window.destroy()
	print("VENTANA CERRADA EXITOSAMENTE")

window.protocol("WM_DELETE_WINDOW", cerrar) 

window.mainloop()