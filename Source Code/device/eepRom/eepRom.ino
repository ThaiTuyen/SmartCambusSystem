#include <EEPROM.h>
void setup() {
  // put your setup code here, to run once:
for (int i = 0; i < 255; i++)
    {EEPROM.write(i, i);
    delay(5); }
    //EEPROM.commit();
}

void loop() {
  // put your main code here, to run repeatedly:

}
