from lib.shared import *
from os import listdir

def get_files():
    files = listdir()
    menu = []
    for file in files:
        if file.endswith(".py") and file != "main.py":
            menu.append(file)
    return(menu)

def show_menu(menu):
    global line, highlight, shift, list_length
    item = 1
    line = 1
    line_height = 10
    short_list = menu [shift:shift+TOTAL_LINES]

    oled.fill(0)

    list_length = len(menu)

    if highlight > list_length:
        highlight = list_length
    if highlight < 1:
        highlight = 1

    # Adjust shift to ensure highlight is visible
    if highlight > shift + TOTAL_LINES:
        shift = highlight - TOTAL_LINES
    if highlight <= shift:
        shift = highlight - 1

    for item in short_list:
        if highlight == line:
            oled.fill_rect(0,(line-1)*line_height, 128, line_height, 1)
            oled.text(">", 0, (line-1)*line_height, 0)
            oled.text(item, 10, (line-1)*line_height, 0)
        else:
            oled.text(item, 10, (line-1)*line_height, 1)
        line += 1
    oled.show()

def launch(filename):
    global file_list
    oled.fill(0)
    oled.text("Launching...", 1, 10)
    oled.text(filename, 1, 20)
    oled.show()
    sleep(.5)
    exec(open(filename).read())
    oled.invert(0)
    show_menu(file_list)

file_list = get_files()
show_menu(file_list)

while True:

    if highlight > list_length:
        highlight = list_length
    elif highlight < 1:
        highlight = 1

    if previous_value != step_pin.value():
        if step_pin.value() == False:

            if direction_pin.value() == False:
                if highlight > 1:
                    highlight -= 1
                else:
                    if shift > 0:
                        shift -= 1
                
            else:
                if highlight < TOTAL_LINES:
                    highlight += 1
                else:
                    if shift+TOTAL_LINES < list_length:
                        shift += 1

            show_menu(file_list)
        previous_value = step_pin.value()   
    
    if button_pin.value() == False and not button_down:
        print("Launching") 
        #button_down = True
        launch(file_list[(highlight-1) + shift])

        print("Returned from Launch")

    if button_pin.value() == True and not button_down:
        button_down = False