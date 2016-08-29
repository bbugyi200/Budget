""" Renders a new window which prompts the user for limit information.
    The limit information is then updated accordingly.
"""

import tkinter as tk
from .constants import fonts, Field, addBuffer


class NewLimits(tk.Toplevel):
    def __init__(self, parent):
        self.parent = parent

    def Make(self):
        """ Creates a new GUI window that prompts the user for the new
        Budget information.
        """
        tk.Toplevel.__init__(self, master=self.parent)

        self.title(self.parent.MONTH + ' - Limit Form')

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

        # Creates a Entry field for each expense type in the database
        self.dynamic_limits = []
        for etype in self.parent.Budget.getExpenseTypes():
            DynLimit = Field()
            text = ''.join([etype, ': '])

            DynLimit.label = tk.Label(FormField, text=text)
            DynLimit.label.grid(row=FormField.row, column=0)
            DynLimit.entry = tk.Entry(FormField)
            DynLimit.entry.grid(row=FormField.row, column=1)
            FormField.row += 1

            self.dynamic_limits.append((etype, DynLimit.entry))


        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side='top')

        addBuffer(bottomFrame, side='top', height=10)

        SubmitButton = tk.Button(bottomFrame,
                                 text='Submit',
                                 command=self.Submit,
                                 font=fonts.button())
        SubmitButton.pack(side='top')

    def Submit(self):
        for etype, entry in self.dynamic_limits:
            value = entry.get()

            self.parent.Budget.updateLimits(value, etype)

        self.parent.refresh_screen()
        self.destroy()
