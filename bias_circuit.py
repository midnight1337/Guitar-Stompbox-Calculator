"""
Date: 2023-05-11
Class: BiasCircuit
Description: This abstract class requires to pass parts necessary for circuit initialisation.
It is inherited in all bias related classes.
"""
from abc import ABC, abstractmethod
from transistor import Bjt


class BiasCircuit(ABC):
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

    def __str__(self):
        return self.__class__.__name__

    @abstractmethod
    def read_calculated_data(self): pass

    @abstractmethod
    def calculate(self): pass

    def circuit_parts(self):
        return self.__dict__
