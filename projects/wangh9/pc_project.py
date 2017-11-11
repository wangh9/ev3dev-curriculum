import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    root = tkinter.Tk()
    root.title("Seller")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: some_callback1(mqtt_client, int(left_speed_entry.get()),
                                                       int(right_speed_entry.get()))
    root.bind('<Up>',
              lambda event: some_callback1(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: some_callback4(mqtt_client)
    root.bind('<Left>', lambda event: some_callback4(mqtt_client))
    # left_button and '<Left>' key

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: some_callback2(mqtt_client)
    root.bind('<space>', lambda event: some_callback2(mqtt_client))
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: some_callback3(mqtt_client)
    root.bind('<Right>', lambda event: some_callback3(mqtt_client))
    # right_button and '<Right>' key

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: some_callback5(mqtt_client, int(left_speed_entry.get()),
                                                    int(right_speed_entry.get()))
    root.bind('<Down>',
              lambda event: some_callback5(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))
    # back_button and '<Down>' key

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))


    root.mainloop()


def some_callback1(mqtt_client,leftspeed,rightspeed):
    print('forward')
    mqtt_client.send_message('forward',[leftspeed,rightspeed])


def some_callback2(mqtt_client):
    print('stop')
    mqtt_client.send_message('stop')

def some_callback3(mqtt_client):
    print('right')
    mqtt_client.send_message('right')

def some_callback4(mqtt_client):
    print('left')
    mqtt_client.send_message('left')

def some_callback5(mqtt_client,leftspeed,rightspeed):
    print('back')
    mqtt_client.send_message('forward', [-leftspeed, -rightspeed])

# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()
main()