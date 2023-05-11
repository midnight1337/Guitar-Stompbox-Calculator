"""
Date: 2023-03-28
Class: Circuit
Description: Circuit class is some kind of Manager. It acts like a real breadboard where you build a particular circuit,
and then you measure your transistor biasing data.
"""
from transistor import Transistor
from resistor import Resistor
from parts import TransistorsBlueprint, ResistorsBlueprint, Vcc
from voltage_divider import VoltageDivider
from collector_feedback import CollectorFeedback


class Circuit(object):
    def __init__(self):
        self.vcc: int = Vcc.VCC.value
        self.transistor: Transistor = Transistor(transistors_blueprint=TransistorsBlueprint)
        self.resistor: Resistor = Resistor(resistors_blueprint=ResistorsBlueprint)
        self.voltage_divider: VoltageDivider = VoltageDivider.__new__(VoltageDivider)
        self.collector_feedback: CollectorFeedback = CollectorFeedback.__new__(CollectorFeedback)

    def breadboard_voltage_divider_bias(self, model: str):
        self.voltage_divider.__init__(vcc=self.vcc, transistor=self.transistor(model=model),
                                      **self.resistor.voltage_divider)

    def calculate_voltage_divider_bias(self):
        self.voltage_divider.calculate()

    def breadboard_collector_feedback_bias(self, model: str):
        self.collector_feedback.__init__(vcc=self.vcc, transistor=self.transistor(model=model),
                                         **self.resistor.collector_feedback)

    def calculate_collector_feedback_bias(self):
        self.collector_feedback.calculate()
