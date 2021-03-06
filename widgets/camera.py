from Tkinter import *
from random import randint

from base import Widget

class CameraFrame(Widget, Canvas):
    def __init__(self, parent=None, num_tiles=128, *args, **kwargs):
        Widget.__init__(self)
        Canvas.__init__(self, parent, borderwidth=0, *args, **kwargs)

        self.num_tiles = num_tiles
        self.items = []

    @staticmethod
    def simulate_value():
        return [randint(0, 255) for i in range(0, 128)]

    def render(self, values):
        """
        value is a list of 128 pixel values.
        """
        
        self.delete(self.items)
        self.items = []

        PAD = 0

        width = (int(self.cget('width')) / float(self.num_tiles)) - 2 * PAD
        height = int(self.cget('height')) - 2 * PAD

        for i, value in enumerate(values):
#            value = scale(value)

            fill = "#%02x%02x%02x" % (value, value, value)

            opts = {
                'fill': fill,
                'outline': fill
            }

            id = self.create_rectangle(int(i * width), PAD, int((i + 1) * width), PAD + height, **opts)
            self.items.append(id)

class CameraStack(Widget, Frame):
    def __init__(self, parent=None, num_tiles=128, num_frames=64, *args, **kwargs):
        Widget.__init__(self)
        Frame.__init__(self, parent, *args, **kwargs)

        self.num_frames = num_frames
        self.num_tiles = num_tiles
        self.frames = {}

    def _create_frame(self, pos):
        height = int(self.cget('height')) / self.num_frames
        
        widget = CameraFrame(self, num_tiles=self.num_tiles, width=self.cget('width'), height=height)
        widget.grid(row=pos)
        
        return widget

    def render(self, pos, values):
        if pos not in self.frames:
            self.frames[pos] = self._create_frame(pos)

        self.frames[pos].render(values)

    def simulate(self):
        for i in range(0, self.num_frames):
            self.render(i, CameraFrame.simulate_value()) 

if __name__ == "__main__":
    CameraStack.test()
