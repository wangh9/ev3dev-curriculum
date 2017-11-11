import tkinter as tk
from tkinter import ttk
import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com

left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
touch_sensor = ev3.TouchSensor()



def main():
    # DONE: 2. Setup an mqtt_client.  Notice that since you don't need to receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).
    # Delete this line, it was added temporarily so that the code we gave you had no errors.
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tk.Tk()
    root.title("Bob finder")
    photo = tk.PhotoImage(file="")
    check_state1 = tk.IntVar()
    check_state2 = tk.IntVar()
    check_state3 = tk.IntVar()

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    Question_lable = ttk.Label(main_frame, text="Where are you Bob?")
    Question_lable.grid(row=0, column=0)
    select_olin= tk.Checkbutton(main_frame,text="Olin Hall",variable=check_state1)
    select_olin.deselect()
    select_olin.grid(row=1, column=0)

    select_monech= tk.Checkbutton(main_frame,text="Monech Hall",variable=check_state2)
    select_monech.deselect()
    select_monech.grid(row=1, column=1)

    select_library= tk.Checkbutton(main_frame,text="Logan Library",variable=check_state3)
    select_library.deselect()
    select_library.grid(row=1, column=2)




    # right_speed_entry = ttk.Entry(main_frame, width=8, justify=tk.RIGHT)
    # right_speed_entry.insert(0, "600")
    # right_speed_entry.grid(row=1, column=2)

    # DONE: 3. Implement the callbacks for the drive buttons. Set both the click and shortcut key callbacks.
    #
    # To help get you started the arm up and down buttons have been implemented.
    # You need to implement the five drive buttons.  One has been writen below to help get you started but is commented
    # out. You will need to change some_callback1 to some better name, then pattern match for other button / key combos.
    confirm_button = ttk.Button(main_frame, text="Confirm")
    confirm_button.grid(row=2, column=1)
    # confirm_button['command'] = lambda: some_callback1(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    # root.bind('<Enter>', lambda event: some_callback1(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    answer_lable = ttk.Label(main_frame, text=" ")
    answer_lable.grid(row=3, column=0)
    # left_button = ttk.Button(main_frame, text="Left")
    # left_button.grid(row=3, column=0)
    # left_button['command'] = lambda: some_callback4(mqtt_client)
    # root.bind('<Left>', lambda event: some_callback4(mqtt_client))
    # left_button and '<Left>' key

    # stop_button = ttk.Button(main_frame, text="Stop")
    # stop_button.grid(row=3, column=1)
    # stop_button['command'] = lambda: some_callback2(mqtt_client)
    # root.bind('<space>', lambda event: some_callback2(mqtt_client))
    # # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    #
    # right_button = ttk.Button(main_frame, text="Right")
    # right_button.grid(row=3, column=2)
    # right_button['command'] = lambda: some_callback3(mqtt_client)
    # root.bind('<Right>', lambda event: some_callback3(mqtt_client))
    # # right_button and '<Right>' key
    #
    # back_button = ttk.Button(main_frame, text="Back")
    # back_button.grid(row=4, column=1)
    # # back_button['command'] = lambda: some_callback5(mqtt_client, int(left_speed_entry.get()),int(right_speed_entry.get()))
    # # root.bind('<Down>',
    # #           lambda event: some_callback5(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))
    # # back_button and '<Down>' key
    #
    # up_button = ttk.Button(main_frame, text="Up")
    # up_button.grid(row=5, column=0)
    # up_button['command'] = lambda: send_up(mqtt_client)
    # root.bind('<u>', lambda event: send_up(mqtt_client))
    #
    # down_button = ttk.Button(main_frame, text="Down")
    # down_button.grid(row=6, column=0)
    # down_button['command'] = lambda: send_down(mqtt_client)
    # root.bind('<j>', lambda event: send_down(mqtt_client))
    #
    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=4, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))
    #
    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=4, column=0)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))
    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# TODO: 4. Implement the functions for the drive button callbacks.

# TODO: 5. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.  This is the final one!
#
# Observations you should make, you did basically this same program using the IR Remote, but your computer can be a
# remote control that can do A LOT more than an IR Remote.  We are just doing the basics here.
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

def radcall():
    radVar = tk.IntVar()
    radSel = radVar.get()




# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
