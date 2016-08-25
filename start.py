#!/usr/bin/python3.4

from IntelliBudget.GUI.main import Main
import tkinter as tk

root = tk.Tk()

M = Main(root)
M.pack(side='top', fill='both', expand=True)

root.mainloop()
