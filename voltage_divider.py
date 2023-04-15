"""
Description: this class do all calculations, for Voltage Divider Bias.
https://www.electronics-tutorials.ws/amplifier/common-collector-amplifier.html
https://www.electronics-tutorials.ws/amplifier/input-impedance-of-an-amplifier.html
"""
import math
import dataclasses


@dataclasses.dataclass
class VoltageDividerDataclass:
    Ib: float = None
    Ic: float = None
    Ie: float = None
    Vc: float = None
    Ve: float = None
    Vb: float = None
    Irbe: float = None
    Irbc: float = None
    Vce: float = None
    Av: float = None
    Z_in: float = None
    Z_out: float = None
    Q_point: dict[str, str] = None


class VoltageDivider(object):
    def __init__(self, transistor: 'Bjt', rc: float, re: float, rbc: float, rbe: float, vcc: int):
        self.transistor: 'Bjt' = transistor
        self.Rbc: float = rbc
        self.Rbe: float = rbe
        self.Rc: float = rc
        self.Re: float = re
        self.Vcc: int = vcc
        self._voltage_divider_dataclass: VoltageDividerDataclass = VoltageDividerDataclass()

    def __str__(self):
        return f"Voltage Divider"

    @property
    def voltage_divider_dataclass(self):
        return self._voltage_divider_dataclass

    def calculate(self):
        self.calculate_base_current()
        self.calculate_collector_current()
        self.calculate_emitter_current()
        self.calculate_collector_voltage()
        self.calculate_emitter_voltage()
        self.calculate_base_voltage()
        self.calculate_rbe_current()
        self.calculate_rbc_current()
        self.calculate_collector_emitter_voltage()
        self.calculate_input_impedance()
        self.calculate_output_impedance()
        self.calculate_voltage_gain()
        # self.calculate_input_coupling_capacitor()
        # self.calculate_output_coupling_capacitor()
        # self.calculate_emitter_capacitor()
        self.determine_q_point()
        print(self.voltage_divider_dataclass)

    def calculate_base_current(self):
        numerator = (self.Vcc * (self.Rbe / (self.Rbe + self.Rbc)) - self.transistor.vbe)
        denominator = (((self.Rbe * self.Rbc) / (self.Rbe + self.Rbc)) + self.Re * (self.transistor.hfe + 1))
        self.voltage_divider_dataclass.Ib = numerator / denominator

    def calculate_collector_current(self):
        self.voltage_divider_dataclass.Ic = self.transistor.hfe * self.voltage_divider_dataclass.Ib

    def calculate_emitter_current(self):
        self.voltage_divider_dataclass.Ie = self.voltage_divider_dataclass.Ib + self.voltage_divider_dataclass.Ic

    def calculate_collector_voltage(self):
        self.voltage_divider_dataclass.Vc = self.Vcc - (self.voltage_divider_dataclass.Ic * self.Rc)

    def calculate_emitter_voltage(self):
        self.voltage_divider_dataclass.Ve = self.Re * self.voltage_divider_dataclass.Ie

    def calculate_base_voltage(self):
        self.voltage_divider_dataclass.Vb = self.voltage_divider_dataclass.Ve + self.transistor.vbe

    def calculate_rbe_current(self):
        self.voltage_divider_dataclass.Irbe = self.voltage_divider_dataclass.Vb / self.Rbe

    def calculate_rbc_current(self):
        self.voltage_divider_dataclass.Irbc = self.voltage_divider_dataclass.Irbe + self.voltage_divider_dataclass.Ib

    def calculate_collector_emitter_voltage(self):
        # bias voltage
        self.voltage_divider_dataclass.Vce = self.voltage_divider_dataclass.Vc - self.voltage_divider_dataclass.Ve

    def determine_q_point(self):
        ic_sat = round((self.Vcc / (self.Rc + self.Re)) * 1000, 3)
        vce_cutoff = self.Vcc
        v_th = (self.Vcc * (self.Rbe / (self.Rbe + self.Rbc)))
        r_th = (self.Rbe * self.Rbc) / (self.Rbe + self.Rbc)    # equivalent base resistance
        ic = round(((v_th - self.transistor.vbe) / (self.Re + (r_th / self.transistor.hfe))) * 1000, 3)
        vce_bias = round(self.Vcc - (self.voltage_divider_dataclass.Ic / 1000 * (self.Rc + self.Re)), 3)
        vb = round(self.transistor.vbe + (self.voltage_divider_dataclass.Ic / 1000 * self.Re), 3)   # v_th is alternative, vb is more accurate

        q_point: dict = {
            "Vce(bias)/Vce(cutoff) [V]": f"[{vce_bias}/{vce_cutoff}]",
            "Ic/Ic(sat)": f"[{ic}/{ic_sat}]"
        }
        self.voltage_divider_dataclass.Q_point = q_point

    def calculate_voltage_gain(self):
        """
        With bypass capacitor Ce:   Av = Rout/re
        Without bypass capacitor Ce:    Av = Rout/Re+re
        """
        re = (25 / self.voltage_divider_dataclass.Ie) / 1000
        Av = self.voltage_divider_dataclass.Z_out / re
        self.voltage_divider_dataclass.Av = Av

    def calculate_input_impedance(self):
        # TODO: remove these / 1000, it depends on multiplier
        # with bypass cap (AC): Zin = R1 || R2 || hfe*re
        # without bypass cap (DC): Zin = R1 || R2 || hfe(Re + re)
        re = (25 / self.voltage_divider_dataclass.Ie) / 1000   # emitter leg resistance, V/A to mV/mA
        z_base_ac = ((self.transistor.hfe + 1) * re)
        z_base_dc = ((self.transistor.hfe + 1) * (self.Re + re))
        r_th = ((self.Rbe * self.Rbc) / (self.Rbe + self.Rbc))      # base equivalent resistance
        input_impedance = ((r_th * z_base_ac) / (r_th + z_base_ac)) / 1000
        self.voltage_divider_dataclass.Z_in = input_impedance

    def calculate_output_impedance(self):
        """
        Zout = Rc || Rl     load is speaker or smth connected to collector of transistor
        """
        z_out = self.Rc
        self.voltage_divider_dataclass.Z_out = z_out

    def calculate_emitter_capacitor(self, frequency: int) -> float:
        """
        Emitter capacitor forms a high pass filter, frequencies above cutoff frequency got maximum gain
        Rule of thumb: Xc = 1/10 of Re at desired frequency
        """
        xc = 0.1 * self.Re
        c_emitter = 1 / (2 * math.pi * frequency * xc)
        return c_emitter

    def calculate_input_coupling_capacitor(self, frequency: int, z_in: float) -> float:
        """z_in is considered only for AC application"""
        c_in = 1 / (2 * math.pi * frequency * z_in)
        return c_in

    def calculate_output_coupling_capacitor(self, frequency: int, z_out: float) -> float:
        c_out = 1 / (2 * math.pi * frequency * z_out)
        return c_out
