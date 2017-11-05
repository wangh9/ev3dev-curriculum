"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time

left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
touch_sensor = ev3.TouchSensor()


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy
        
    def drive_inches(self,lenth,velocity):
        """  """
        if lenth < 0:
            velocity = - velocity

        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        left_motor.run_forever(speed_sp=velocity)
        right_motor.run_forever(speed_sp=velocity)
        time_s = abs(lenth / (1.3 * math.pi * velocity / 360 + 0))
        time.sleep(time_s)
        left_motor.stop()
        right_motor.stop(stop_action="brake")

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        left_motor.run_to_rel_pos(position_sp= 450 * -degrees_to_turn/90,speed_sp = turn_speed_sp)
        right_motor.run_to_rel_pos(position_sp= 450 * degrees_to_turn/90,speed_sp = turn_speed_sp)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def arm_up(self):
        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

    def arm_down(self):
        arm_revolutions_for_full_range = 14.2 * 360
        arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        arm_motor.position = 0

    def arm_calibration(self):
        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        arm_revolutions_for_full_range = 14.2 * 360
        arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        arm_motor.position = 0

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        self.running = False

    def forward(self,leftspeed,rightspeed):
        left_motor.run_forever(speed_sp=leftspeed)
        right_motor.run_forever(speed_sp=rightspeed)

    def stop(self):
        left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def right(self):
        right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        left_motor.run_forever(speed_sp=600)

    def left(self):
        left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        right_motor.run_forever(speed_sp=600)

    def back(self, leftspeed, rightspeed):
        left_motor.run_forever(speed_sp=leftspeed)
        right_motor.run_forever(speed_sp=rightspeed)