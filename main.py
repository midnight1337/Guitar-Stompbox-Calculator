"""
Author: Kamil Koltowski
E-mail: kamil.koltows@gmail.com
Description: This tool provides ability to do all calculations, necessary for designing guitar stomp-boxes circuits.
"""
from circuit import Circuit


transistors_blueprint = [
    ("2N2222", 60),
    ("2N2223", 200)
]

# transistors_blueprint = {
#     "2N2222": {
#         "model": "2N2222",
#         "hfe": 60
#     },
#     "2N2223": {
#         "model": "2N2223",
#         "hfe": 200
#     },
# }

# resistors_blueprint = {
#     "rb": 410,
#     "rc": 47,
#     "re": 0.1,
#     "rbc": 5.6,
#     "rbe": 6.8,
#     "multiplier": 10 ** 3
# }

resistors_blueprint = {
    "rb": 1,
    "rc": 3.9,
    "re": 3.3,
    "rbc": 10,
    "rbe": 4.7,
    "multiplier": 10 ** 3
}

if __name__ == "__main__":
    circuit = Circuit(transistors_blueprint=transistors_blueprint, resistors_blueprint=resistors_blueprint, vcc=15)
    circuit.collector_feedback(model="2N2222")
    circuit.voltage_divider(model="2N2223")
