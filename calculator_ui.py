"""Container for user interface class"""
from math import *
import pygame
import tkinter as tk
from tkinter import ttk
from keypad import Keypad


class CalculatorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basic Calculator")
        self.init_component()

    def init_component(self):
        self.calculated = True
        font = {"font": ("Minecraft", 16)}
        option1 = {"column": 0, "row": 3, "columnspan": 2}
        option2 = {"column": 2, "row": 3}
        pad = {"padx": 2, "pady": 2}
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.display_text = tk.StringVar(value="0")
        self.display_list = []
        self.num_list = list("7894561230.")
        self.num_pad = Keypad(self, self.num_list, 3)
        self.num_pad.re_grid_button("0", **option1, **pad)
        self.num_pad.re_grid_button(".", **option2, **pad)
        self.operator_list = list("+-*/^") + ["mod", "="]
        self.operator_pad = Keypad(self, self.operator_list, 1)
        self.num_pad.configure(**font)
        self.operator_pad.configure(**font)
        self.display = tk.Label(self, bg="black", fg="yellow", **pad, height=4, **font,
                                textvariable=self.display_text, anchor="se")
        misc_list = ["AC", "(", ")", "DEL", "e", "π", "!", "sqrt", "ln", "log₂", "log₁₀"]
        self.misc_pad = Keypad(self, misc_list, 4)
        self.misc_pad.configure(**font)
        self.misc_pad.bind("<Button>",  self.button_handler, list("()eπ!"))
        self.misc_pad.bind("<Button>", self.clear_handler, ["AC"])
        self.misc_pad.bind("<Button>", self.del_handler, ["DEL"])
        self.misc_pad.bind("<Button>", self.func_handler, misc_list[-4:])
        self.num_pad.bind("<Button>", self.button_handler, self.num_list)
        self.operator_pad.bind("<Button>", self.button_handler, list("+-*/^") + ["mod"])
        self.operator_pad.bind("<Button>", self.calculate_handler, ["="])
        self.display.grid(column=0, row=0, columnspan=self.winfo_screenwidth(),
                          sticky="nsew")
        self.misc_pad.grid(column=0, row=1, sticky="nsew", columnspan=self.winfo_screenwidth())
        self.num_pad.grid(column=0, row=2, sticky="nsew")
        self.operator_pad.grid(column=1, row=2, sticky="nsew")

    def clear_handler(self, event):
        self.display["fg"] = "yellow"
        self.calculated = True
        self.display_text.set("0")
        self.display_list.clear()

    def del_handler(self, event):
        self.display["fg"] = "yellow"
        if self.calculated:
            self.display_text.set("0")
            self.display_list.clear()
        else:
            current = self.display_text.get()
            if self.display_list:
                if current[-(len(self.display_list[-1])):] == self.display_list[-1]:
                    self.display_text.set(current[:-(len(self.display_list[-1]))])
                    self.display_list.pop(-1)
                    if not self.display_list:
                        self.display_text.set("0")
            else:
                self.display_text.set("0")

    def func_handler(self, event):
        user_input = event.widget["text"]
        current = self.display_text.get()
        self.display["fg"] = "yellow"
        if self.calculated:
            self.calculated = False
        if current == "0":
            current = f"{user_input}("
            self.display_list.append(f"{user_input}(")
        elif current[-1] in self.operator_list:
            current += f"{user_input}("
            self.display_list.append(f"{user_input}(")
        else:
            current += f"*{user_input}("
            self.display_list.append(f"*{user_input}(")
        self.display_text.set(current)

    def button_handler(self, event):
        user_input = event.widget["text"]
        current = self.display_text.get()
        self.display["fg"] = "yellow"
        if current == "0":
            if user_input in self.operator_list + [".", "!"]:
                current += user_input
                self.display_list.append(user_input)
            elif user_input in list("(eπ"):
                user_input = f"*{user_input}"
                current += user_input
                self.display_list.append(user_input)
            else:
                current = user_input
                self.display_list.clear()
                self.display_list.append(user_input)
        elif float(current) < 0:
            if self.calculated:
                if user_input in self.operator_list + [".", "!"]:
                    current += user_input
                    self.display_list.append(user_input)
                elif user_input in list("(eπ"):
                    user_input = f"*{user_input}"
                    current += user_input
                    self.display_list.append(user_input)

    def calculate_handler(self, *args):
        try:
            if self.calculated:
                pass
            else:
                expression = self.display_text.get()
                expression = replace_syntax(simplify_factorial(clean(expression)))
                ans = eval(expression)
                self.display_list.clear()
                if ans == int(ans):
                    ans = int(ans)
                    self.display_text.set(str(ans))
                    self.display_list.extend(list(str(ans)))
                else:
                    self.display_text.set(f"{ans:.8g}")
                    self.display_list.extend(list(f"{ans:.8g}"))
                self.calculated = True
        except:
            self.display["fg"] = "red"
            pygame.mixer.init()
            pygame.mixer.music.load("illuminati.mp3")
            pygame.mixer.music.play()

    def run(self):
        self.mainloop()


def replace_syntax(expression: str):
    expression = expression.replace("^", "**")
    expression = expression.replace("mod", "%")
    expression = expression.replace("e", "exp(1)")
    expression = expression.replace("π", "pi")
    expression = expression.replace("ln", "log")
    expression = expression.replace("log₂", "log2")
    expression = expression.replace("log₁₀", "log10")
    return expression


def clean(expression: str):
    num = ""
    simplified = ""
    for i in expression+" ":
        if i.isnumeric() or i == ".":
            num += i
        else:
            if "." in num:
                num = f"{float(num):f}"
            else:
                try:
                    num = str(int(num))
                except:
                    pass
            simplified += num
            simplified += i
            num = ""
    return simplified[:-1]


def simplify_factorial(expression: str):
    num = ""
    temp = []
    for i in expression+" ":
        if i.isnumeric() or i == ".":
            num += i
        else:
            if i == "!":
                num += i
            temp.append(num)
            num = ""
    for i in temp:
        if "!" in i:
            expression = expression.replace(i, f"factorial({i[:-1]})")
    return expression
