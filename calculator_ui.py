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
        self.rowconfigure(2, weight=2)
        menubar = tk.Menu(self)
        self.history = tk.Menu(menubar, tearoff=False)
        self.history.configure(**font)
        self.history_expression = []
        self.history_ans = []
        menubar.add_cascade(label="History", menu=self.history, **font)
        self.config(menu=menubar)
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
        self.misc_pad.re_grid_button("log₁₀", column=2, row=2, columnspan=2, **pad)
        self.misc_pad.configure(**font)
        self.misc_pad.bind("<Button>",  self.func_handler, list("(eπ"))
        self.misc_pad.bind("<Button>", self.clear_handler, ["AC"])
        self.misc_pad.bind("<Button>", self.del_handler, ["DEL"])
        self.misc_pad.bind("<Button>", self.func_handler, misc_list[-4:])
        self.misc_pad.bind("<Button>", self.operator_handler, ["!"])
        self.misc_pad.bind("<Button>", self.num_handler, [")"])
        self.num_pad.bind("<Button>", self.num_handler, self.num_list[:-1])
        self.num_pad.bind("<Button>", self.operator_handler, ["."])
        self.operator_pad.bind("<Button>", self.operator_handler, list("+-*/^") + ["mod"])
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
        if self.calculated or current == "0":
            self.calculated = False
            self.display_list.clear()
            if user_input in list("(eπ"):
                current = user_input
                self.display_list.append(user_input)
            else:
                current = f"{user_input}("
                self.display_list.append(f"{user_input}(")
        else:
            if current[-1] == ".":
                pass
            elif current[-1].isnumeric() or current[-1] == "!":
                if user_input in list("(eπ"):
                    current += f"*{user_input}"
                    self.display_list.append(f"*{user_input}")
                else:
                    current += f"*{user_input}("
                    self.display_list.append(f"*{user_input}(")
            else:
                if user_input in list("(eπ"):
                    current += user_input
                    self.display_list.append(user_input)
                else:
                    current += f"*{user_input}("
                    self.display_list.append(f"*{user_input}(")
        self.display_text.set(current)

    def num_handler(self, event):
        user_input = event.widget["text"]
        current = self.display_text.get()
        self.display["fg"] = "yellow"
        if self.calculated:
            self.calculated = False
            self.display_list.clear()
            current = user_input
            if not user_input == "0":
                self.display_list.append(user_input)
        else:
            if user_input == "0":
                if current == "0":
                    current = user_input
                else:
                    current += user_input
                    self.display_list.append(user_input)
            else:
                if current == "0":
                    current = user_input
                    self.display_list.append(user_input)
                elif current[-1] == "!":
                    current += f"*{user_input}"
                    self.display_list.append(f"*{user_input}")
                else:
                    current += user_input
                    self.display_list.append(user_input)
        self.display_text.set(current)

    def operator_handler(self, event):
        user_input = event.widget["text"]
        current = self.display_text.get()
        self.display["fg"] = "yellow"
        if self.calculated:
            self.calculated = False
            current += user_input
            self.display_list.append(user_input)
        else:
            if current[-1] == "!":
                if user_input in "!.":
                    pass
                else:
                    current += user_input
                    self.display_list.append(user_input)
            elif current[-1] in list("+-*/^.") + ["mod"]:
                pass
            elif current[-1] == "(":
                if user_input in list("+-."):
                    current += user_input
                    self.display_list.append(user_input)
                else:
                    pass
            else:
                current += user_input
                self.display_list.append(user_input)
        self.display_text.set(current)

    def calculate_handler(self, *args):
        try:
            if self.calculated:
                pass
            else:
                self.calculated = True
                expression = self.display_text.get()
                math_expression = clean_zero(expression)
                expression = replace_syntax(simplify_factorial(clean_zero(expression)))
                ans = eval(expression)
                self.display_list.clear()
                if ans == int(ans):
                    ans = int(ans)
                    ans = str(ans)
                else:
                    ans = f"{ans:.10g}"
                self.display_text.set(ans)
                self.display_list.extend(list(ans))
                history = f"{math_expression:<30} {'=':<} {ans}"
                self.history_expression = [history] + self.history_expression
                self.history_ans = [math_expression] + self.history_ans
                if len(self.history_ans) > 5:
                    self.history_ans.pop(-1)
                    self.history_expression.pop(-1)
                self.history.delete(0, len(self.history_ans)-1)
                for i in range(len(self.history_ans)):
                    self.history.add_command(label=self.history_expression[i],
                                             command=lambda x=self.history_ans[i]:
                                             self.history_handler(x), foreground="blue")
        except:
            self.display["fg"] = "red"
            self.calculated = False
            pygame.mixer.init()
            pygame.mixer.music.load("illuminati.mp3")
            pygame.mixer.music.play()

    def history_handler(self, history):
        current = self.display_text.get()
        result = history
        if self.calculated:
            self.calculated = False
            current = result
            self.display_list.clear()
        else:
            if current == "0":
                current = result
                self.display_list.clear()
            else:
                current += result
        self.display_list.append(result)
        self.display_text.set(current)

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


def clean_zero(expression: str):
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
