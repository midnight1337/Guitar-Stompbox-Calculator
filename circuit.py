"""
Circuit is some kind of manager of the whole tool.
"""
from transistor import Transistor
from resistor import Resistor
from collector_feedback import CollectorFeedback
from voltage_divider import VoltageDivider


class Circuit(object):
    def __init__(self, transistors_blueprint: dict[str, dict[str, str | int]], resistors_blueprint: dict[str, int | float], vcc: int = 9):
        self.transistor: Transistor = Transistor(transistors_blueprint=transistors_blueprint)
        self.resistors: Resistor = Resistor(**resistors_blueprint)
        self.vcc = vcc

    def collector_feedback(self, model: str):
        CollectorFeedback(transistor=self.transistor(model=model), **self.resistors.collector_feedback(), vcc=self.vcc).calculate_and_read_values()

    def voltage_divider(self, model: str):
        VoltageDivider(transistor=self.transistor(model=model), **self.resistors.voltage_divider(), vcc=self.vcc).calculate_and_read_values()

    def collector_feedback_for_all_initialised_transistors(self):
        for q in self.transistor.transistors:
            CollectorFeedback(transistor=self.transistor(model=q), **self.resistors.collector_feedback(), vcc=self.vcc).calculate_and_read_values()
