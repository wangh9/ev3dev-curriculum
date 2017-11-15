import ev3dev.ev3 as ev3
import time

import robot_controller as robo


left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
touch_sensor = ev3.TouchSensor()
class DataContainer(object):

    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print("IR Remote")
    print(" - Use IR remote channel 2 to drive around")
    print(" - Use IR remote channel 3 to for the arm")
    print(" - Press the Back button on EV3 to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("I R Remote")

    ev3.Leds.all_off()  # Turn the leds off
    robot = robo.Snatch3r()
    dc = DataContainer()

    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)


    assert touch_sensor
    rc1 = ev3.RemoteControl(channel=2)
    rc2 = ev3.RemoteControl(channel=3)

    rc1.on_red_up = lambda state: handle_red_up_1(state)
    rc1.on_red_down = lambda state: handle_red_down_1(state)
    rc1.on_blue_up = lambda state: handle_blue_up_1(state)
    rc1.on_blue_down = lambda state: handle_blue_down_1(state)

    rc2.on_red_up = lambda state: handle_arm_up_button(state,robot)
    rc2.on_red_down = lambda state: handle_arm_down_button(state,robot)
    rc2.on_blue_up = lambda state: handle_calibrate_button(state,robot)


    while dc.running:

        rc1.process()
        rc2.process()
        btn.process()
        time.sleep(0.01)

    robot.shutdown()

def handle_red_up_1(button_state):
    if button_state:
        left_motor.run_forever(speed_sp=800)
        time.sleep(0.01)
    else:
        left_motor.stop(stop_action="brake")

def handle_red_down_1(button_state):
    if button_state:
        left_motor.run_forever(speed_sp=-800)
        time.sleep(0.01)
    else:
        left_motor.stop(stop_action="brake")

def handle_blue_up_1(button_state):
    if button_state:
        right_motor.run_forever(speed_sp=800)
        time.sleep(0.01)
    else:
        right_motor.stop(stop_action="brake")

def handle_blue_down_1(button_state):
    if button_state:
        right_motor.run_forever(speed_sp=-800)
        time.sleep(0.01)
    else:
        right_motor.stop(stop_action="brake")


def handle_arm_up_button(button_state, robot):
    if button_state:
        robot.arm_up()


def handle_arm_down_button(button_state, robot):
    if button_state:
        robot.arm_down()


def handle_calibrate_button(button_state, robot):
    if button_state:
        robot.arm_calibration()


def handle_shutdown(button_state, dc):
    if button_state:
        dc.running = False

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
