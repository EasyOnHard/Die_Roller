from machine import Pin, I2C
from time import sleep
from lib.ssd1306 import SSD1306_I2C
import framebuf

id = 1
sda = Pin(6)
scl = Pin(7)

i2c = I2C(id=1, scl=Pin(7), sda=Pin(6))

oled = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=i2c.scan()[0])
oled.init_display()

oled.fill(1)
oled.show()

sleep(1)