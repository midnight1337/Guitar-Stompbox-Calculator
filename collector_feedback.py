"""

Date: 2023-03-28
Class: CollectorFeedbackBiasData
Description: This dataclass is database for calculated data from CollectorFeedbackBias class.

Class: CollectorFeedbackBias
Description: This class represents Collector Feedback Bias circuit, and do all related calculations.
"""


class CollectorFeedback(object):
    def __init__(self, transistor: 'Bjt', rb: float, rc: float, re: float, vcc: int):
        """
        :param transistor:
        :param rb:
        :param rc:
        :param re:
        :param vcc:
        """
        self.transistor: 'Bjt' = transistor
        self.Rb: float = rb
        self.Rc: float = rc
        self.Re: float = re
        self.Vcc: int = vcc
        self.documentation: dict = {}

    def read_documentation(self):
        print(f"Collector Feedback:\n", self.documentation)

    def write_documentation(self, ib: float, ic: float, ie: float, vb: float, vc: float, ve: float,
                            zin: float, av: float, q_point: dict):
        self.documentation = {
            "Transistor": self.transistor,
            "Ib [uA]": ib * 1000000,
            "Ic [mA]": ic * 1000,
            "Ie [mA]": ie * 1000,
            "Vb [V]": vb,
            "Vc [V]": vc,
            "Ve [V]": ve,
            "Zin [KOhm]": zin / 1000,
            "Av(gain) [V]": av,
            "Q_point": q_point
        }

        for k, v in self.documentation.items():
            if k == "Q_point" or type(v) is type(self.transistor):
                continue
            self.documentation[k] = round(v, 3)

        # self.documentation = {k: round(v, 3) for k, v in self.documentation.items()}
        return self.documentation

    def calculate(self):
        ib: float = self.calculate_base_current()
        ic: float = self.calculate_collector_current(base_current=ib)
        ie: float = self.calculate_emitter_current(base_current=ib, collector_current=ic)
        vc: float = self.calculate_collector_voltage(collector_current=ic)
        ve: float = self.calculate_emitter_volatge(emitter_current=ie)
        vb: float = self.calculate_base_voltage(emitter_voltage=ve)
        vce: float = self.calculate_collector_emitter_voltage(collector_voltage=vc, emitter_voltage=ve)
        q_point: dict[str, str] = self.calculate_q_point(collector_emitter_voltage=vce, collector_current=ic)
        z_in: float = self.calculate_input_impedance(emitter_current=ie)
        av: float = self.calculate_voltage_gain(emitter_current=ie)

        self.write_documentation(ib=ib, ic=ic, ie=ie, vb=vb, vc=vc, ve=ve, zin=z_in, av=av, q_point=q_point)
        self.read_documentation()

    def calculate_base_current(self) -> float:
        return (self.Vcc - self.transistor.vbe) / (self.Rb + (self.transistor.hfe + 1) * (self.Rc + self.Re))

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

    def calculate_q_point(self, collector_emitter_voltage: float, collector_current: float) -> dict[str, str]:
        collector_emitter_voltage = round(collector_emitter_voltage, 3)
        collector_current = round(collector_current * 1000, 3)
        collector_current_sat = round((self.Vcc / (self.Rc + self.Re)) * 1000, 3)

        q_point: dict = {
            "Vce(bias)/Vce(cutoff) [V]": f"[{collector_emitter_voltage}/{self.Vcc}]",
            "Ic/Ic(sat) [mA]": f"[{collector_current}/{collector_current_sat}]"
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

    def plot_q_point(self):
        pass
