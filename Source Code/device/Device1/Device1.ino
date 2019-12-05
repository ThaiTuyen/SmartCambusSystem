

#include <SoftwareSerial.h>
#include "SimpleKalmanFilter.h"
#include "SFE_BMP180.h"
#include "MQ2.h"
#include "UDOpenLora.h"
#include "DHT.h"
#include "max6675.h"
#include <EEPROM.h>
#include <avr/sleep.h>
#include <avr/power.h>

#define DHTPIN 2
#define AUX_PIN 4
#define Bution 3
#define max_TypeK_Pin 5
#define M0_PIN 7
#define M1_PIN 8
#define Network A0
#define GASPIN A1
#define Noise_Mic_Pin A2

#define lora_power TSMT_PWR_30DB
#define DHTTYPE DHT11
#define DEBUGER

SimpleKalmanFilter pressureKalmanFilter(1, 1, 0.01);
MAX6675 thermocouple1( max_TypeK_Pin);
SFE_BMP180 pressure;

DHT dht(DHTPIN, DHTTYPE);

MQ2 mq2(GASPIN);

HardwareSerial* debugSerial = &Serial;
SoftwareSerial LoraSerial(10, 9); // RX, TX
UDOpenLora loraBoard(&LoraSerial);

/*--------------SENDER------------*/

int networkAddrH = 0x30;
int networkAddrL = 0x30;
int networkChanel = 0x19;
int deviceAddrH = 0x00; // 1 device : 1 addrH & addrL : receiver device address
int deviceAddrL = 0x00;

char msg[80];
int length_t = 0;
byte h = 0;
byte t = 0;
float lpg = 0, co = 0; // mq2
volatile bool  NetworkOn = false, sendMes = false,ButionON = false;
volatile byte cout = 0, Wait = 0;
char KEY[] = "FG1234";
char ACK [] = "FG2302";

void setup() {
  ReadEEPROM();
  Serial.begin(9600);
  dht.begin();
  mq2.begin();
  thermocouple1.setupMax6675();
  pinMode(Network, OUTPUT);
  pinMode(Bution, INPUT);
  digitalWrite(Network, LOW);
  pressure.begin();
  LoraSerial.begin(9600);
  loraBoard.setDebugPort(debugSerial);
  Serial.print("Configure Lora Module: ");
  loraBoard.setIOPin(M0_PIN, M1_PIN, AUX_PIN);
  delay(1000);
  loraBoard.LoraBegin((byte)(networkAddrH), (byte)(networkAddrL), (byte)(networkChanel), lora_power);
  Serial.println("GATE DONE");
  timerSetup();
  if (NetworkOn) {
    TIMSK1 = (1 << TOIE1);
  }
  attachInterrupt(1, ButionInterrupt, FALLING);
  NetworkLed(4, 1000);
}

void loop() {
  if (sendMes&&NetworkOn)
  {
    getAndSendData();
    sendMes = false;
  }
   if (ButionON){
    CheckBution();
    ButionON = false;
   }
  else if (NetworkOn)
  {
      digitalWrite(Network, HIGH);
      delay(200);
      digitalWrite(Network, LOW);
  }
    TCNT1 = 3036;
    enterSleep();
//getAndSendData();
}

void getAndSendData()
{
  float estimated_Pressure = pressureKalmanFilter.updateEstimate(getPressure());
  int Tmax = thermocouple1.readCelsius();
  Serial.println(estimated_Pressure, 6);
for(int i = 1; i<5; i++)
{  
  co = mq2.read(true);
  Serial.println(co);
  delay(100);
}
  h = dht.readHumidity();
  t = dht.readTemperature();
  int Noise_value = get_Noise_Value();
  sprintf (msg, "%s%d%s%d%s%d%s%d%s%d%s%d%s", "{\"S:FG2302\",\"", t, "\",\"", h , "\",\"" , Tmax, "\",\"", int(estimated_Pressure), "\",\"", int(co) , "\",\"" , Noise_value, "\"}");
  loraBoard.SendMessage((byte)(deviceAddrH), (byte)(deviceAddrL), msg); //send message
  NetworkLed(2);
  memset(msg, '\0', 80);
}
