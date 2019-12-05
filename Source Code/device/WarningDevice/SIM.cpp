#include "SIM.h"


SIM::SIM()
{
}

SIM::~SIM()
{
}

void SIM::Begin()
{
  if (hwSerialPort)
  {
    hwSerialPort->setTimeout(3000);
    hwSerialPort->begin(9600);
    this->SIMSerialPort =  hwSerialPort;
  } else
  {
    swSerialPort->setTimeout(3000);
    swSerialPort->begin(9600);
    this->SIMSerialPort =  (Stream*)swSerialPort;
  }
  delay(1000);
  sendCommand("ATE0");
  waitForMessage("OK", 1000);
  //sendCommand("AT + CIPCLOSE");
  //waitForMessage("OK", 1000);
}

void SIM::SetSIMPort(SoftwareSerial* SIMSerialPort)
{
  this->swSerialPort = SIMSerialPort;
}

void SIM::SetSIMPort(HardwareSerial& SIMSerialPort)
{
  this->hwSerialPort = &SIMSerialPort;
}

void SIM::bufferFlush()
{
  delay(500);
  while (SIMSerialPort->available() > 0)
  {
    SIMSerialPort->read();
  }
}

bool SIM::sendCommand(String command)
{
  bufferFlush();
  SIMSerialPort->print(command);
  SIMSerialPort->print("\r\n");
  if (debugPort == true)
  {
    Serial.print("\n> ");
    Serial.println(command);
  }
  delay(100);
}

String SIM::receivedMessage()
{
  String messageFromServer = "";
  if (SIMSerialPort->available() > 0)
  {
    delay(100);
    messageFromServer = SIMSerialPort->readString();
  }
  return messageFromServer;
}


String SIM::waitForMessage(int timeout)
{
  delay(timeout);
  String messRead = receivedMessage();
  if (debugPort == true)
  {
    Serial.print("messRead : ");
    Serial.println(messRead);
  }
  return messRead;
}

bool SIM::waitForMessage(String stringInMess, int timeout)
{
  unsigned long timeStart = millis();
  String messRead = "";
  while ((timeStart + timeout) > millis())
  {
    messRead += receivedMessage();
    if (messRead.indexOf(stringInMess) >= 0)
    {
      if (debugPort == true)
      {
        Serial.print("messRead : ");
        Serial.println(messRead);
      }
      return true;
    }
  }
  if (debugPort == true)
  {
    Serial.print("fales : messRead = ");
    Serial.println(messRead);
  }
  return false;
}

bool SIM::TCPSetup()
{
  bufferFlush();
  sendCommand("AT+ cipshut");
  waitForMessage(1000);
  sendCommand("AT + CIPMUX=0"); // muti connection
  waitForMessage(1000);
  sendCommand("AT+ CGATT=1"); // connect GPRS
  waitForMessage(1000);
  sendCommand("AT + CSTT = \"BikeLock\",\"\",\"\" "); //set apn
  waitForMessage("OK", 1000);
  sendCommand("AT+CIICR");
  if (!waitForMessage("OK", 2000))
  {
    return false;
  }
  sendCommand("AT+CIFSR");
  waitForMessage(2000);
  sendCommand("AT+CIPSPRT=1");
  waitForMessage(500);
  return true;
}
