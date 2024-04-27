from PIL import ImageTk, Image
import tkinter
import serial

#FUNCION XOR PARA EL CODIGO HAMMING
def XOR(a, b):
    if a == 1 and b == 1:
        return 0
    elif a == 0 and b == 0:
        return 0
    else:
        return 1

#FUNCION PARA CALCULAR LA PRIMERA PARIDAD
def primeraParidad(codigoHammingComparar):
    paridad1 = XOR(codigoHammingComparar[8], codigoHammingComparar[10])
    paridad1 = XOR(codigoHammingComparar[6], paridad1)
    paridad1 = XOR(codigoHammingComparar[4], paridad1)
    paridad1 = XOR(codigoHammingComparar[2], paridad1)
    codigoHammingComparar[0] = paridad1

#FUNCION PARA CALCULAR LA SEGUNDA PARIDAD
def segundaParidad(codigoHammingComparar):
    paridad2 = XOR(codigoHammingComparar[9], codigoHammingComparar[10])
    paridad2 = XOR(codigoHammingComparar[6], paridad2)
    paridad2 = XOR(codigoHammingComparar[5], paridad2)
    paridad2 = XOR(codigoHammingComparar[2], paridad2)
    codigoHammingComparar[1] = paridad2

#FUNCION PARA CALCULAR LA TERCERA PARIDAD
def terceraParidad(codigoHammingComparar):
    paridad3 = XOR(codigoHammingComparar[5], codigoHammingComparar[6])
    paridad3 = XOR(codigoHammingComparar[4], paridad3)
    codigoHammingComparar[3] = paridad3

#FUNCION PARA CALCULAR LA CUARTA PARIDAD
def cuartaParidad(codigoHammingComparar):
    paridad4 = XOR(codigoHammingComparar[9], codigoHammingComparar[10])
    paridad4 = XOR(codigoHammingComparar[8], paridad4)
    codigoHammingComparar[7] = paridad4

#COMUNICACION SERIAL ARDUINO PYTHON PARA EL RECIBO DE DATOS
dev = serial.Serial('COM3', 9600)

def actualizarHammingRecibido():
    #SE UTILIZA UN BUCLE INFINITO PORQUE TIENE QUE ESPERAR INDEFINIDAMENTE HASTA QUE HAYAN DATOS QUE LEER DEL ARDUINO
    while True:
        #VERIFICA SI HAY DATOS QUE LEER DEL ARDUINO
        if dev.in_waiting > 0:
            #LEE LA LINEA RECIBDA DEL ARDUINO, CONVIERTE LOS BYTES RECIBIDOS EN UNA CADENA UTF-8 Y POR ULTIMO ELIMINA LAS CUALQUIER CARACTER DE NUEVA LINEA O ESPACIO EN BLANCO
            hammingString = dev.readline().decode().rstrip()
            #CONVIERTE EL STRING EN UN ARRAY DE ENTEROS, SEPRANDOLOS POR LOS ESPACIOS EN BLANCO ENTRE LOS NUMERO DEL STRING RECIBIDO
            hammingEnteros = [int(num) for num in hammingString.split()]
            #REGRESA EL HAMMING RECIBIDO EN UN ARRAY
            return hammingEnteros
            #ROMPE EL BUCLE INFINITO
            break

#SE VERIIFCA SI HAY ERRORES COMPARANDO EL HAMMING RECIBIDO CON EL HAMING PARA COMPARA Y SI HAY ALGUN ERROR SE SUMA Y DEVUELVE LA POSICION DEL ERROR
def compararParidades(codigoHammingRecibido, codigoHammingComparar):
    posicionError = 0
    if codigoHammingRecibido[7] != codigoHammingComparar[7]:
        posicionError += 8
    if codigoHammingRecibido[3] != codigoHammingComparar[3]:
        posicionError += 4
    if codigoHammingRecibido[1] != codigoHammingComparar[1]:
        posicionError += 2
    if codigoHammingRecibido[0] != codigoHammingComparar[0]:
        posicionError += 1
    return posicionError

#CORRIGE DONDE ESTA EL ERROR
def corregir(codigoHammingRecibido, error):
    lista = ""
    if codigoHammingRecibido[error] == 1:
        codigoHammingRecibido[error] = 0
    elif codigoHammingRecibido[error] == 0:
        codigoHammingRecibido[error] = 1

    msg2.config(text="El codigo Hamming recibido tiene un error en la posición: " + str(error + 1))
    msg3.config(text="El codigo hamming corregido es:")
    print("El codigo hamming corregido es: ")
    print(codigoHammingRecibido)
    aux = [("  " + str(item)) for item in codigoHammingRecibido]
    lista = lista.join(aux)
    return lista

def actualizarInterfazGrafica():
    codigoHammingRecibido = actualizarHammingRecibido()
    print(codigoHammingRecibido)
    codigoHammingComparar = codigoHammingRecibido[:]
    lista = ""
    aux = [("  " + str(item)) for item in codigoHammingRecibido]
    lista = lista.join(aux)
    msg.config(text=lista)
    #GENERAR PARIDADES
    primeraParidad(codigoHammingComparar)
    segundaParidad(codigoHammingComparar)
    terceraParidad(codigoHammingComparar)
    cuartaParidad(codigoHammingComparar)
    #VERIFICAR EL ERROR
    error = compararParidades(codigoHammingRecibido, codigoHammingComparar)
    if error == 0:
        print("El codigo Hamming recibido no tiene errores.")
        msg2.config(text="El codigo Hamming recibido no tiene errores.")
    else:
        print("El codigo Hamming recibido tiene un error en la posicion:", (error))
        error = error - 1
        lista = corregir(codigoHammingRecibido, error)
        print(lista)
        #ACTUALIZAR EL CODIGO HAMMING DE LA INTERFAZ GRAFICA
        msg.config(text=lista)

#CREAR VENTANA PRINCIPAL
win = tkinter.Tk()
win.title("Receptor Codigo Hamming")
win.geometry("500x500") 

#CARGAR LA IMAGEN Y PONERLA EN LA PARTE SUPERIOR
image_path = "C:/Users/usuario/Desktop/TRABAJO COM. DATOS VERSION FINAL\Hamming Parte II ESCLAVO (GRAFICA, I2C y COMUNICACION SERIAL)/Codigo Python/UlimaLogo.png"
image = Image.open(image_path)
image = image.resize((200, 200))
photo = ImageTk.PhotoImage(image)
image_label = tkinter.Label(win, image=photo)
image_label.pack()

#MUESTRA EL MENSAJE "HAMMING RECIBIDO"
input_label = tkinter.Label(win, text="El Codigo Hamming recibido es:", font=("Arial", 12, "bold"))
input_label.pack()

#CREAR CONTENEDOR PARA AGRUPAR WIDGETS,CON UN TAMAÑO DE 20 PIXELES ARRIBA Y ABAJO
container = tkinter.Frame(win)
container.pack(pady=20)

#MUESTRA EL HAMMING RECIBIDO
msg = tkinter.Label(container, text= "", font=("Arial", 12, "bold"))
msg.pack(side=tkinter.TOP)

#MENSAJE ERROR POSICION
msg2 = tkinter.Label(win, text= "", font=("Arial", 12, "bold"))
msg2.pack(side=tkinter.TOP)

#MENSAJE HAMMING CORREGIDO
msg3 = tkinter.Label(win, text= "", font=("Arial", 12, "bold"))
msg3.pack(side=tkinter.TOP)

#SE CREA UN CONTENEDOR PARA PARA AGRUPAR Y ORGANIZAR    
container2 = tkinter.Frame(win)
container2.pack(pady=20)

#EJECUTA LA FUNCION MAIN
msg4 = tkinter.Label(container2, text="", font=("Arial", 12, "bold"))
msg4.pack(side=tkinter.TOP)

#BOTÓN PARA ACTUALIZAR LA INTERFAZ GRÁFICA
button = tkinter.Button(win, text="Actualizar", font=("Arial", 14, "bold"), command=actualizarInterfazGrafica)
button.pack(pady=20)

#CERRAR VENTANA
def cerrar():
    win.destroy()
    print("Ventana cerrada exitosamente")
win.protocol("WM_DELETE_WINDOW", cerrar) # cuando ocurra "x", cerrar la ventana

win.mainloop()