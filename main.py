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

def calculate_input_impedance_detailed():
    """
    Formula: Z_in = Xc_in(f) + ( (R1 || R2) || (re' + (Re || Xc_e(f))) )
    :return:
    """
    frequency_range = 1000
    c_in = 1
    c_e = 22
    r1 = 90000
    r2 = 22000
    transistor_re = 25  # calculate it with emitter current
    hfe = 100
    re = 1500
    result = []

    def calculate_xc(frequency, capacitance):
        capacitance = capacitance / 1000000
        xc = 1 / (2 * 3.14 * frequency * capacitance)
        print(xc)
        return xc

    def calculate_z_in():
        for f in range(1, frequency_range):
            xc_in = calculate_xc(f, c_in)
            xc_e = calculate_xc(f, c_e)

            a = (r1*r2)/(r1+r2)
            b = (((re * xc_e)/(re + xc_e)) + transistor_re) * hfe
            c = (a*b)/(a+b)
            formula = (xc_in + c)
            result.append(formula)

    calculate_z_in()
    print(result)

def main():
    calculate_input_impedance_detailed()
    # breadboard = Breadboard()
    #
    # breadboard.breadboard_voltage_divider_circuit(model="2N2222")
    # breadboard.calculate_voltage_divider_bias()
    # breadboard.read_voltage_divider_bias_data()
    #
    # breadboard.breadboard_collector_feedback_circuit(model="2N2222")
    # breadboard.calculate_collector_feedback_bias()


if __name__ == "__main__":
    main()
