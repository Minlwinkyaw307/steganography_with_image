from tkinter import *
from tkinter import ttk

import tkinter as tk

class Home(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('500x500')
        self.grid()
        # self.pack()
        self.create_widgets()
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=3)


    def create_widgets(self):
        self.image_location_label = tk.Label(self, text='File Location')
        self.image_location_label.grid(row=0, column=0)

        self.image_location_entry = tk.Entry(self)
        self.image_location_entry.grid(row=0, column=1)


        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")
        #
        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=self.master.destroy)
        # self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Home(master=root)
app.mainloop()