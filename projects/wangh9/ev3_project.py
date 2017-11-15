import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time

import robot_controller as robo
touch_sensor = ev3.TouchSensor()
def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.
main()

