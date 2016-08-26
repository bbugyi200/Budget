""" Renders a new window which prompts the user for limit information.
    The limit information is then updated accordingly.
"""

import tkinter as tk
from .constants import MONTH, fonts


class NewLimits(tk.Toplevel):
    def __init__(self, parent):
        self.parent = parent

    def Make(self):
        """ Creates a new GUI window that prompts the user for the new
        Budget information.
        """
        tk.Toplevel.__init__(self, master=self.parent)

        self.title(MONTH + ' - Limit Form')

        TopFrame = tk.Frame(self)
        TopFrame.grid(row=0)

        row = 0
        WindowTitle = tk.Label(TopFrame,
                               text="Spending Limits",
                               font=fonts.title())
        WindowTitle.grid(row=row, columnspan=5); row += 1

        WindowTitleBuffer = tk.Frame(TopFrame, height=10)
        WindowTitleBuffer.grid(row=row); row += 1

        TLimLabel = tk.Label(TopFrame, text="Total Limit: ")
        TLimLabel.grid(row=row)

        self.TLimEntry = tk.Entry(TopFrame)
        self.TLimEntry.grid(row=row, column=1); row += 1

        bottomFrame = tk.Frame(self)
        bottomFrame.grid(row=1, columnspan=5)

        # Adds space between submit button and top Entry boxes
        submitBuffer = tk.Frame(bottomFrame, height=10)
        submitBuffer.pack(side='top')

        submit_button = tk.Button(bottomFrame,
                                  text='Submit',
                                  command=self.Submit,
                                  font=fonts.button())
        submit_button.pack()

    def Submit(self):
        TotalLimit = self.TLimEntry.get()

        self.parent.Budget.updateLimits(TotalLimit)

        self.parent.refresh_screen()
        self.destroy()
