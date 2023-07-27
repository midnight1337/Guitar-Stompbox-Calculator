"""
Date: 2023-05-13
Class: BiasData
Description: This dataclass purpose is to store calculated bias data in related circuit classes
"""
from dataclasses import dataclass


@dataclass
class BiasData:
    """
    ib: float - base current [uA]
    ic: float - collector current [mA]
    ie: float - emitter current [mA]
    vc: float - collector voltage [V]
    ve: float - emitter voltage [V]
    vb: float - base voltage [V]
    vce: float - collector-emitter voltage (determines bias level of input signal) [V]
    av: float - voltage gain [dB/V]??
    z_in: float - input impedance [KΩ]
    z_out: float - output impedance [KΩ]
    q_point: list[list] - q-point of working transistor [Vce(bias)/Vce(cutoff) [V] | Ic/Ic(saturation) [mA]]
    """
    ib: float
    ic: float
    ie: float
    vb: float
    vc: float
    ve: float
    vce: float
    av: float
    z_in_ac: float
    z_in_dc: float
    z_out: float
    q_point: list[list]

    def get_data(self):
        return self.__dict__

    def convert_data(self):
        self.ib *= 1000000
        self.ic *= 1000
        self.ie *= 1000
        self.z_in_ac /= 1000
        self.z_in_dc /= 1000
        self.z_out /= 1000

        for k, v in self.__dict__.items():
            if k == "q_point":
                self.q_point[0][0] = self.vce
                self.q_point[1][0] = self.ic
            else:
                self.__dict__[k] = round(v, 3)
