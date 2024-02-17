"""Container for string cleaner function class"""
from math import *


def replace_syntax(expression: str):
    """Replace all math symbol into syntax"""
    expression = expression.replace("^", "**")
    expression = expression.replace("mod", "%")
    expression = expression.replace("π", "pi")
    expression = expression.replace("ln", "log")
    expression = expression.replace("log₂", "log2")
    expression = expression.replace("log₁₀", "log10")
    return expression


def clean_zero(expression: str):
    """Get rid of leading zero"""
    num = ""
    simplified = ""
    for i in expression + " ":
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
    """Change the exclamation mark which mean factorial symbol in math into syntax"""
    num = ""
    temp = []
    for i in expression + " ":
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


def able_to_eval(expression):
    """Make string of math expression be able to eval"""
    expression = clean_zero(expression)
    expression = simplify_factorial(expression)
    expression = replace_syntax(expression)
    return expression
