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


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor


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

    def arm_up(self, arm_motor, touch_sensor):
        """
        Moves the Snatch3r arm to the up position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
          :type touch_sensor: ev3.TouchSensor
        """
        # DONE: 4. Implement the arm up movement by fixing the code below
        # Command the arm_motor to run forever in the positive direction at max speed.
        # Create a while loop that will block code execution until the touch sensor is pressed.
        #   Within the loop sleep for 0.01 to avoid running code too fast.
        # Once past the loop the touch sensor must be pressed. Stop the arm motor using the brake stop action.
        # Make a beep sound

        # Code that attempts to do this task but has many bugs.  Fix them!
        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

    def arm_down(self,arm_motor):
        """
        Moves the Snatch3r arm to the down position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
        """
        # DONE: 5. Implement the arm up movement by fixing the code below
        # Move the arm to the absolute position_sp of 0 at max speed.
        # Wait until the move completes
        # Make a beep sound

        # Code that attempts to do this task but has bugs.  Fix them.
        arm_revolutions_for_full_range = 14.2 * 360
        arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        arm_motor.position = 0

    def arm_calibration(self,arm_motor, touch_sensor):
        """
        Runs the arm up until the touch sensor is hit then back to the bottom again, beeping at both locations.
        Once back at in the bottom position, gripper open, set the absolute encoder position to 0.  You are calibrated!
        The Snatch3r arm needs to move 14.2 revolutions to travel from the touch sensor to the open position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
          :type touch_sensor: ev3.TouchSensor
        """
        # DONE: 3. Implement the arm calibration movement by fixing the code below (it has many bugs).  It should to this:
        #   Command the arm_motor to run forever in the positive direction at max speed.
        #   Create an infinite while loop that will block code execution until the touch sensor's is_pressed value is True.
        #     Within that loop sleep for 0.01 to avoid running code too fast.
        #   Once past the loop the touch sensor must be pressed. So stop the arm motor quickly using the brake stop action.
        #   Make a beep sound
        #   Now move the arm_motor 14.2 revolutions in the negative direction relative to the current location
        #     Note the stop action and speed are already set correctly so we don't need to specify them again
        #   Block code execution by waiting for the arm to finish running
        #   Make a beep sound
        #   Set the arm encoder position to 0 (the last line below is correct to do that, it's new so no bug there)

        # Code that attempts to do this task but has MANY bugs (nearly 1 on every line).  Fix them!
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

    def  ir_sensor(self):
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor
