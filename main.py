import abc
VCC: int = 9


class Bjt:
    def __init__(self, name, hfe):
        self.name = name
        self.hfe = hfe
        self.Rb: float = 3300
        self.Rc: float = 13
        self.Re: float = 0
        self.Ib: float = ...
        self.Ic: float = ...
        self.Ie: float = ...
        self.Vb: float = ...
        self.Vc: float = ...
        self.Ve: float = ...
        self.Vrb: float = ...
        self.Vrc: float = ...
        self.Vre: float = ...
        self.Vbe: float = 0.7
        self.Vce: float = ...
        self.q_point: set = ...
        self.gain_value = ...

    def get_documentation(self):
        documentation = [
            ("Ib[mA]", self.Ib),
            ("Ic", self.Ic),
            ("Ie", self.Ie),
            ("Vb", self.Vb),
            ("Vc", self.Vc),
            ("Ve", self.Ve),
            ("Vce", self.Vce),
            ("Qpoint", self.q_point)
        ]
        print(documentation)
        return documentation

    def calculate(self):
        self.calcualte_base_current()
        self.calculate_collector_current()
        self.calculate_emitter_current()
        self.calculate_collector_voltage()
        self.calculate_emitter_volatge()
        self.calculate_base_voltage()
        self.calculate_collector_emitter_voltage()
        self.calculate_q_point()

    def calcualte_base_current(self):
        self.Ib = ((VCC - self.Vbe)/(self.Rb + (self.hfe + 1)*(self.Rc + self.Re))) #* 1000  # mA to uA
        self.Ib = round(self.Ib, 6)

    def calculate_collector_current(self):
        self.Ic = self.Ib * self.hfe

    def calculate_emitter_current(self):
        self.Ie = self.Ic + self.Ib

    def calculate_base_voltage(self):
        self.Vb = self.Ve + self.Vbe

    def calculate_collector_voltage(self):
        self.Vrc = self.Ic * self.Rc
        self.Vc = VCC - self.Vrc

    def calculate_emitter_volatge(self):
        self.Ve = self.Ie * self.Re
        self.Ve = round(self.Ve, 2)

    def calculate_collector_emitter_voltage(self):
        self.Vce = self.Vc - self.Ve
        self.Vce = round(self.Vce, 2)

    def calculate_q_point(self):
        Ic_max = VCC / (self.Rc + self.Re)      # (Vce, Ic)
        self.q_point = (self.Vce, self.Ic)


q1 = Bjt(name="MPS374", hfe=300)
q1.calculate()
q1.get_documentation()
