void enterSleep(void)
{
  attachInterrupt(1, ButionInterrupt, FALLING);
  set_sleep_mode(SLEEP_MODE_IDLE);

  sleep_enable();
  power_adc_disable();
  power_spi_disable();
  power_timer0_disable();
  power_timer2_disable();
  power_twi_disable();
  /* Now enter sleep mode. */
  sleep_mode();
  /* The program will continue from here after the timer timeout*/
  sleep_disable(); /* First thing to do is disable sleep. */
  /* Re-enable the peripherals. */
  power_all_enable();
}


void CheckBution()
{
  if (digitalRead(Bution) == LOW)
  {
    delay(2000);
    if (digitalRead(Bution) == LOW)
    { NetworkLed(3, 500);
      if (!NetworkOn)
      {
        TIMSK1 = (1 << TOIE1);
        sprintf (msg, "%s%s%s%s%s", "{\"RECNWFG\",\"A:\"" , ACK, "\",\"I:\"" , KEY, "\"}");
        loraBoard.SendMessage((byte)(deviceAddrH), (byte)(deviceAddrL), msg);
        memset(msg, '\0', 80);
        NetworkOn = true;
      } else
      {
        sprintf (msg, "%s%s%s%s%s", "{\"UNCNWFG\",\"A:\"" , ACK, "\",\"I:\"" , KEY, "\"}");
        loraBoard.SendMessage((byte)(deviceAddrH), (byte)(deviceAddrL), msg);
        memset(msg, '\0', 80);
        TIMSK1 = (0 << TOIE1);
        NetworkOn = false;
      }
      EEPROM.write(100, NetworkOn);
      delay(5);
      while (digitalRead(Bution) == LOW);
    } else if (NetworkOn)
    {
      getAndSendData();
    }
  }
}

void  ButionInterrupt()
{
  ButionON = true;
  //detachInterrupt(1);
}

void ReadEEPROM()
{
  NetworkOn = bool(EEPROM.read(100));
}


void timerSetup()
{
  /* Reset Timer/Counter1 */
  TCCR1A = 0;
  TCCR1B = 0;
  TIMSK1 = 0;
  /* Setup Timer/Counter1 */
  TCCR1B |= (1 << CS12) | (0 << CS11) | (1 << CS10);
  TCNT1 = 3036;
  TIMSK1 = (1 << TOIE1);
}


ISR (TIMER1_OVF_vect)
{
  TCNT1 = 3036;
  Wait = Wait + 1;
  cout = 0;
  if (Wait >= 5) //15= 1 mins
  {
    sendMes = true;
    Wait = 0;
  }
}
