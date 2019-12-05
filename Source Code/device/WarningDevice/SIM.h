#ifndef SIM_H_
#define SIM_H_
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include <SoftwareSerial.h>

class SIM
{
  public:
    SIM();
    ~SIM();
    void Begin();
    void SetSIMPort(SoftwareSerial* SIMSerialPort);
    void SetSIMPort(HardwareSerial& SIMSerialPort);
    bool sendCommand(String command);
    String waitForMessage(int timeout);
    bool waitForMessage(String stringInMess, int timeout);
    String receivedMessage();
    
  protected:
    SoftwareSerial* swSerialPort;
    HardwareSerial* hwSerialPort;
    Stream* SIMSerialPort;
    bool debugPort = true;
    
  private:
    void bufferFlush();
    bool TCPSetup();

};

#endif /* SIM_H_ */
