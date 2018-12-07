from pyfirmata import Arduino, util
import time
import Tkinter

# Set up the board
print "Initializing Arduino..."
board = Arduino('COM5')

# Iterator thread helps serial buffer not overflow
iter = util.Iterator(board)
iter.start()



#pin13 = board.get_pin('d:13:o')
claw = board.get_pin('d:6:s') # D9 pin as servo.  Claw Servo Green
left_arm = board.get_pin('d:9:s')  #  Left Arm Servo Yellow
right_arm = board.get_pin('d:10:s')  # Right Arm Servo Blue
base = board.get_pin('d:11:s')  # Base Servo Red
pin5 = board.get_pin('d:5:s')

def init_robot():
    claw.write(90)
    left_arm.write(115)
    right_arm.write(130)
    base.write(0)
    pin5.write(90)




def close_claw():
    print "Closing the Claw"
    claw.write(0)
    time.sleep(.5)
    pin5.write(90)
def open_claw():
    print "Opening the Claw"
    claw.write(90) #  Avoid going above 90, servo will whine
    time.sleep(.5)
def draw_card():
    init_robot()
    pin5.write(0)
    time.sleep(.5)
    right_arm.write(70)
    close_claw()
    right_arm.write(130)

def rotate_base(a):
    print "Slider location: ", (rotate.get())
    base.write(a)
def lift(a):
    left_arm.write(a)
def reach(a):
    right_arm.write(a)
def loc1():
    print "Drawing Card (soon)"
    base.write(20)
    time.sleep(.5)
    right_arm.write(90)
    time.sleep(.5)
    left_arm.write(65)
    time.sleep(.8)
def loc2():
    base.write(55)
    time.sleep(.5)
    right_arm.write(85)
    time.sleep(.5)
    left_arm.write(65)
    time.sleep(.5)
def loc3():
    base.write(90)
    time.sleep(.5)
    right_arm.write(85)
    time.sleep(.5)
    left_arm.write(65)
    time.sleep(.5)
def loc4():
    base.write(110)
    time.sleep(.5)
    right_arm.write(90)
    time.sleep(.5)
    left_arm.write(65)
    time.sleep(.5)
def loc5():
    base.write(155)
    time.sleep(.5)
    right_arm.write(100)
    time.sleep(.5)
    left_arm.write(70)
    time.sleep(.5)
def loc6():
    base.write(180)
    time.sleep(.5)
    right_arm.write(100)
    time.sleep(.5)
    left_arm.write(70)
    time.sleep(.5)

    
def place_in_loc1():
    loc1()
    open_claw()
    init_robot()
def place_in_loc2():
    loc2()
    open_claw()
    init_robot()
def place_in_loc3():
    loc3()
    open_claw()
    init_robot()
def place_in_loc4():
    loc4()
    open_claw()
    init_robot()
    return
def place_in_loc5():
    loc5()
    open_claw()
    init_robot()
    return
def place_in_loc6():
    loc6()
    open_claw()
    init_robot()


if __name__ == '__main__':
    # Let Arduino set up
    time.sleep(1)
    print "Ready!"
    window = Tkinter.Tk()
    frame = Tkinter.Frame(window)
    frame.pack()

    rotate = Tkinter.Scale(window, from_=0, to=180, orient=Tkinter.HORIZONTAL, command=rotate_base)  # Right arm servo can't recover at 180
    rotate.set(90)
    rotate.pack()

    lift = Tkinter.Scale(window, from_=0, to=130, orient=Tkinter.HORIZONTAL, command=lift)
    lift.set(90)
    lift.pack()

    reach = Tkinter.Scale(window, from_=0, to=130, orient=Tkinter.HORIZONTAL, command=reach)
    reach.set(90)
    reach.pack()

    Button = Tkinter.Button

    btn0 = Button(frame, text="OPEN ", command=open_claw)
    btn0.pack(side=Tkinter.LEFT)

    btn1 = Button(frame, text="CLOSE", command=close_claw)
    btn1.pack(side=Tkinter.LEFT)

    btn2 = Button(frame, text="LOC1", command=place_in_loc1)
    btn2.pack(side=Tkinter.BOTTOM)

    btn3 = Button(frame, text="LOC2", command=place_in_loc2)
    btn3.pack(side=Tkinter.BOTTOM)

    btn4 = Button(frame, text="LOC3", command=place_in_loc3)
    btn4.pack(side=Tkinter.BOTTOM)

    btn5 = Button(frame, text="LOC4", command=place_in_loc4)
    btn5.pack(side=Tkinter.BOTTOM)

    btn6 = Button(frame, text="LOC5", command=place_in_loc5)
    btn6.pack(side = Tkinter.BOTTOM)

    btn7 = Button(frame, text="LOC6", command=place_in_loc6)
    btn7.pack(side=Tkinter.BOTTOM)

    window.mainloop()



