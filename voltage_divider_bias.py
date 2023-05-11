"""
Description: this class do all calculations, for Voltage Divider Bias.
https://www.electronics-tutorials.ws/amplifier/common-collector-amplifier.html
https://www.electronics-tutorials.ws/amplifier/input-impedance-of-an-amplifier.html
"""
from bias_circuit import BiasCircuit
from transistor import Bjt
import math
import dataclasses


@dataclasses.dataclass
class VoltageDividerBiasDataclass:
    """
    ib: float = None - base current
    ic: float = None - collector current
    ie: float = None - emitter current
    vc: float = None - collector voltage
    ve: float = None - emitter voltage
    vb: float = None - base voltage
    irbe: float = None - current across base-emitter resistor
    irbc: float = None - current across base-collectr resistor
    vce: float = None - collector-emitter voltage (determines bias level of input signal)
    av: float = None - voltage gain [dB]??
    z_in: float = None - input impedance
    z_out: float = None - output impedance
    q_point: dict[str, str] = None - q-point of working transistor ()
    """
    ib: float = None
    ic: float = None
    ie: float = None
    vc: float = None
    ve: float = None
    vb: float = None
    irbe: float = None
    irbc: float = None
    vce: float = None
    av: float = None
    z_in: float = None
    z_out: float = None
    q_point: dict[str, str] = None


class VoltageDividerBias(BiasCircuit):
    def __init__(self, vcc: int, transistor: Bjt, rc: float, re: float, rbc: float, rbe: float):
        super().__init__(vcc=vcc, transistor=transistor, rc=rc, re=re)
        self.rbc: float = rbc
        self.rbe: float = rbe
        self.voltage_divider_bias_dataclass: VoltageDividerBiasDataclass = VoltageDividerBiasDataclass()
    
    def read_circuit_data(self) -> VoltageDividerBiasDataclass:
        """Return all data"""
        return self.voltage_divider_bias_dataclass

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
        print(self.voltage_divider_bias_dataclass)

    def calculate_base_current(self):
        numerator = (self.vcc * (self.rbe / (self.rbe + self.rbc)) - self.transistor.vbe)
        denominator = (((self.rbe * self.rbc) / (self.rbe + self.rbc)) + self.re * (self.transistor.hfe + 1))
        self.voltage_divider_bias_dataclass.ib = numerator / denominator

    def calculate_collector_current(self):
        self.voltage_divider_bias_dataclass.ic = self.transistor.hfe * self.voltage_divider_bias_dataclass.ib

    def calculate_emitter_current(self):
        self.voltage_divider_bias_dataclass.ie = self.voltage_divider_bias_dataclass.ib + self.voltage_divider_bias_dataclass.ic

    def calculate_collector_voltage(self):
        self.voltage_divider_bias_dataclass.vc = self.vcc - (self.voltage_divider_bias_dataclass.ic * self.rc)

    def calculate_emitter_voltage(self):
        self.voltage_divider_bias_dataclass.ve = self.re * self.voltage_divider_bias_dataclass.ie

    def calculate_base_voltage(self):
        self.voltage_divider_bias_dataclass.vb = self.voltage_divider_bias_dataclass.ve + self.transistor.vbe

    def calculate_rbe_current(self):
        self.voltage_divider_bias_dataclass.irbe = self.voltage_divider_bias_dataclass.vb / self.rbe

    def calculate_rbc_current(self):
        self.voltage_divider_bias_dataclass.irbc = self.voltage_divider_bias_dataclass.irbe + self.voltage_divider_bias_dataclass.ib

    def calculate_collector_emitter_voltage(self):
        # bias voltage
        self.voltage_divider_bias_dataclass.vce = self.voltage_divider_bias_dataclass.vc - self.voltage_divider_bias_dataclass.ve

    def determine_q_point(self):
        ic_sat = round((self.vcc / (self.rc + self.re)) * 1000, 3)
        vce_cutoff = self.vcc
        v_th = (self.vcc * (self.rbe / (self.rbe + self.rbc)))
        r_th = (self.rbe * self.rbc) / (self.rbe + self.rbc)    # equivalent base resistance
        ic = round(((v_th - self.transistor.vbe) / (self.re + (r_th / self.transistor.hfe))) * 1000, 3)
        vce_bias = round(self.vcc - (self.voltage_divider_bias_dataclass.ic / 1000 * (self.rc + self.re)), 3)
        vb = round(self.transistor.vbe + (self.voltage_divider_bias_dataclass.ic / 1000 * self.re), 3)   # v_th is alternative, vb is more accurate

        q_point: dict = {
            "Vce(bias)/Vce(cutoff) [V]": f"[{vce_bias}/{vce_cutoff}]",
            "ic/ic(sat)": f"[{ic}/{ic_sat}]"
        }
        self.voltage_divider_bias_dataclass.Q_point = q_point

    def calculate_voltage_gain(self):
        """
        With bypass capacitor Ce:   Av = Rout/re    make plot with set of frequency and show how gain is changing according to freq
        Without bypass capacitor Ce:    Av = Rout/Re+re
        """
        re = (25 / self.voltage_divider_bias_dataclass.ie) / 1000
        av = self.voltage_divider_bias_dataclass.z_out / re
        self.voltage_divider_bias_dataclass.av = av

    def calculate_input_impedance(self):
        # TODO: remove these / 1000, it depends on multiplier
        # with bypass cap (AC): Zin = R1 || R2 || hfe*re
        # without bypass cap (DC): Zin = R1 || R2 || hfe(Re + re)
        re = (25 / self.voltage_divider_bias_dataclass.ie) / 1000   # emitter leg resistance, V/A to mV/mA
        z_base_ac = ((self.transistor.hfe + 1) * re)
        z_base_dc = ((self.transistor.hfe + 1) * (self.re + re))
        r_th = ((self.rbe * self.rbc) / (self.rbe + self.rbc))      # base equivalent resistance
        input_impedance = ((r_th * z_base_ac) / (r_th + z_base_ac)) / 1000
        self.voltage_divider_bias_dataclass.Z_in = input_impedance

    def calculate_output_impedance(self):
        """
        Zout = Rc || Rl     load is speaker or smth connected to collector of transistor
        """
        z_out = self.rc
        self.voltage_divider_bias_dataclass.z_out = z_out

    def calculate_emitter_capacitor(self, frequency: int) -> float:
        """
        Emitter capacitor forms a high pass filter, frequencies above cutoff frequency got maximum gain
        make plot with set of frequency and show how gain is changing according to freq

        Rule of thumb: Xc = 1/10 of Re at desired frequency
        """
        xc = 0.1 * self.re
        c_emitter = 1 / (2 * math.pi * frequency * xc)
        return c_emitter

    def calculate_input_coupling_capacitor(self, frequency: int, z_in: float) -> float:
        """z_in is considered only for AC application"""
        c_in = 1 / (2 * math.pi * frequency * z_in)
        return c_in

    def calculate_output_coupling_capacitor(self, frequency: int, z_out: float) -> float:
        c_out = 1 / (2 * math.pi * frequency * z_out)
        return c_out
