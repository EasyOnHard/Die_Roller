import random
import board
import digitalio
import rotaryio
from time import sleep, monotonic

rotary = rotaryio.IncrementalEncoder(board.D8, board.D7)
button = digitalio.DigitalInOut(board.D6)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

previous_rotary_pos = None
previous_button_state = False
selected_menu_option = 0
selected_menu_number = None
in_menu = True


def roll(sides=20):
    return random.randrange(1, sides + 1, 1)


def button_press():
    global previous_button_state
    current_button_state = button.value
    if current_button_state and not previous_button_state:
        previous_button_state = current_button_state
        return True
    previous_button_state = current_button_state
    return False


def button_hold(hold_time=1.5):
    if not button.value:
        return False
    start_time = monotonic()
    while button.value:
        if monotonic() - start_time >= hold_time:
            return True
    return "Partially"


class menu:
    global selected_menu_option
    menu_options = [6, 8, 10, 12, 20]

    @staticmethod
    def menu(roll_result = None):
        for index, option in enumerate(menu.menu_options):
            if index == selected_menu_option:
                if roll_result != None and index == selected_menu_option:
                    print(f"[ d{option} ] d{option}: {roll_result}")
                else:
                    print(f"[ d{option} ]")
            else:
                print(f"  d{option} ")
        print("")

    @staticmethod
    def loop_menu():
        global selected_menu_option
        selected_menu_option = (rotary.position) % len(menu.menu_options)


menu.menu()
while True:
    if in_menu:
        position = rotary.position
        hold_result = button_hold(1)
        if hold_result is "Partially":
            selected_menu_number = menu.menu_options[selected_menu_option]
            menu.menu(roll(selected_menu_number))
            sleep(.5)
        elif previous_rotary_pos is None or position != previous_rotary_pos:
            menu.loop_menu()
            menu.menu()
        previous_rotary_pos = position
    sleep(0.01)
