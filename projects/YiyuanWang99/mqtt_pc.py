
import tkinter as tk
from tkinter import ttk
import ev3dev.ev3 as ev3
import time
from PIL import Image
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

    photo = tk.PhotoImage(file="C:\CSSE120\PyCharm2\ev3dev-curriculum\examples\lovelydraw.gif")

    # background = tk.PhotoImage(file="C:\CSSE120\PyCharm2\ev3dev-curriculum\examples\jiang.PNG")

    check_state1 = tk.IntVar()
    check_state2 = tk.IntVar()
    check_state3 = tk.IntVar()

    main_frame = ttk.Frame(root, padding=50, relief='raised')
    main_frame.grid()

    ro_lable = ttk.Label(main_frame,text="I'm not a robot Bob")
    ro_lable.grid(row=2,column=0)

    entry_box = ttk.Entry(main_frame, width=10, justify=tk.RIGHT)
    entry_box.insert(0,'')
    entry_box.grid(row=2,column=1)


    photo_lable = ttk.Label(main_frame,imag=photo)
    photo_lable.grid(row=2,column=2)

    # background_lable = ttk.Label(main_frame,justify=tk.LEFT,image=background,compound=tk.CENTER)
    # background_lable.grid()

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

    confirm_button = ttk.Button(main_frame, text="Confirm")
    confirm_button.grid(row=4, column=1)
    confirm_button['command'] = (lambda : some_callback1(mqtt_client, int(entry_box.get()),int(check_state1.get()), int(check_state2.get()),int(check_state3.get())))

    answer_lable = ttk.Label(main_frame, text=" ")
    answer_lable.grid(row=5, column=0)

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=6, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))
    #
    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=0)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))
    root.mainloop()


def some_callback1(mqtt_client,code1,state1,state2,state3):
        print('Message send')
        mqtt_client.send_message('find_the_target',[code1,state1,state2,state3])

# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()






# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
