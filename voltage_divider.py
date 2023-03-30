"""
Description: this class do all calculations, for Voltage Divider Bias.
"""


class VoltageDivider(object):
    def __init__(self, transistor: 'Bjt', rbc: float, rbe: float, rc: float, re: float, vcc: int):
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

    def write_documentation(self, ib: float, ic: float, ie: float, vc: float, ve: float, vb: float,
                            irbe: float, irbc: float, vce: float, q_point: dict, v_check: bool):
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
            "Q_point": q_point,
            "Voltage check": v_check,
        }

        for k, v in self.documentation.items():
            if k == "Q_point" or type(v) is type(self.transistor):
                continue
            self.documentation[k] = round(v, 3)

    def calculate_and_read_values(self):
        ib: float = self.calculate_base_current()
        ic: float = self.calculate_collector_current(base_current=ib)
        ie: float = self.calculate_emitter_current(base_current=ib, collector_current=ic)
        vc: float = self.calculate_collector_voltage(collector_current=ic)
        ve: float = self.calculate_emitter_voltage(emitter_current=ic)
        vb: float = self.calculate_base_voltage(emitter_voltage=ve)
        irbe: float = self.calculate_rbe_current(base_voltage=vb)
        irbc: float = self.calculate_rbc_current(rbe_current=irbe, base_current=ib)
        vce: float = self.calculate_collector_emitter_voltage(collector_voltage=vc, emitter_voltage=ve)
        z_in: float = self.calculate_input_impedance(emitter_current=ic)
        q_point: dict[str, str] = self.determine_q_point()
        v_check: bool = self.check_voltage_across_rbe_and_rbc(irbc_current=irbc, irbe_current=irbe)

        self.write_documentation(ib=ib, ic=ic, ie=ie, vc=vc, ve=ve, vb=vb, irbe=irbe,
                                 irbc=irbc, vce=vce, q_point=q_point, v_check=v_check)
        self.read_documentation()

    def calcualte_equivalent_base_resistance(self) -> float:
        return (self.Rbe * self.Rbc) / (self.Rbe + self.Rbc)

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

    def calculate_collector_emitter_voltage(self, collector_voltage: float, emitter_voltage: float) -> float:
        # bias voltage
        return collector_voltage - emitter_voltage

    def determine_q_point(self) -> dict[str, str]:
        ic_sat = round((self.Vcc / (self.Rc + self.Re)) * 1000, 3)
        vce_cutoff = self.Vcc
        v_th = (self.Vcc * (self.Rbe / (self.Rbe + self.Rbc)))
        r_th = (self.Rbe * self.Rbc) / (self.Rbe + self.Rbc)    # equivalent base resistance
        ic = round(((v_th - self.transistor.vbe) / (self.Re + (r_th / self.transistor.hfe))) * 1000, 3)
        vce_bias = round(self.Vcc - (ic * 1000 * (self.Rc + self.Re)), 3)
        vb = self.transistor.vbe + (ic * self.Re)   # v_th is alternative, vb is more accurate

        q_point: dict = {
            "Vce(bias)/Vce(cutoff) [V]": f"[{vce_bias}/{vce_cutoff}]",
            "Ic/Ic(sat) [mA]": f"[{ic}/{ic_sat}]"
        }
        return q_point

    def calculate_input_impedance(self, emitter_current: float) -> float:
        # TODO: remove these / 1000, it depends on multiplier
        # on going: with bypass cap: Zin = R1 || R2 || hfe*re
        # without bypass cap (DC): Zin = R1 || R2 || hfe(Re + re)
        re = (25 / emitter_current) / 1000   # V/A to mV/mA
        re_eqv = (self.Re * self.Rc) / (self.Re + self.Rc)
        z_base = ((self.transistor.hfe + 1) * (re_eqv + re))
        r_bias = ((self.Rbe * self.Rbc) / (self.Rbe + self.Rbc))

        input_impedance = ((r_bias * z_base) / (r_bias + z_base))
        return input_impedance

    def check_voltage_across_rbe_and_rbc(self, irbc_current: float, irbe_current: float) -> bool:
        vrbc = irbc_current * self.Rbc
        vrbe = irbe_current * self.Rbe
        return bool(round((vrbc + vrbe)) == self.Vcc)

    def plot_q_point(self):
        # TODO: graphical plotting q point
        pass
