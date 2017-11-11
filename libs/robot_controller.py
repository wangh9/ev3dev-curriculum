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
color_sensor = ev3.ColorSensor()


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor
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

    def seek_beacon(self):
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100

        while not touch_sensor.is_pressed:

            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) > 2 and math.fabs(current_heading) < 10:
                    print("start finding!", current_heading)
                    if (current_heading > 2):
                        self.forward(turn_speed, -turn_speed)
                    if (current_heading < -2):
                        self.forward(-turn_speed, turn_speed)
                if math.fabs(current_heading) > 10:
                    print("Heading too far off", current_heading)
                    self.stop()

                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if (current_distance > 0):
                        self.forward(forward_speed, forward_speed)
                    if current_distance == 0:
                        self.forward(forward_speed, forward_speed)
                        time.sleep(0.8)
                        self.stop()
                        return True
            time.sleep(0.2)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False

    def drive_to_color(button_state, robot, color_to_seek):
        """
        When the button_state is True (pressed), drives the robot forward until the desired color is detected.
        When the color_to_seek is detected the robot stops moving forward and speaks a message.

        Type hints:
          :type button_state: bool
          :type robot: robo.Snatch3r
          :type color_to_seek: int
        """
        COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
        if button_state:
            ev3.Sound.speak("Seeking " + COLOR_NAMES[color_to_seek]).wait()
            robot.forward(600, 600)
            while (robot.color_sensor.color != color_to_seek):
                time.sleep(0.01)
            robot.stop()
            # DONE: 3. Implement the task as stated in this module's initial comment block
            # It is recommended that you add to your Snatch3r class's constructor the color_sensor, as shown
            #   self.color_sensor = ev3.ColorSensor()
            #   assert self.color_sensor
            # Then here you can use a command like robot.color_sensor.color to check the value



            # DONE: 4. Call over a TA or instructor to sign your team's checkoff sheet.
            #
            # Observations you should make, the instance variable robot.color_sensor.color is always updating
            # to the color seen and that value is given to you as an int.

            ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()

    def find_the_target(self,code1,state1,state2,state3):
        if code1 == 8147:
            if state1 == True and state2 == False and state3 == False:
                print("go to Olin")
                ev3.Sound.speak("Olin it is").wait()
                time.sleep(1)
                left_motor.run_forever(speed_sp=600)
                right_motor.run_forever(speed_sp=600)
                while (color_sensor.color != "Red"):
                    time.sleep(0.01)
                left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

            if state1 == False and state2 == True and state3 == False:
                print("go to Monech")
                ev3.Sound.speak("Monech it is").wait()

            if state1 == False and state2 == False and state3 == True:
                print("go to Library")
                ev3.Sound.speak("library it is").wait()
        else:
            ev3.Sound.speak("You are a Robot Bob").wait()