"""
Date: 2023-05-11
Class: Circuit
Description: This abstract class requires to initialise methods related to biasing,
and pass parts necessary for circuit breadboard. It is inherited in all bias related classes.
"""
from abc import ABC, abstractmethod
from transistor import Bjt
from bias_data import BiasData


class Circuit(ABC):
    def __init__(self, vcc: int, transistor: Bjt, rc: float, re: float, cc: float, ce: float, cb: float):
        """
        :param vcc: Voltage Supply
        :param transistor: Transistor object
        :param rc: Collector resistor
        :param re: Emitter resistor
        :param cc: Collector capacitor
        :param ce: Emitter capacitor
        :param cb: Base capacitor
        """
        self.vcc: int = vcc
        self.transistor: Bjt = transistor
        self.rc: float = rc
        self.re: float = re
        self.cc: float = cc
        self.ce: float = ce
        self.cb: float = cb
        self.bias_data: BiasData = BiasData.__new__(BiasData)
    
    def __str__(self):
        return self.__class__.__name__

    def get_bias_data(self):
        return self.bias_data.get_data()

    def get_circuit_parts(self):
        return self.__dict__

    @abstractmethod
    def calculate_bias(self): pass

    @abstractmethod
    def calculate_base_current(self): pass

    @abstractmethod
    def calculate_collector_current(self): pass

    @abstractmethod
    def calculate_emitter_current(self): pass

    @abstractmethod
    def calculate_collector_voltage(self): pass

    @abstractmethod
    def calculate_emitter_voltage(self): pass

    @abstractmethod
    def calculate_base_voltage(self): pass

    @abstractmethod
    def calculate_collector_emitter_voltage(self): pass

    @abstractmethod
    def calculate_input_impedance(self): pass

    @abstractmethod
    def calculate_output_impedance(self): pass

    @abstractmethod
    def calculate_voltage_gain(self): pass

    @abstractmethod
    def determine_q_point(self): pass
