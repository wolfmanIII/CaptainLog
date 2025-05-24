import tkinter
from tkinter import ttk
import sv_ttk

class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = ttk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

sv_ttk.set_theme("dark")
app = Application()
app.master.title('Sample application')
app.mainloop() 