from dataclasses import dataclass, field
from enum import Enum


class Vcc(Enum):
    VCC = 12


@dataclass
class TransistorsBlueprint:
    """This dataclass acts like a datasheet for transistors"""
    transistors: dict[str, dict[str, str | int]] = field(default_factory=lambda: {
        "2N2222": {
            "model": "2N2222",
            "hfe": 100,
            "type": "NPN"
        },
        "2N2223": {
            "model": "2N2223",
            "hfe": 100,
            "type": "NPN"
        },
    }
                                                         )


@dataclass
class ResistorsBlueprint:
    MULTIPLIER = 10 ** 3

    voltage_divider_bias: dict[str, int | float] = field(default_factory=lambda: {
        "rc": 1.2,
        "re": 0.22,
        "rbc": 20,
        "rbe": 3.6
    }
                                                         )
    collector_feedback_bias: dict[str, int | float] = field(default_factory=lambda: {
        "rb": 410,
        "rc": 47,
        "re": 0.1,
    }
                                                            )

    def __post_init__(self):
        for k, v in self.voltage_divider_bias.items():
            self.voltage_divider_bias[k] = v * self.MULTIPLIER
        for k, v in self.collector_feedback_bias.items():
            self.collector_feedback_bias[k] = v * self.MULTIPLIER
