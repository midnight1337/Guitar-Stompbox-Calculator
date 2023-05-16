"""
Author: Kamil Koltowski
E-mail: kamil.koltows@gmail.com
Description: This tool provides ability to do all calculations, necessary for designing guitar stomp-boxes circuits.
TODO:
1) Refactor whole code -> Should resistor.py be implemented with more layers of abstraction? (refer to capacitor.py)
2) Make bias circuits work ok with converting values
3) Add capacitor calculations
4) Plot q value
5) Plot capacitor values with frequency range, make few plots for some values or smth
6) Add other BJT bias circuits
7) Add JFET bias circuits
8) Add filters calculator (passive, active, baxandall, james, maybe marshall etc)
8) Deploy tool on website
-Add somewhere a SQL as database for transistors or saved data in tool
"""
from breadboard import Breadboard


# Voltage Divider:
#  {'Transistor': Bjt(model='2N3904', hfe=100, type='NPN', vbe=0.7, internal_emitter_voltage_drop=0.025), 'Ib [uA]': 44.736,
#  'Ic [mA]': 4.474, 'Ie [mA]': 4.518, 'Vc [V]': 6.632, 'Ve [V]': 0.984, 'Vb [V]': 1.684, 'Irbe [mA]': 0.468, 'Irbc [mA]': 0.513,
#  'Vce [V]': 5.648, 'Av [Gain]': 5.321, 'Z_in [KOhm]': 0.476, 'Z_out []': 1200.0, 'C_in []': 0.008, 'C_out []': 0.0, 'C_emitter []': 0.0,
#  'Q_point': {'Vce(bias)/Vce(cutoff) [V]': '[5.592/12]', 'Ic/Ic(sat) [mA]': '[4.513/8.451]'}, 'Voltage check': 1}
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
    breadboard = Breadboard()

    breadboard.breadboard_voltage_divider_circuit(model="2N2222")
    breadboard.calculate_voltage_divider_bias()
    breadboard.read_voltage_divider_bias_data()

    breadboard.breadboard_collector_feedback_circuit(model="2N2222")
    breadboard.calculate_collector_feedback_bias()


if __name__ == "__main__":
    main()
