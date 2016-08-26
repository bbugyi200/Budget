""" Renders a new window which prompts the user for limit information.
    The limit information is then updated accordingly.
"""

import tkinter as tk
from .constants import MONTH, fonts, Field, addBuffer


class NewLimits(tk.Toplevel):
    def __init__(self, parent):
        self.parent = parent

    def Make(self):
        """ Creates a new GUI window that prompts the user for the new
        Budget information.
        """
        tk.Toplevel.__init__(self, master=self.parent)

        self.title(MONTH + ' - Limit Form')

        topFrame = tk.Frame(self)
        topFrame.pack(side='top')

        WindowTitle = tk.Label(topFrame,
                               text="Spending Limits",
                               font=fonts.title())
        WindowTitle.pack(side='top')

        addBuffer(topFrame, side='top', height=10)

        FormField = tk.Frame(topFrame)
        FormField.pack(side='top')
        FormField.row = 0

        self.TotalLimit = Field()
        self.TotalLimit.label = tk.Label(FormField, text="Total Limit: ")
        self.TotalLimit.label.grid(row=FormField.row, column=0)
        self.TotalLimit.entry = tk.Entry(FormField)
        self.TotalLimit.entry.grid(row=FormField.row, column=1)
        FormField.row += 1

        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side='top')

        addBuffer(bottomFrame, side='top', height=10)

        SubmitButton = tk.Button(bottomFrame,
                                  text='Submit',
                                  command=self.Submit,
                                  font=fonts.button())
        SubmitButton.pack(side='top')

    def Submit(self):
        TotalLimit = self.TotalLimit.entry.get()

        self.parent.Budget.updateLimits(TotalLimit)

        self.parent.refresh_screen()
        self.destroy()
