"""
Description: This class do calculations for Collector Feedback Bias.
"""


class CollectorFeedback(object):
    def __init__(self, transistor: 'Bjt', rb: float, rc: float, re: float, vcc: int = 9):
        self.Vcc: int = vcc
        self.transistor: 'Bjt' = transistor
        self.Rb: float = rb
        self.Rc: float = rc
        self.Re: float = re
        self.documentation: dict = {}

    def __str__(self):
        return f"Collector Feedback"

    def read_documentation(self):
        print(self.documentation)

    def write_documentation(self, ib: float, ic: float, ie: float, vb: float, vc: float, ve: float, zin: float, av: float, qpoint: dict):
        self.documentation = {
            "Model": self.transistor.model,
            "Hfe": self.transistor.hfe,
            "Ib [uA]": ib * 1000000,
            "Ic [mA]": ic * 1000,
            "Ie [mA]": ie * 1000,
            "Vb [V]": vb,
            "Vc [V]": vc,
            "Ve [V]": ve,
            "Zin [KOhm]": zin / 1000,
            "Av [V]": av,
            "Qpoint": qpoint
        }

        for k, v in self.documentation.items():
            if k == "Qpoint" or type(v) is str:
                continue
            self.documentation[k] = round(v, 3)

        # self.documentation = {k: round(v, 3) for k, v in self.documentation.items()}
        return self.documentation

    def calculate_and_save_values(self):
        Ib = self.calculate_base_current()
        Ic = self.calculate_collector_current(base_current=Ib)
        Ie = self.calculate_emitter_current(base_current=Ib, collector_current=Ic)
        Vc = self.calculate_collector_voltage(collector_current=Ic)
        Ve = self.calculate_emitter_volatge(emitter_current=Ie)
        Vb = self.calculate_base_voltage(emitter_voltage=Ve)
        Vce = self.calculate_collector_emitter_voltage(collector_voltage=Vc, emitter_voltage=Ve)
        Q_point = self.calculate_q_point(collector_emitter_voltage=Vce, collector_current=Ic)
        Zin = self.calculate_input_impedance(emitter_current=Ie)
        Av = self.calculate_voltage_gain(emitter_current=Ie)

        self.write_documentation(ib=Ib, ic=Ic, ie=Ie, vb=Vb, vc=Vc, ve=Ve, zin=Zin, av=Av, qpoint=Q_point)

    def calculate_base_current(self) -> float:
        return (self.Vcc - self.transistor.vbe) / (self.Rb + (self.transistor.hfe + 1) * (self.Rc + self.Re))  # A to mA

    def calculate_collector_current(self, base_current: float) -> float:
        return base_current * self.transistor.hfe

    def calculate_emitter_current(self, base_current: float, collector_current: float) -> float:
        return base_current + collector_current

    def calculate_collector_voltage(self, collector_current: float) -> float:
        voltage_drop_on_rc = self.Rc * collector_current
        return self.Vcc - voltage_drop_on_rc

    def calculate_emitter_volatge(self, emitter_current: float) -> float:
        return self.Re * emitter_current

    def calculate_base_voltage(self, emitter_voltage: float) -> float:
        return self.transistor.vbe + emitter_voltage

    def calculate_collector_emitter_voltage(self, collector_voltage: float, emitter_voltage: float) -> float:
        return collector_voltage - emitter_voltage

    def calculate_q_point(self, collector_emitter_voltage: float, collector_current: float) -> dict:
        collector_emitter_voltage = round(collector_emitter_voltage, 3)
        collector_current = round(collector_current * 1000, 3)
        maximum_collector_current = round((self.Vcc / (self.Rc + self.Re)) * 1000, 3)

        q_point: dict = {
            "Vce bias/VCC [V]": f"[{collector_emitter_voltage}/{self.Vcc}]",
            "Ic/Ic max [mA]": f"[{collector_current}/{maximum_collector_current}]"
        }
        return q_point

    def calculate_voltage_gain(self, emitter_current: float) -> float:
        # 2nd method
        # gm = emitter_current / self.transistor.internal_emitter_voltage_drop
        # gain = gm * self.Rc

        re = self.transistor.internal_emitter_voltage_drop / emitter_current
        return self.Rc / (self.Re + re)

    def calculate_input_impedance(self, emitter_current: float) -> float:
        # 2nd method
        # re = self.transistor.internal_emitter_voltage_drop / emitter_current
        # z_in = self.transistor.hfe * (self.Re + re)
        # r_pi = Zin, not sure if calculating correct

        gm = emitter_current / self.transistor.internal_emitter_voltage_drop
        r_pi = ((self.transistor.hfe + 1) / gm)
        return r_pi
