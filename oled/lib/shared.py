from machine import I2C, Pin
from time import sleep
from lib.ssd1306 import SSD1306_I2C

i2c = I2C(id=1, scl=Pin(7), sda=Pin(6))

# Menu Variables
line = 1 
highlight = 1
shift = 0
list_length = 0
TOTAL_LINES = 6

oled = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=i2c.scan()[0])
oled.init_display()

button_pin = Pin(0, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(1, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(2, Pin.IN, Pin.PULL_UP)

previous_value = True
button_down = False