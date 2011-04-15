from Tkinter import *

from connection import serial_connection

from widgets.angle import *
from widgets.camera import *

WIDTH = 1200
HEIGHT = 512

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.grid()
        self.create_widgets()

    def create(self, cls, label, row, col, width, height, **kwargs):
        cell_width = WIDTH / 12
        cell_height = HEIGHT / 8

        act_width = cell_width * width
        act_height = cell_height * height

        frame = Frame(self)
        frame.grid(row=row, column=col, rowspan=height, columnspan=width)

        lbl = Label(frame, text=label)
        lbl.grid()

        obj = cls(frame, width=act_width, height=act_height, **kwargs)
        obj.grid()
        obj.simulate()

        return obj

    def create_widgets(self):
        self.hist_stack = self.create(CameraStack, "Camera Stack", 0, 0, 4, 7)
        self.cur_frame = self.create(CameraFrame, "Current Camera Image", 7, 0, 8, 1)
        self.cam_angle = self.create(Angle, "Camera Angle Target", 0, 4, 2, 2)

        self.wheel_angle = self.create(MultiAngle, "Wheel Angle / Target", 2, 4, 2, 2)
        self.batt_voltage = self.create(Angle, "Batt Voltage", 4, 4, 2, 2, max_val=8000)

        self.motor_current = self.create(Angle, "Motor Current", 0, 6, 2, 2, max_val=5000)
        self.motor_power = self.create(Angle, "Power", 2, 6, 2, 2, max_val=256)
        self.speed = self.create(Angle, "Speed", 4, 6, 2, 2, max_val=300)

        self.hist_line = self.create(CameraStack, "Line Sensor Stack", 0, 8, 4, 7, num_tiles=8)
        self.cur_line = self.create(CameraFrame, "Line Sensor Image", 7, 8, 4, 1, num_tiles=8)


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

