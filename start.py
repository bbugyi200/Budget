#!/usr/bin/python3

from IntelliBudget.GUI.main import BudgetGUI
import tkinter as tk

root = tk.Tk()

BG = BudgetGUI(root)
BG.pack()

root.mainloop()
