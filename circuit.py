"""
Date: 2023-05-11
Class: BiasCircuit
Description: This abstract class requires to pass parts necessary for circuit initialisation.
It is inherited in all bias related classes.
"""
from abc import ABC, abstractmethod
from transistor import Bjt
from bias_data import BiasData


class Circuit(ABC):
    def __init__(self, vcc: int, transistor: Bjt, rc: float, re: float):
        """
        :param vcc:
        :param transistor:
        :param rc:
        :param re:
        """
        self.vcc: int = vcc
        self.transistor: Bjt = transistor
        self.rc: float = rc
        self.re: float = re
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
