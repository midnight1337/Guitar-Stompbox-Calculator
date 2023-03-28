"""
Author: Kamil Koltowski
E-mail: kamil.koltows@gmail.com
Description: This tool provides ability to do all calculations for designing guitar stompboxes.
"""
from circuit import Circuit

transistors_blueprint = [
    ("2N2222", 60),
    ("2N2223", 100)
]

resistors_blueprint = {
    "rb": 410,
    # "rc": 47,
    # "re": 0.1,
    # "multiplier": 10 ** 3
    "rbc": 30,
    "rbe": 20.9,
    "rc": 0.15,
    "re": 0.15,
    "multiplier": 10 ** 3
}

if __name__ == "__main__":
    circuit = Circuit(transistors_blueprint=transistors_blueprint, resistors_blueprint=resistors_blueprint)
    circuit.initialise_transistors()
    circuit.determine_resistance()
    circuit.collector_feedback(model="2N2222")
    circuit.voltage_divider(model="2N2222")
