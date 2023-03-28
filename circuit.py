"""
Circuit is some kind of manager of the whole tool.
"""
from transistor import Transistor
from resistor import Resistor
from collector_feedback import CollectorFeedback
from voltage_divider import VoltageDivider


class Circuit(object):
    def __init__(self, transistors_blueprint: list[tuple[str, int]], resistors_blueprint: dict[str, int | float]):
        self.transistor: Transistor = Transistor(transistors_blueprint=transistors_blueprint)
        self.resistors: Resistor = Resistor(**resistors_blueprint)

    def initialise_transistors(self):
        self.transistor.initialise_bjt_transistors()

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
