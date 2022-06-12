import quake
import tkinter as tk
from tkinter import ttk
from ctypes import windll

def test():
    pass
windll.shcore.SetProcessDpiAwareness(1)

mainWindow=tk.Tk()
mainWindow.title('Taiwan Earthquake Analysis')

window_width = 500
window_height = 500

screen_width = mainWindow.winfo_screenwidth()
screen_height = mainWindow.winfo_screenheight()

center_x = int(screen_width/2 - window_width /2)
center_y = int(screen_height/2 - window_height /2)


view_recent = ttk.Button(mainWindow, text='View Recent', command=test)
query_specific_date = ttk.Button(mainWindow, text='Query speific date')
view_recent.pack(ipadx=100)
query_specific_date.pack()
mainWindow.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
mainWindow.mainloop()


