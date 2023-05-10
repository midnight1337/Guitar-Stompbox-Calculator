"""
Circuit is some kind of manager of the whole tool.
"""
from abc import ABC, abstractmethod
from collector_feedback import CollectorFeedback
from voltage_divider import VoltageDivider, VoltageDividerDataclass
from transistor import Transistor, Bjt
from resistor import Resistor


class Circuit(ABC):
    """This abstract class requires to pass parts necessary for circuit initialisation"""

    def __init__(self, transistor: Bjt, resistors: dict[str, int | float], vcc: int):
        self.transistor: Bjt = transistor
        self.resistors: dict[str, int | float] = resistors
        self.vcc: int = vcc

    @abstractmethod
    def read_circuit_data(self): pass

    @abstractmethod
    def calculate(self): pass


class CircuitVoltageDivider(Circuit):
    def __init__(self, transistor: Bjt, resistors: dict[str, int | float], vcc: int):
        super().__init__(transistor=transistor, resistors=resistors, vcc=vcc)

    def read_circuit_data(self):
        return VoltageDividerDataclass

    def calculate(self):
        voltage_divider: VoltageDivider = VoltageDivider(transistor=self.transistor, vcc=self.vcc, **self.resistors)
        voltage_divider.calculate()


class CircuitCollectorFeedback(Circuit):
    def __init__(self, transistor: Bjt, resistors: dict[str, int | float], vcc: int):
        super().__init__(transistor=transistor, resistors=resistors, vcc=vcc)

    def read_circuit_data(self):
        pass

    def calculate(self):
        collector_feedback: CollectorFeedback = CollectorFeedback(transistor=self.transistor, vcc=self.vcc,
                                                                  **self.resistors)
        collector_feedback.calculate()


class Breadboard(object):
    """This class is some kind of Manager. It acts like a real breadboard where you build a particular circuit"""
    def __init__(self, transistor: Transistor, resistor: Resistor, vcc: int):
        self.vcc: int = vcc
        self.transistor: Transistor = transistor
        self.resistor: Resistor = resistor
        self.voltage_divider: CircuitVoltageDivider = CircuitVoltageDivider.__new__(CircuitVoltageDivider)
        self.collector_feedback: CircuitCollectorFeedback = CircuitCollectorFeedback.__new__(CircuitCollectorFeedback)

    def calculate_voltage_divider_bias(self, model: str):
        self.voltage_divider.__init__(transistor=self.transistor(model=model),
                                      resistors=self.resistor.voltage_divider_bias,
                                      vcc=self.vcc)
        self.voltage_divider.calculate()

    def calculate_collector_feedback_bias(self, model: str):
        self.collector_feedback.__init__(transistor=self.transistor(model=model),
                                         resistors=self.resistor.collector_feedback_bias,
                                         vcc=self.vcc)
        self.collector_feedback.calculate()
