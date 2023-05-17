"""
Date: 2023-03-28
Class: VoltageDivider
Description: This class represents Voltage Divider Bias circuit, and do all related calculations.

https://www.electronics-tutorials.ws/amplifier/common-collector-amplifier.html
https://www.electronics-tutorials.ws/amplifier/input-impedance-of-an-amplifier.html
https://www.diystompboxes.com/biascalc/ffbias.html
https://www.electronics-tutorials.ws/amplifier/amp_2.html
"""
import math
from transistor import Bjt
from circuit import Circuit


class VoltageDivider(Circuit):
    def __init__(self, vcc: int, transistor: Bjt, rc: float, re: float, rbc: float, rbe: float, cc: float, ce: float, cb: float):
        super().__init__(vcc=vcc, transistor=transistor, rc=rc, re=re, cc=cc, ce=ce, cb=cb)
        self.rbc: float = rbc
        self.rbe: float = rbe

    def calculate_bias(self):
        self.calculate_base_current()
        self.calculate_collector_current()
        self.calculate_emitter_current()
        self.calculate_collector_voltage()
        self.calculate_emitter_voltage()
        self.calculate_base_voltage()
        self.calculate_collector_emitter_voltage()
        self.calculate_input_impedance()
        self.calculate_output_impedance()
        self.calculate_voltage_gain()
        # self.calculate_input_coupling_capacitor()
        # self.calculate_output_coupling_capacitor()
        # self.calculate_emitter_capacitor()
        self.determine_q_point()

        self.bias_data.convert_data()

    def calculate_base_current(self):
        numerator = (self.vcc * (self.rbe / (self.rbe + self.rbc)) - self.transistor.vbe)
        denominator = (((self.rbe * self.rbc) / (self.rbe + self.rbc)) + self.re * (self.transistor.hfe + 1))
        self.bias_data.ib = numerator / denominator

    def calculate_collector_current(self):
        self.bias_data.ic = self.transistor.hfe * self.bias_data.ib

    def calculate_emitter_current(self):
        self.bias_data.ie = self.bias_data.ib + self.bias_data.ic

    def calculate_collector_voltage(self):
        self.bias_data.vc = self.vcc - (self.bias_data.ic * self.rc)

    def calculate_emitter_voltage(self):
        self.bias_data.ve = self.re * self.bias_data.ie

    def calculate_base_voltage(self):
        self.bias_data.vb = self.bias_data.ve + self.transistor.vbe

    def calculate_collector_emitter_voltage(self):
        self.bias_data.vce = self.bias_data.vc - self.bias_data.ve

    def determine_q_point(self):
        """
        TODO: to be investigated
        """
        v_thevenin = (self.vcc * (self.rbe / (self.rbe + self.rbc)))    # equivalent base voltage?
        r_thevenin = (self.rbe * self.rbc) / (self.rbe + self.rbc)      # equivalent base resistance?
        vb = round(self.transistor.vbe + (self.bias_data.ic / 1000 * self.re), 3)  # v_th is alternative, vb is more accurate??

        vce_bias = round(self.vcc - (self.bias_data.ic / 1000 * (self.rc + self.re)), 3)    # output: 11.994??
        vce_cutoff = self.vcc

        ic = round(((v_thevenin - self.transistor.vbe) / (self.re + (r_thevenin / self.transistor.hfe))) * 1000, 3)
        ic_saturation = round((self.vcc / (self.rc + self.re)) * 1000, 3)

        self.bias_data.q_point = [[vce_bias, vce_cutoff], [ic, ic_saturation]]

    def calculate_voltage_gain(self):
        transistor_re = (self.transistor.internal_emitter_voltage_drop / self.bias_data.ie)
        if self.ce != 0:
            self.calculate_voltage_gain_for_ac_application(transistor_re=transistor_re)
        else:
            self.calculate_voltage_gain_for_dc_application(transistor_re=transistor_re)

    def calculate_voltage_gain_for_ac_application(self, transistor_re: float):
        """
        TODO: plot it with Xc changing in frequency
        Voltage gain with bypass capacitor Ce:   Av = Rout/re + (Re || Xc(Ce))
        """
        av = self.bias_data.z_out / transistor_re
        self.bias_data.av = av

    def calculate_voltage_gain_for_dc_application(self, transistor_re: float):
        av = self.bias_data.z_out / (self.re + transistor_re)
        self.bias_data.av = av

    def calculate_input_impedance(self):
        # with emitter bypass cap: Zin = R1 || R2 || hfe*re
        # without emitter bypass cap: Zin = R1 || R2 || hfe(Re + re)
        transistor_re = (self.transistor.internal_emitter_voltage_drop / self.bias_data.ie)
        r_thevenin = ((self.rbe * self.rbc) / (self.rbe + self.rbc))  # base equivalent resistance

        if self.ce != 0:
            self.calculate_input_impedance_for_ac_application(transistor_re=transistor_re, r_thevenin=r_thevenin)
        else:
            self.calculate_input_impedance_for_dc_application(transistor_re=transistor_re, r_thevenin=r_thevenin)

    def calculate_input_impedance_for_ac_application(self, transistor_re: float, r_thevenin: float):
        base_impedance_ac = ((self.transistor.hfe + 1) * transistor_re)
        input_impedance_ac = ((r_thevenin * base_impedance_ac) / (r_thevenin + base_impedance_ac))
        self.bias_data.z_in_ac = input_impedance_ac

    def calculate_input_impedance_for_dc_application(self, transistor_re: float, r_thevenin: float):
        base_impedance_dc = ((self.transistor.hfe + 1) * (self.re + transistor_re))
        input_impedance_dc = ((r_thevenin * base_impedance_dc) / (r_thevenin + base_impedance_dc))
        self.bias_data.z_in_dc = input_impedance_dc

    def calculate_output_impedance(self):
        z_out = self.rc
        self.bias_data.z_out = z_out

    def calculate_emitter_capacitor(self, frequency: int):
        """
        Emitter capacitor forms a high pass filter, frequencies above cutoff frequency got maximum gain
        make plot with set of frequency and show how gain is changing according to freq

        Rule of thumb: Xc = 1/10 of Re at desired frequency
        """
        xc = 0.1 * self.re
        self.ce = 1 / (2 * math.pi * frequency * xc)

    def calculate_input_coupling_capacitor(self, frequency: int, z_in: float):
        """z_in is considered only for AC application"""
        self.cb = 1 / (2 * math.pi * frequency * z_in)

    def calculate_output_coupling_capacitor(self, frequency: int, z_out: float):
        self.cc = 1 / (2 * math.pi * frequency * z_out)
