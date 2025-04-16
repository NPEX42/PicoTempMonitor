from machine import Pin
import time
from dht import DHT11
from machine import I2C, RTC

from I2C_LCD import I2CLcd

import os


DHT_PIN = 15
SDA_PIN = 4
SCL_PIN = 5
LED_PIN = 25

BACKLIGHT_PIN = 16


class TempMonitor():
    def __init__(self):
        self.dht = DHT11(Pin(DHT_PIN))
        self.LED = Pin(LED_PIN, Pin.OUT)
        self.i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
        self.devices = self.i2c.scan()
        self.lcd = I2CLcd(self.i2c, self.devices[0], 2, 16)
        self.lcd.putstr("Temp Monitor")
        time.sleep(3)
        self.lcd.clear()
        self.backlight_sense = Pin(BACKLIGHT_PIN, Pin.IN, Pin.PULL_UP)
        self.rtc = RTC()
        print(self.rtc.datetime()[5])
        
    def poll(self):
        self.dht.measure()
        self.pulseLED()
        
    
    def showLCD(self):
        self.lcd.move_to(0, 0)
        self.lcd.putstr(f"Temp: {self.dht.temperature()} C {self.rtc.datetime()[4]}:{self.rtc.datetime()[5]}")
        self.lcd.move_to(0, 1)
        self.lcd.putstr(f"Humidity: {self.dht.humidity()}%   ")
        if self.backlight_sense.value():
            self.lcd.backlight_on()#
        else:
            self.lcd.backlight_off()
    
    def pulseLED(self):
        self.LED.on();
        time.sleep_ms(100)
        self.LED.off();
        
    def saveToFlash(self):
        file = open("temps.csv", "a+")
        file.write(f"{self.rtc.datetime()[4]}:{self.rtc.datetime()[5]}:{self.rtc.datetime()[6]},{self.dht.temperature()},{self.dht.humidity()}\n")
        file.close()
        
        
        
        

tempMon = TempMonitor()



while True:
    time.sleep(1)
    tempMon.poll()
    tempMon.showLCD()
    tempMon.saveToFlash()