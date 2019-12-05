#include <SoftwareSerial.h>
#include "UDOpenLora.h"
#include <Wire.h>
//#include <EEPROM.h>
#include <avr/sleep.h>
#include <avr/power.h>
#include "SIM.h"
#define SIM_RESET 6

#define DEBUGER

#define AUX_PIN 3
#define BUTTON_ON_PIN 11
#define BUTTON_OFF_PIN 2

#define M0_PIN 4
#define M1_PIN 5
#define IN1_RE A1
#define IN2_RE A2
#define lora_power TSMT_PWR_30DB

const int PIN_TX = 7;
const int PIN_RX = 8;
const int BAUDRATE = 9600;


HardwareSerial* debugSerial = &Serial;
SoftwareSerial LoraSerial(10, 9); // RX, TX
UDOpenLora loraBoard(&LoraSerial);

SoftwareSerial SimSerial(8, 7); // RX, TX
SIM Sim;

int networkAddrH = 0x50;
int networkAddrL = 0x50;
int networkChanel = 0x19;
int deviceAddrH = 0x00; // 1 device : 1 addrH & addrL : receiver device address
int deviceAddrL = 0x00;
byte SourceAddr_H, SourceAddr_L;
char data_buf[128];
uint8_t data_len;
char msg[50];
int length_t = 0;
void setup()
{
  // sim setup
  pinMode(SIM_RESET, INPUT);
  pinMode (IN1_RE, OUTPUT);
  pinMode (IN2_RE, OUTPUT);
  digitalWrite(IN1_RE, HIGH);
  digitalWrite(IN2_RE, HIGH);
  pinMode(BUTTON_ON_PIN, INPUT_PULLUP);
  pinMode(BUTTON_ON_PIN, INPUT_PULLUP);
#ifdef DEBUGER
  Serial.begin(9600);
#endif
  Sim.SetSIMPort(&SimSerial);
  Sim.Begin();
  LoraSerial.begin(9600);
  LoraSerial.listen();
  loraBoard.setDebugPort(debugSerial);
  Serial.print("Configure Lora Module: ");
  loraBoard.setIOPin(M0_PIN, M1_PIN, AUX_PIN);
  delay(1000);
  loraBoard.LoraBegin((byte)(networkAddrH), (byte)(networkAddrL), (byte)(networkChanel), lora_power);
  Serial.println("GATE DONE");
  // end setup sim
  sprintf (msg, "%s", "{\"ACMESWAR\",\"12345\"}");
  digitalWrite(IN2_RE, LOW);
  delay(500);
  digitalWrite(IN2_RE, HIGH);
}

void loop()
{
  if (CheckWarning())
  {
   HandleReceveMesageWarning();
  }
  CheckButtonWarning();
  //delay(10);
}

bool CheckWarning()
{
  String data = "";
  if (loraBoard.ReceiveMsg(&SourceAddr_H, &SourceAddr_L, data_buf, &data_len) == RET_SUCCESS)
  {
    Serial.println();
    Serial.print("Msg from: 0x");
    Serial.print(SourceAddr_H, HEX);
    Serial.println(SourceAddr_L, HEX);
    Serial.print("Message length:");
    Serial.println(data_len);
    for (int i = 0; i < data_len; i++)
    {
      data = data + data_buf[i];
    }
    Serial.print("Receive Message:");
    Serial.println(data);
    return (data.indexOf("WARNING") >= 0 && data.indexOf("12345") >= 0) ? true : false;
  }
  return false;
}

void HandleReceveMesageWarning()
{
  Serial.println("Have Warning mess");
  sprintf (msg, "%s", "{\"ACMESWAR\",\"12345\"}");
  loraBoard.SendMessage((byte)(deviceAddrH), (byte)(deviceAddrL), msg);
  memset(msg, '\0', 50);
  digitalWrite(IN1_RE, LOW);
  digitalWrite(IN2_RE, LOW);
  unsigned long timeStart = millis();
  bool makeCall = false;
  while (digitalRead(BUTTON_OFF_PIN) == HIGH)
  {
    if ((timeStart + 5000) < millis()&&makeCall==false)
    {
      HandleMakeCall();
      makeCall = true;
    }
    delay(10);
  }
  digitalWrite(IN1_RE, HIGH);
  digitalWrite(IN2_RE, HIGH);
  Serial.println("OK");
}

void CheckButtonWarning()
{
  if (digitalRead(BUTTON_ON_PIN) == LOW)
  {
    delay(100);
    if (digitalRead(BUTTON_ON_PIN) == LOW)
    {
      HandleButtonWarning();
    }
  }
}
void HandleButtonWarning()
{
  Serial.println("Have Warning button");
  digitalWrite(IN1_RE, LOW);
  digitalWrite(IN2_RE, LOW);
  unsigned long timeStart = millis();
  bool makeCall = false;
  while (digitalRead(BUTTON_OFF_PIN) == HIGH)
  {
    if ((timeStart + 5000) < millis()&&makeCall==false)
    {
      HandleMakeCall();
      makeCall = true;
    }
    delay(10);
  }
  digitalWrite(IN1_RE, HIGH);
  digitalWrite(IN2_RE, HIGH);
  Serial.println("OK");
}

void HandleMakeCall()
{
  Serial.println("Make Call");
  SimSerial.listen();
  delay(1000);
  Sim.sendCommand("AT");
  Sim.waitForMessage(1000);
  Sim.sendCommand("ATD+ +84932517611;");
  Sim.waitForMessage(1000);
  delay(2000);
  //Sim.sendCommand("ATH");
  //Sim.waitForMessage(1000);
  LoraSerial.listen();
}
