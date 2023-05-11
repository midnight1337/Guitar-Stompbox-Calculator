"""
Circuit class is some kind of Manager. It acts like a real breadboard where you build a particular circuit, and
then you can measure your bias data.
"""
from transistor import Transistor
from resistor import Resistor
from voltage_divider_bias import VoltageDividerBias
from collector_feedback_bias import CollectorFeedbackBias


class Circuit(object):
    def __init__(self, transistor: Transistor, resistor: Resistor, vcc: int):
        self.vcc: int = vcc
        self.transistor: Transistor = transistor
        self.resistor: Resistor = resistor
        self.voltage_divider_bias: VoltageDividerBias = VoltageDividerBias.__new__(VoltageDividerBias)
        self.collector_feedback_bias: CollectorFeedbackBias = CollectorFeedbackBias.__new__(CollectorFeedbackBias)

    def breadboard_voltage_divider_bias(self, model: str):
        self.voltage_divider_bias.__init__(vcc=self.vcc, transistor=self.transistor(model=model),
                                           **self.resistor.voltage_divider_bias)

    def calculate_voltage_divider_bias(self):
        self.voltage_divider_bias.calculate()

    def breadboard_collector_feedback_bias(self, model: str):
        self.collector_feedback_bias.__init__(vcc=self.vcc, transistor=self.transistor(model=model),
                                              **self.resistor.collector_feedback_bias)

    def calculate_collector_feedback_bias(self):
        self.collector_feedback_bias.calculate()
