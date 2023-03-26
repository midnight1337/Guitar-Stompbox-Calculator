from bjt import Bjt
from transistor import Transistor
VCC = 12


class VDBias:
    def __init__(self, rc, re, rb_1, rb_2):
        self.Rc = rc
        self.Rb_eqv = None
        self.Re = re
        self.Rb_1 = rb_1
        self.Rb_2 = rb_2
        self.Ic = None
        self.Ib = None
        self.Ie = None
        self.Vc = None
        self.Vb = None
        self.Ve = None
        self.Vce = None
        self.z_in = None
        self.Ic_max = None
        self.Av = None

    def calculate(self):
        self.calculate_equivalent_base_resistance()
        self.calculate_base_voltage()
        self.calculate_base_current()
        self.calculate_collector_current()
        self.calculate_emitter_current()
        self.calculate_collector_voltage()
        self.calculate_emitter_voltage()
        self.calculate_bias_voltage()
        self.calculate_voltage_gain()
        self.calculate_input_impedance()

    def setup_documentation(self):
        documentation = {
            "Ib [uA]": self.Ib * 1000000,
            "Ic [mA]": self.Ic * 1000,
            "Ie [mA]": self.Ie * 1000,
            "Vc [V]": self.Vc,
            "Vb [V]": self.Vb,
            "Ve [V]": self.Ve,
            "Vce [V]": self.Vce,
            "Av [Gain]": self.Av,
            "Zin [K Ohm]": self.z_in / 1000
        }
        documentation = {k: round(v, 3) for k, v in documentation.items() if k != "Qpoint"}
        print(documentation)

    def calculate_equivalent_base_resistance(self):
        self.Rb_eqv = (self.Rb_1 * self.Rb_2) / (self.Rb_1 + self.Rb_2)

    def calculate_base_voltage(self):
        # self.Vb = (VCC * self.Rb_2 / (self.Rb_1 + self.Rb_2))
        # self.Vb = bjt.Vbe + (bjt.hfe + 1) * self.Ib * self.Re
        self.Vb = self.Ve + bjt.Vbe

    def calculate_collector_voltage(self):
        self.Vc = VCC - (self.Ic * self.Rc)

    def calculate_emitter_voltage(self):
        self.Ve = self.Re * self.Ie

    def calculate_base_current(self):
        self.Ib = (self.Vb - bjt.Vbe) / (self.Rb_eqv + (self.Re * (bjt.hfe + 1)))

    def calculate_collector_current(self):
        self.Ic = self.Ib * bjt.hfe

    def calculate_emitter_current(self):
        # self.Ie = (bjt.hfe + 1) * self.Ib

        self.Ie = (self.Vb - bjt.Vbe) / ((self.Rb_eqv / (bjt.hfe + 1)) + self.Re)

    def calculate_voltage_gain(self):
        # re - emitter resistance
        internal_emitter_voltage_drop = 0.025
        re = internal_emitter_voltage_drop / self.Ie
        self.Av = self.Rc / (self.Re + re)

        # 2nd method
        gm = self.Ie / internal_emitter_voltage_drop
        Gv = gm * self.Rc

    def calculate_input_impedance(self):
        # 1nd has mistake somewhere
        internal_emitter_voltage_drop = 0.025
        gm = self.Ie / internal_emitter_voltage_drop
        re = internal_emitter_voltage_drop / self.Ie
        r1 = self.Rb_eqv
        r2 = ((bjt.hfe + 1) * (self.Re + re))
        self.z_in = self.calculate_resistor_in_parallel(r1=r1, r2=r2)

        # 2nd method
        r1 = self.Rb_eqv
        r_pi = bjt.hfe / gm
        self.z_in = self.calculate_resistor_in_parallel(r1=r1, r2=r_pi)

    def calculate_bias_voltage(self):
        self.Vce = self.Vc - self.Ve

    def calculate_resistor_in_parallel(self, r1, r2):
        r_eqv = (r1 * r2) / (r1 + r2)
        return r_eqv


# resistors = {
#     "rc": 3 * 10**3,
#     "re": 0 * 10**3,
#     "rb_1": 500 * 10**3,
#     "rb_2": 0 * 10**3
# }

resistors = {
    "rc": 150,
    "re": 150,
    "rb_1": 30 * 10**3,
    "rb_2": 20.9 * 10**3
}



# smth wrong here
bjt = Bjt("2N2222", 60)
bjt1 = Bjt("BC107", 200)

t = Transistor()
print(type(t))
t.add_transistor(transistor=bjt)

print(t.transistors["2N2222"])
print(t.transistors["2N2222"].hfe)
print(t(model="2N2222"))

print(bjt)
print(bjt1)
print(bjt1 == bjt)
print(bjt1 > bjt)



a = VDBias(**resistors)
# a.calculate()
# a.setup_documentation()
