#include <Wire.h>
int i=0;
void setup()
{
  /*COMIENZO DE LA COMUNICACION SERIAL*/
  Serial.begin(9600);

  /*PINES DE SALIDA*/
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
  
  /*PINES DE ENTRADA*/
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
  
  /*COMIENZO DE LA COMUNICACION I2C*/
  Wire.begin(1);
  /*SE LLAMA A LA FUNCION PARA LA RECEPCION DE PINES Y ESTADOS*/
  if(i<11)
  {
    Wire.onReceive(receiveEvent);
    //Serial.println(i);
  }
}

void loop()
{
  delay(300);
  /*UNA VEZ LLEGUE I=11, SE LLAMA A LA FUNCION ALMACENAR PARA GUARDAR EN UN STRING LOS ESTADOS*/
  if(i==11)
  {
    almacenar();
  }
}

void receiveEvent(int c)
{
  int pinOut=0;
  int estado=0;
  int codigo;
  if(Wire.available()==2)
  {
    pinOut=Wire.read();
  }
  if(Wire.available()==1)
  {
    estado=Wire.read();
  }
  digitalWrite(pinOut,estado);
  i++;
}

void almacenar()
{
  String codigoHamming = "";
  int num =0;
  if(num==0)
  {
  /*LEE LOS PINES DE ENTRADA*/
    for(int i=22;i<=32;i++)
    {
      if(digitalRead(i)==1)
      {
        codigoHamming += "1 ";
      }
      if(digitalRead(i)==0)
      {
        codigoHamming+="0 ";
      }
    }
  }
  delay(2000);
  Serial.println(codigoHamming);
  delay(2000);
  num++;
  //ESTE FUE EL ULTIMO CAMBIO, ORIGINALMENTE i++
  i=0;
}
