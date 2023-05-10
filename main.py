"""
Author: Kamil Koltowski
E-mail: kamil.koltows@gmail.com
Description: This tool provides ability to do all calculations, necessary for designing guitar stomp-boxes circuits.
"""
from circuit import Breadboard
from transistor import Transistor
from resistor import Resistor
from parts import TransistorsBlueprint, ResistorsBlueprint, Vcc

# Voltage Divider:
#  {'Transistor': Bjt(model='2N3904', hfe=100, type='NPN', vbe=0.7, internal_emitter_voltage_drop=0.025), 'Ib [uA]': 44.736, 'Ic [mA]': 4.474, 'Ie [mA]': 4.518, 'Vc [V]': 6.632, 'Ve [V]': 0.984, 'Vb [V]': 1.684, 'Irbe [mA]': 0.468, 'Irbc [mA]': 0.513, 'Vce [V]': 5.648, 'Av [Gain]': 5.321, 'Z_in [KOhm]': 0.476, 'Z_out []': 1200.0, 'C_in []': 0.008, 'C_out []': 0.0, 'C_emitter []': 0.0, 'Q_point': {'Vce(bias)/Vce(cutoff) [V]': '[5.592/12]', 'Ic/Ic(sat) [mA]': '[4.513/8.451]'}, 'Voltage check': 1}
# hfe: 100, vbe: 0.7
# resistors_blueprint = {
#     "rb": 0.22,
#     "rc": 1.2,
#     "re": 0.22,
#     "rbc": 20,
#     "rbe": 3.6,
#     "multiplier": 10 ** 3
# }


def main():
    transistor = Transistor(transistors_blueprint=TransistorsBlueprint)
    resistor = Resistor(resistors_blueprint=ResistorsBlueprint)
    circuit = Breadboard(transistor=transistor, resistor=resistor, vcc=Vcc.VCC.value)
    circuit.calculate_voltage_divider_bias(model="2N2222")
    circuit.calculate_collector_feedback_bias(model="2N2222")


if __name__ == "__main__":
    main()
