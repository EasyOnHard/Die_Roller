from lib.shared import *
from random import randint

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

def roll(die):
    global button_down, line, highlight
    
    # Simulate a dice roll
    roll_result = randint(1, int(die[1:]))  # Extract the dice size from "d20", "d6", etc.
    
    # Display the roll result on the highlighted line
    line_height = 10
    y_position = (highlight - 1) * line_height  # Calculate the y-position of the highlighted line
    
    oled.fill_rect(0, y_position, 128, line_height, 1)
    oled.text(">", 0, y_position, 0)
    oled.text(die, 10, y_position, 0)  # Display the dice name on the highlighted line
    oled.text(str(roll_result), 80, y_position, 0)  # Display the roll result next to it
    oled.show()
    
    # Wait for the button to be released before returning
    while button_pin.value() == False:
        pass

dice = ["d20", "d4", "d6", "d12", "d100"]
show_menu(dice)

while True:
    previous_highlight = highlight

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

            show_menu(dice)
        previous_value = step_pin.value()   
    
    if button_pin.value() == False and not button_down:
        button_down = True
        roll(dice[(highlight-1) + shift])

    if button_pin.value() == True and button_down:
        button_down = False