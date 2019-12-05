

double getPressure() {
  char status;
  double T, P;
  status = pressure.startTemperature();
  if (status != 0) {
    delay(status);
    status = pressure.getTemperature(T);
    if (status != 0) {
      status = pressure.startPressure(3);
      if (status != 0) {
        delay(status);
        status = pressure.getPressure(P, T);
        if (status != 0) {
          return (P);
        }
      }
    }
  }
}

int get_Noise_Value()
{
  int analogData = analogRead(Noise_Mic_Pin);
  int noiseValue = (map(analogData, 0, 1023, 0, 100));
#ifdef DEBUG
  Serial.print("batteryValue : ");
  Serial.print(batteryValue);
  Serial.println(" :%");
#endif
  return noiseValue;
}

void NetworkLed(byte i)
{
  byte num = 0;
  do
  {
    digitalWrite(Network, HIGH);
    delay(200);
    digitalWrite(Network, LOW);
    delay(200);
    num = num + 1;
  } while ( num < i);
}

void NetworkLed(byte i, byte Delay)
{
  byte num = 0;
  do
  {
    digitalWrite(Network, HIGH);
    delay(Delay);
    digitalWrite(Network, LOW);
    delay(Delay);
    num = num + 1;
  } while ( num < i);
}


//if (data.indexOf("RQDATA") >= 0 && data.indexOf(String(ACK)) >= 0)
//data.indexOf("ACCNFG")
