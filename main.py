from tkinter import *
from tkinter import ttk
import sv_ttk

from view.application import Application

sv_ttk.set_theme("dark")
app = Application()
app.master.title('Captain Log')
app.mainloop() 