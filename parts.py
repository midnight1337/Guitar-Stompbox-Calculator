from dataclasses import dataclass, field
from enum import Enum


class Vcc(Enum):
    VCC = 12


@dataclass
class TransistorsBlueprint:
    transistors: dict[str, dict[str, str | int]] = field(default_factory=lambda: {
        "2N2222": {
            "model": "2N2222",
            "hfe": 60
        },
        "2N2223": {
            "model": "2N2223",
            "hfe": 100
        },
    }
                                                         )


@dataclass
class ResistorsBlueprint:
    MULTIPLIER = 10 ** 3

    resistors_voltage_divider: dict[str, int | float] = field(default_factory=lambda: {
        "rc": 1,
        "re": 1,
        "rbc": 1,
        "rbe": 1
    }
                                                 )
    resistors_collector_feedback: dict[str, int | float] = field(default_factory=lambda: {
        "rb": 410,
        "rc": 47,
        "re": 0.1,
    }
                                                 )

    def __post_init__(self):
        for k, v in self.resistors_voltage_divider.items():
            self.resistors_voltage_divider[k] = v * self.MULTIPLIER
        for k, v in self.resistors_collector_feedback.items():
            self.resistors_collector_feedback[k] = v * self.MULTIPLIER
