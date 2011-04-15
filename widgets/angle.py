from Tkinter import *
from random import randint
import math

from base import Widget

class Angle(Widget, Canvas):
    def __init__(self, parent=None, max_val=180, *args, **kwargs):
        Widget.__init__(self)
        Canvas.__init__(self, parent, borderwidth=0, *args, **kwargs)

        self.line = None
        self.label = None
        self.max_val = max_val
        self.color = 'black'
        self.text_margin_bottom = 20

        self.size = min(int(self.cget('width')), int(self.cget('height')))
        self.create_arc(0, 0, self.size, self.size * 2, extent=180, fill='white')

    @staticmethod
    def simulate_value():
        return randint(0, 180)

    def render(self, value):
        """
        value is an angle from 0 to 179
        """
        if self.line:
            self.delete(self.line)
        if self.label:
            self.delete(self.label)

        self.create_text(self.size / 2, self.size - self.text_margin_bottom, font='arial 20 bold', text=str(value), fill=self.color)

        value = int(value * (180 / float(self.max_val)))

        x = self.size / 2 + math.cos(math.radians(180 - value)) * (self.size / 2)
        y = self.size - math.sin(math.radians(value)) * self.size

        self.line = self.create_line(self.size / 2, self.size, x, y, width=3, fill=self.color)

class MultiAngle(Angle):
    def __init__(self, *args, **kwargs):
        self.lines = {}

        self.colors = {
            0: 'black',
            1: 'red'
        }

        Angle.__init__(self, *args, **kwargs)

    def simulate(self):
        for i in range(0, 2):
            self.render(i, Angle.simulate_value())

    def render(self, index, value):
        self.line = self.lines.get(index, None)
        self.color = self.colors.get(index, 'black')
        self.text_margin_bottom = 25 * (index + 1)

        Angle.render(self, value)

if __name__ == '__main__':
    MultiAngle.test()
