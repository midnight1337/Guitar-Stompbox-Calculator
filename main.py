"""
Author: Kamil Koltowski
E-mail: kamil.koltows@gmail.com
Description: This tool provides ability to do all calculations for designing guitar stompboxes.
"""
from circuit import Circuit

transistors_blueprint = [
    ("2N2222", 100),
    ("2N2223", 100)
]

resistors_blueprint = {
    "rb": 410,
    "rbc": 5.6,
    "rbe": 6.8,
    "rc": 10,
    "re": 4.7,
    "multiplier": 10 ** 3
}

if __name__ == "__main__":
    circuit = Circuit(transistors_blueprint=transistors_blueprint, resistors_blueprint=resistors_blueprint)
    circuit.collector_feedback(model="2N2222")
    circuit.voltage_divider(model="2N2222")
