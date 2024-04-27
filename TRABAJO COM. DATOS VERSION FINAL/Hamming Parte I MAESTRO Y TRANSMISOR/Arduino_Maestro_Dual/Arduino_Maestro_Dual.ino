#include <Wire.h>
//TAMAÑO DEL ARRAY
const int SIZE = 11;
//CREAR ARRAY
int codigoHamming[SIZE];

void setup() 
{
  Serial.begin(9600);
  //PINES DE ENTRADA
  pinMode(22,INPUT);
  pinMode(23,INPUT);
  pinMode(24,INPUT);
  pinMode(25,INPUT);
  pinMode(26,INPUT);
  pinMode(27,INPUT);
  pinMode(28,INPUT);
  pinMode(29,INPUT);
  pinMode(30,INPUT);
  pinMode(31,INPUT);
  pinMode(32,INPUT);
  //PINES DE SALIDA
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);
  Wire.begin(1);
}

// ARREGLO DE PINES DE ENTRADA DEL ARDUINO ESCLAVO
byte pin[] ={2,3,4,5,6,7,8,9,10,11,12};

void loop() 
{
  if (Serial.available()) 
  {
    /*ALMACENA LO RECIBIDO EN UN STRING*/
    String data = Serial.readString();
    /*CONVERTIR EL STRING EN UN ARRAY DE INT*/
    int i = 0; //INDICE PARA RECORRER EL ARRAY codigoHamming
    int indiceInicio = 0; //INDICA EL INDICE DE INICIO DE LA SUBCADENA QUE SE EXTRAE
    int indiceFin = data.indexOf(','); //INDICA LA POSICION DONDE SE ENCUENTRA LA COMA, SINO ENCUENTRA DEVUELVE -1 (PARTE DE LA CLASE STRING)

    /*SE EJECUTARA MIENTRAS HAYAN COMAS EN EL STRING Y EL ARRAY TENGA ESPACIO LIBRE*/
    while (indiceFin != -1 && i < SIZE) 
    {
      String elementoString = data.substring(indiceInicio, indiceFin); //ES UNA FUNCION DE LA CLASE STRING, EXTRAE LO QUE SE ENCUENTRA ENTRE EL INICIO Y LA COMA
      codigoHamming[i] = elementoString.toInt(); //CONVIERTE EL ELEMENTO STRING EN UN INT Y SE ALMACENA EN LA POSICION i DE ARRAY
      i++; //AUMENTA EL INDICE EN 1
      indiceInicio = indiceFin + 1; //EL NUEVO INICIO ES EL INDICE FINAL + 1
      indiceFin = data.indexOf(',', indiceInicio); //SE ACTUALIZA EL INDICE DESDE DONDE SE DEBE BUSCAR LA SIGUIENTE COMA
    }

    /*ENCENDER LEDS*/  
    for (int j = 0; j < SIZE; j++)
    {
      if(codigoHamming[j]==1)
      { 
        digitalWrite((j+2),HIGH);
      }
      if(codigoHamming[j]==0)
      {
        digitalWrite((j+2),LOW);
      }
      
    }
    /*LEE LOS LEDS DE ENTRADA Y LOS ENVIA COMO ESTADOS PARA LOS PINES QUE RECIBIRÁ EL ARDUINO ESCLAVO MEDIANTE I2C*/
  }
  for(int i=0;i<11;i++)
    {
      Wire.beginTransmission(1);
      Wire.write(pin[i]);
      Wire.write(digitalRead(i+22));
      Wire.endTransmission();
      delay(300);
    }
}
