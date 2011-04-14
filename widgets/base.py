from Tkinter import *

class Widget(object):
    def simulate(self):
        self.render(self.__class__.simulate_value())

    @classmethod
    def test(cls):
        class Application(Frame):
            def __init__(s, master=None):
                Frame.__init__(s, master)

                s.pack()
                s.create_widgets()

            def create_widgets(s):
                s.QUIT = Button(s)
                s.QUIT["text"] = "QUIT"
                s.QUIT["fg"]   = "red"
                s.QUIT["command"] =  s.quit

                s.QUIT.pack()

                s.app = cls(s, width=1024, height=512)
                s.app.pack(fill=X, expand=True)
                s.app.simulate()

        root = Tk()
        app = Application(master=root)
        app.mainloop()
        root.destroy()

