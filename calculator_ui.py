"""Container for user interface class"""
from math import *
import tkinter as tk
from tkinter import ttk
from keypad import Keypad


class CalculatorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basic Calculator")
        self.init_component()

    def init_component(self):
        self.state = False
        option = {"font": ("Minecraft", 16)}
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.display_text = tk.StringVar()
        self.num_pad = Keypad(self, list("789456123 0."), 3)
        self.operator_pad = Keypad(self, list("+-*/^") + ["mod", "="], 1)
        self.num_pad.configure(**option)
        self.operator_pad.configure(**option)
        self.display = tk.Label(self, anchor="se", bg="black", fg="yellow", padx=2, pady=2,
                                textvariable=self.display_text, height=4, **option)
        self.num_pad.bind_all_button("<Button>", self.button_handler)
        self.operator_pad.bind_all_button("<Button>", self.button_handler)
        self.operator_pad.bind("<Button>", self.calculate_handler, "=")
        self.display.grid(column=0, row=0, columnspan=self.winfo_screenwidth(),
                          sticky="nsew")
        self.num_pad.grid(column=0, row=1, sticky="nsew")
        self.operator_pad.grid(column=1, row=1, sticky="nsew")

    def button_handler(self, event):
        user_input = event.widget["text"]
        current = self.display_text.get()
        current += user_input
        self.display_text.set(current)

    def calculate_handler(self, *args):
        expression = self.display_text.get()
        expression = expression.replace("^", "**")
        expression = expression.replace("mod", "%")
        self.display_text.set(str(eval(expression)))

    def run(self):
        self.mainloop()
