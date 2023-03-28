"""
Description: this class do all calculations, for Voltage Divider Bias.
"""


class VoltageDivider(object):
    def __init__(self, transistor: 'Bjt', rbc: float, rbe: float, rc: float, re: float, vcc: int = 9):
        self.transistor: 'Bjt' = transistor
        self.Rbc: float = rbc
        self.Rbe: float = rbe
        self.Rc: float = rc
        self.Re: float = re
        self.Vcc: int = vcc
        self.documentation: dict = {}

    def __str__(self):
        return f"Voltage Divider"

    def read_documentation(self):
        print(f"Voltage Divider:\n", self.documentation)

    def write_documentation(self, ib: float):
        self.documentation = {
            "Transistor": self.transistor,
            "Ib [uA]": ib * 1000000
        }

        for k, v in self.documentation.items():
            if k == "Qpoint" or type(v) is type(self.transistor):
                continue
            self.documentation[k] = round(v, 3)

    def calculate(self):
        Ib = self.calculate_base_current()
        self.write_documentation(ib=Ib)

    def calcualte_base_resistance(self):
        Rb = (self.Rbe * self.Rbc) / (self.Rbe + self.Rbc)
        print(Rb)

    def calculate_base_current(self):
        numerator = (self.Vcc * (self.Rbe / (self.Rbe + self.Rbc)) - self.transistor.vbe)
        denominator = (((self.Rbe * self.Rbc) / (self.Rbe + self.Rbc)) + self.Re * (self.transistor.hfe + 1))
        return numerator / denominator
