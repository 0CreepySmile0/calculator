"""Container for string cleaner function class"""
from math import *


class ExpressionCleaner:
    """Class that contain useful method to convert string of mathematical format
    into evaluable syntax.
    """
    @staticmethod
    def replace_syntax(expression: str) -> str:
        """Replace all math symbol into syntax"""
        expression = expression.replace("^", "**")
        expression = expression.replace("mod", "%")
        expression = expression.replace("π", "pi")
        expression = expression.replace("ln", "log")
        expression = expression.replace("log₂", "log2")
        expression = expression.replace("log₁₀", "log10")
        return expression

    @staticmethod
    def clean_zero(expression: str) -> str:
        """Get rid of leading zero"""
        num = ""
        simplified = ""
        for i in expression + " ":
            if i.isnumeric() or i == ".":
                num += i
            else:
                if "." in num:
                    num = f"{float(num)}"
                else:
                    try:
                        num = str(int(num))
                    except:
                        pass
                simplified += num
                simplified += i
                num = ""
        return simplified[:-1]

    @staticmethod
    def simplify_factorial(expression: str) -> str:
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

    @classmethod
    def able_to_eval(cls, expression: str) -> str:
        """Make string of math expression be able to eval"""
        expression = cls.clean_zero(expression)
        expression = cls.simplify_factorial(expression)
        expression = cls.replace_syntax(expression)
        return expression
