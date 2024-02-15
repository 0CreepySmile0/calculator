"""Container for Keypad class."""
import tkinter as tk


class Keypad(tk.Frame):
    """Keypad class used for creating keypad for calculator"""
    def __init__(self, parent, keynames=[], columns=1, **kwargs):
        super().__init__(parent, **kwargs)
        self.keynames = keynames
        self.init_components(columns)

    def init_components(self, columns) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        """
        if len(self.keynames) / columns != int(len(self.keynames) / columns):
            rows = len(self.keynames) // columns + 1
        else:
            rows = len(self.keynames) // columns
        for i in range(rows):
            self.rowconfigure(i, weight=1)
        for i in range(columns):
            self.columnconfigure(i, weight=1)
        self.button_list = {i: tk.Button(self, text=i) for i in self.keynames}
        col, row = 0, 0
        for i in self.button_list.values():
            i.grid(column=col, row=row, sticky=tk.NSEW, pady=2, padx=2)
            col += 1
            if col == columns:
                col = 0
                row += 1

    def bind_all_button(self, sequence, func):
        """Bind an event handler to an event sequence."""
        for i in self.button_list:
            self.button_list[i].bind(sequence, func)

    def bind(self, sequence, func, button_key):
        """Bind an event handler to specific button key."""
        self.button_list[button_key].bind(sequence, func)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.
        """
        for i in self.button_list.values():
            i[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        """
        return self.button_list[self.keynames[0]][key]

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons."""
        for i in self.button_list.values():
            i.configure(**kwargs)

    @property
    def frame(self):
        """Get frame object which is super class of this class."""
        return super()
