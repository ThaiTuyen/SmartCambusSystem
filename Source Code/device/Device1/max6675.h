// this library is public domain. enjoy!
// www.ladyada.net/learn/sensors/thermocouple

#if ARDUINO >= 100
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif
 
  
class MAX6675 {
 public:
  MAX6675( int8_t CS);

  double readCelsius(void);
  void setupMax6675(void);
  double readFahrenheit(void);
  // For compatibility with older versions:
  double readFarenheit(void) { return readFahrenheit(); }
 private:
  int8_t  cs;
  int8_t sclk = 13, miso = 12;
  uint8_t spiread(void);
};
