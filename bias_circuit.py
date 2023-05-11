"""
This abstract class requires to pass parts necessary for circuit initialisation
"""
from abc import ABC, abstractmethod
from transistor import Bjt


class BiasCircuit(ABC):
    def __init__(self, vcc: int, transistor: Bjt, rc: float, re: float):
        self.vcc: int = vcc
        self.transistor: Bjt = transistor
        self.rc: float = rc
        self.re: float = re

    @abstractmethod
    def read_circuit_data(self): pass

    @abstractmethod
    def calculate(self): pass

    def __str__(self):
        return self.__class__.__name__

    def circuit_parts(self):
        return self.__dict__
