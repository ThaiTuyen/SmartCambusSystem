void enterSleep(void)
{
  attachInterrupt(1, ButionInterrupt, FALLING);
  attachInterrupt(0, LoraMessInterrupt, FALLING);
  set_sleep_mode(SLEEP_MODE_IDLE);
  sleep_enable();
  power_adc_disable();
  power_spi_disable();
  power_timer0_disable();
  power_timer2_disable();
  power_twi_disable();
  /* Now enter sleep mode. */
  Serial.println("Sleep");
  sleep_mode();
  /* The program will continue from here after the timer timeout*/
  sleep_disable(); /* First thing to do is disable sleep. */
  /* Re-enable the peripherals. */
  power_all_enable();
  Serial.println("Wakeup");
}

void  LoraMessInterrupt()
{
  detachInterrupt(0);
}

void  ButionInterrupt()
{
  detachInterrupt(1);
}
