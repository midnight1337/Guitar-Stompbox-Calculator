"""
Author: Kamil Koltowski
E-mail: kamil.koltows@gmail.com
Description: This tool provides ability to do all calculations, necessary for designing guitar stomp-boxes circuits.
"""
from circuit import CircuitManager
from transistor import Transistor
from resistor import ResistorsCollectorFeedback, ResistorsVoltageDivider
from parts import TransistorsBlueprint, ResistorsBlueprint, Vcc


if __name__ == "__main__":
    transistors = Transistor(TransistorsBlueprint().transistors)
    resistors_voltage_divider = ResistorsVoltageDivider(**ResistorsBlueprint().resistors_voltage_divider)
    resistors_collector_feedback = ResistorsCollectorFeedback(**ResistorsBlueprint().resistors_collector_feedback)

    circuit = CircuitManager(transistors=transistors,
                             resistors_voltage_divider=resistors_voltage_divider,
                             resistors_collector_feedback=resistors_collector_feedback,
                             vcc=Vcc.VCC.value)
    circuit.calculate_voltage_divider(model="2N2222")
    circuit.calculate_collector_feedback(model="2N2222")

