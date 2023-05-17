"""
Date: 2023-03-28
Class: Circuit
Description: Circuit class is some kind of Manager. It acts like a real breadboard where you build a particular circuit,
and then you measure your transistor biasing data.
"""
from transistor import Transistor
from resistor import Resistor
from capacitor import Capacitor
from parts import TransistorsBlueprint, ResistorsBlueprint, CapacitorsBlueprint, Vcc
from voltage_divider import VoltageDivider
from collector_feedback import CollectorFeedback


class Breadboard(object):
    def __init__(self):
        self.vcc: int = Vcc.VCC.value
        self.transistor: Transistor = Transistor(transistors_blueprint=TransistorsBlueprint)
        self.resistor: Resistor = Resistor(resistors_blueprint=ResistorsBlueprint)
        self.capacitor: Capacitor = Capacitor(capacitors_blueprint=CapacitorsBlueprint)

        self.voltage_divider: VoltageDivider = VoltageDivider.__new__(VoltageDivider)
        self.collector_feedback: CollectorFeedback = CollectorFeedback.__new__(CollectorFeedback)

    def breadboard_voltage_divider_circuit(self, model: str):
        self.voltage_divider.__init__(vcc=self.vcc, transistor=self.transistor(model=model),
                                      **self.resistor.voltage_divider)

    def calculate_voltage_divider_bias(self):
        self.voltage_divider.calculate_bias()

    def read_voltage_divider_bias_data(self):
        print(self.voltage_divider.get_bias_data())

    def breadboard_collector_feedback_circuit(self, model: str):
        self.collector_feedback.__init__(vcc=self.vcc, transistor=self.transistor(model=model),
                                         **self.resistor.collector_feedback)

    def calculate_collector_feedback_bias(self):
        self.collector_feedback.calculate()

    def read_collector_feedback_bias_data(self):
        self.collector_feedback.read_calculated_data()
