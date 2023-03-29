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

    def write_documentation(self, ib: float, ic: float, ie: float, vc: float, ve: float, vb: float, irbe: float, irbc: float, vce: float, v_check: bool):
        # TODO: change 'multiplier' to variable, it depends on actual multiplier used in resistor class
        self.documentation = {
            "Transistor": self.transistor,
            "Ib [uA]": ib * 1000000,
            "Ic [mA]": ic * 1000,
            "Ie [mA]": ie * 1000,
            "Vc [V]": vc,
            "Ve [V]": ve,
            "Vb [V]": vb,
            "Irbe [mA]": irbe * 1000,
            "Irbc [mA]": irbc * 1000,
            "Vce [V]": vce,
            "Voltage check": v_check,
        }

        for k, v in self.documentation.items():
            if k == "Qpoint" or type(v) is type(self.transistor):
                continue
            self.documentation[k] = round(v, 3)

    def calculate(self):
        Ib = self.calculate_base_current()
        Ic = self.calculate_collector_current(base_current=Ib)
        Ie = self.calculate_emitter_current(base_current=Ib, collector_current=Ic)
        Vc = self.calculate_collector_voltage(collector_current=Ic)
        Ve = self.calculate_emitter_voltage(emitter_current=Ic)
        Vb = self.calculate_base_voltage(emitter_voltage=Ve)
        Irbe = self.calculate_rbe_current(base_voltage=Vb)
        Irbc = self.calculate_rbc_current(rbe_current=Irbe, base_current=Ib)
        Vce = self.calculate_collector_emitter_voltage(collector_voltage=Vc, emitter_voltage=Ve)
        z_in = self.calculate_input_impedance(emitter_current=Ic)

        v_check: bool = self.check_voltage_across_rbe_and_rbc(irbc_current=Irbc, irbe_current=Irbe)
        self.write_documentation(ib=Ib, ic=Ic, ie=Ie, vc=Vc, ve=Ve, vb=Vb, irbe=Irbe, irbc=Irbc, vce=Vce, v_check=v_check)

    def calcualte_equivalent_base_resistance(self):
        Rb = (self.Rbe * self.Rbc) / (self.Rbe + self.Rbc)

    def calculate_base_current(self) -> float:
        numerator = (self.Vcc * (self.Rbe / (self.Rbe + self.Rbc)) - self.transistor.vbe)
        denominator = (((self.Rbe * self.Rbc) / (self.Rbe + self.Rbc)) + self.Re * (self.transistor.hfe + 1))
        return numerator / denominator

    def calculate_collector_current(self, base_current: float) -> float:
        return self.transistor.hfe * base_current

    def calculate_emitter_current(self, base_current: float, collector_current: float) -> float:
        return base_current + collector_current

    def calculate_collector_voltage(self, collector_current: float):
        return self.Vcc - (collector_current * self.Rc)

    def calculate_emitter_voltage(self, emitter_current: float) -> float:
        return self.Re * emitter_current

    def calculate_base_voltage(self, emitter_voltage: float) -> float:
        return emitter_voltage + self.transistor.vbe

    def calculate_rbe_current(self, base_voltage: float) -> float:
        return base_voltage / self.Rbe

    def calculate_rbc_current(self, rbe_current: float, base_current: float) -> float:
        return rbe_current + base_current

    def calculate_collector_emitter_voltage(self, collector_voltage: float, emitter_voltage: float):
        # bias voltage
        return collector_voltage - emitter_voltage

    def determine_q_point(self):
        pass

    def calculate_input_impedance(self, emitter_current: float):
        # TODO: remove these / 1000, it depends on multiplier
        # on going
        re = (25 / emitter_current) / 1000   # V/A to mV/mA
        re_eqv = (self.Re * self.Rc) / (self.Re + self.Rc)
        z_base = ((self.transistor.hfe + 1) * (re_eqv + re))
        r_bias = ((self.Rbe * self.Rbc) / (self.Rbe + self.Rbc))

        print(z_base)
        print(r_bias)
        input_impedance = ((r_bias * z_base) / (r_bias + z_base))
        print(input_impedance)
        return input_impedance

    def check_voltage_across_rbe_and_rbc(self, irbc_current: float, irbe_current: float) -> bool:
        vrbc = irbc_current * self.Rbc
        vrbe = irbe_current * self.Rbe
        return bool(round((vrbc + vrbe)) == self.Vcc)
