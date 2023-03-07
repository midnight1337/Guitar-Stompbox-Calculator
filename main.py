import abc
VCC: int = 9


class Bjt:
    def __init__(self, name, hfe, Rb, Rc, Re):
        self.name = name
        self.hfe = hfe
        self.Rb: float = Rb
        self.Rc: float = Rc
        self.Re: float = Re
        self.Vbe: float = 0.6
        self.Ib: float = ...
        self.Ic: float = ...
        self.Ie: float = ...
        self.Vb: float = ...
        self.Vc: float = ...
        self.Ve: float = ...
        self.Vrb: float = ...
        self.Vrc: float = ...
        self.Vre: float = ...
        self.Vce: float = ...
        self.Ic_max = ...
        self.Av = ...
        self.z_input = ...
        self.Q_point = ...
        self.documentation: dict = {}

    def get_documentation(self):
        self.documentation = {
            "Ib [uA]": self.Ib * 1000000,
            "Ic [mA]": self.Ic * 1000,
            "Ie [mA]": self.Ie * 1000,
            "Vb [V]": self.Vb,
            "Vc [V]": self.Vc,
            "Ve [V]": self.Ve,
            "Vce [V]": self.Vce,
            "Icmax [mA]": self.Ic_max * 1000,
            "Z_input[KOhm]": self.z_input / 1000,
            "Av [Gain[V]]": self.Av,
            "Qpoint": self.Q_point
        }
        for k, v in self.documentation.items():
            if k == "Qpoint":
                continue
            self.documentation[k] = round(v, 3)

        # self.documentation = {k: round(v, 3) for k, v in self.documentation.items()}
        return self.documentation

    def calculate(self):
        self.calcualte_base_current()
        self.calculate_collector_current()
        self.calculate_emitter_current()
        self.calculate_collector_voltage()
        self.calculate_emitter_volatge()
        self.calculate_base_voltage()
        self.calculate_collector_emitter_voltage()
        self.calculate_q_point()
        self.calculate_input_impedance()
        self.calculate_voltage_gain()

    def calcualte_base_current(self):
        self.Ib = ((VCC - self.Vbe) / (self.Rb + (self.hfe + 1)*(self.Rc + self.Re)))  # A to mA

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

    def calculate_collector_emitter_voltage(self):
        self.Vce = self.Vc - self.Ve

    def calculate_q_point(self):
        self.Ic_max = VCC / (self.Rc + self.Re)
        self.Q_point = (round(self.Vce, 3), round(self.Ic * 1000, 3), [VCC, round(self.Ic_max * 1000, 3)])

    def calculate_voltage_gain(self):
        internal_emitter_voltage_drop = 0.025
        re = internal_emitter_voltage_drop / self.Ie
        self.Av = self.Rc / (self.Re + re)

        # 2nd method
        gm = self.Ie / internal_emitter_voltage_drop
        gain = gm * self.Rc

    def calculate_input_impedance(self):
        # r_pi = Zin, not sure if calculating correct
        internal_emitter_voltage_drop = 0.025
        gm = self.Ie / internal_emitter_voltage_drop
        r_pi = ((self.hfe + 1) / gm)
        self.z_input = r_pi

        # 2nd method
        re = internal_emitter_voltage_drop / self.Ie
        z_in = self.hfe * (self.Re + re)


transistor = [
    {
        "name": "BC237",
        "hfe": 265
    },
    {
        "name": "BC107",
        "hfe": 200
    },
    {
        "name": "2N2222",
        "hfe": 60
    }
]

resistors = {
    "Rb": 410 * 10**3,
    "Rc": 47 * 10**3,
    "Re": 0.1 * 10**3
}

# Rb = 1M, Vc = 4.7
resistors_q1 = {
    "Rb": 1500 * 10**3,
    "Rc": 5.1 * 10**3,
    "Re": 0
}

q = Bjt(**transistor[2], **resistors)
q.calculate()
doc = q.get_documentation()
print(doc)

q1 = Bjt(**transistor[1], **resistors_q1)
q1.calculate()
doc = q1.get_documentation()
print(doc)
