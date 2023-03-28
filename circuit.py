"""
Circuit is some kind of manager of the whole tool.
"""
from transistor import Transistor
from bjt import Bjt
from resistor import Resistor
from collector_feedback import CollectorFeedback
from voltage_divider import VoltageDivider


class Circuit(object):
    def __init__(self, transistors_blueprint: list, resistors_blueprint: dict):
        self.transistor: Transistor = Transistor()
        self.transistors_blueprint: list = transistors_blueprint
        self.resistors: Resistor = Resistor(**resistors_blueprint)

    def initialise_transistors(self):
        # TODO: Move it to transistor class, initialise Bjt there
        for q in self.transistors_blueprint:
            self.transistor.add_transistor(transistor=Bjt(*q))

    def determine_resistance(self):
        self.resistors.determine_resistance()

    def collector_feedback(self, model: str):
        collector_feedback = CollectorFeedback(transistor=self.transistor(model=model), **self.resistors.collector_feedback())
        collector_feedback.calculate_and_save_values()
        collector_feedback.read_documentation()

    def voltage_divider(self, model: str):
        voltage_divider = VoltageDivider(transistor=self.transistor(model=model), **self.resistors.voltage_divider())
        voltage_divider.calculate()
        voltage_divider.read_documentation()

    def collector_feedback_for_all_initialised_transistors(self):
        for q in self.transistor.transistors:
            collector_feedback = CollectorFeedback(transistor=self.transistor(model=q), **self.resistors.collector_feedback())
            collector_feedback.calculate_and_save_values()
            collector_feedback.read_documentation()
