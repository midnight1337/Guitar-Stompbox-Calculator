"""
Circuit is some kind of manager of the whole tool.
"""
from abc import ABC, abstractmethod
from collector_feedback import CollectorFeedback
from voltage_divider import VoltageDivider


class Circuit(ABC):
    def __init__(self, transistor: 'Bjt', resistors: dict[str, int | float], vcc: int):
        self.vcc: int = vcc
        self.transistor: 'Bjt' = transistor
        self.resistors: dict[str, int | float] = resistors

    @abstractmethod
    def calculate(self): pass


class CircuitVoltageDivider(Circuit):
    def __init__(self, transistor: 'Bjt', resistors: dict[str, int | float], vcc: int):
        super().__init__(transistor=transistor, resistors=resistors, vcc=vcc)

    def calculate(self):
        voltage_divider: VoltageDivider = VoltageDivider(transistor=self.transistor, vcc=self.vcc, **self.resistors)
        voltage_divider.calculate()


class CircuitCollectorFeedback(Circuit):
    def __init__(self, transistor: 'Bjt', resistors: dict[str, int | float], vcc: int):
        super().__init__(transistor=transistor, resistors=resistors, vcc=vcc)

    def calculate(self):
        collector_feedback: CollectorFeedback = CollectorFeedback(transistor=self.transistor, vcc=self.vcc,
                                                                  **self.resistors)
        collector_feedback.calculate()


class CircuitManager(object):
    def __init__(self, transistors: 'Bjt', resistors_voltage_divider: 'Resistor', resistors_collector_feedback: 'Resistor', vcc: int):
        self.vcc: int = vcc
        self.transistors: 'Bjt' = transistors
        self.resistors_voltage_divider: 'Resistor' = resistors_voltage_divider
        self.resistors_collector_feedback: 'Resistor' = resistors_collector_feedback
        self.voltage_divider: CircuitVoltageDivider = CircuitVoltageDivider.__new__(CircuitVoltageDivider)
        self.collector_feedback: CircuitCollectorFeedback = CircuitCollectorFeedback.__new__(CircuitCollectorFeedback)

    def calculate_voltage_divider(self, model: str, vcc: int = None):
        if not vcc:
            vcc = self.vcc
        self.voltage_divider.__init__(transistor=self.transistors(model=model),
                                      resistors=self.resistors_voltage_divider.resistors,
                                      vcc=vcc)
        self.voltage_divider.calculate()

    def calculate_collector_feedback(self, model: str, vcc: int = None):
        if not vcc:
            vcc = self.vcc
        self.collector_feedback.__init__(transistor=self.transistors(model=model),
                                         resistors=self.resistors_collector_feedback.resistors,
                                         vcc=vcc)
        self.collector_feedback.calculate()
