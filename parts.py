"""
Date: 2023-04-15
Description: This file provides classes that represents a particular parts in a real circuit.

Class: Vcc
Description: Voltage Supply value

Class: TransistorsBlueprint
Description: Blueprint for all transistor models

Class: ResistorsBlueprint
Description: Blueprint for resistors in particular bias circuits.

Class: CapacitorsBlueprint
Description: Blueprint for capacitors in circuit
"""
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
            "type": "NPN",
            "vbe": 0.7
        },
        "2N2223": {
            "model": "2N2223",
            "hfe": 100,
            "type": "NPN"
        },
    })

    jfet: dict = field(default_factory=lambda: {None: None})


@dataclass
class ResistorsBlueprint:
    """
    MULTIPLIER = 1000 stands for KOhm
    """
    MULTIPLIER = 10 ** 3

    voltage_divider: dict[str, int | float] = field(default_factory=lambda: {
        "rc": 1.2,
        "re": 0.22,
        "rbc": 20,
        "rbe": 3.6
    })

    collector_feedback: dict[str, int | float] = field(default_factory=lambda: {
        "rb": 410,
        "rc": 47,
        "re": 0.1,
    })

    def __post_init__(self):
        for k, v in self.voltage_divider.items():
            self.voltage_divider[k] = v * self.MULTIPLIER
        for k, v in self.collector_feedback.items():
            self.collector_feedback[k] = v * self.MULTIPLIER


@dataclass
class CapacitorsBlueprint:
    """
    MULTIPLIER = 1 stands for 1uF
    """
    MULTIPLIER = 1
    voltage_divider = {
        "ce": 22,
        "cc": 1,
        "cb": 1
    }

    collector_feedback = {
        "ce": 22,
        "cc": 1,
        "cb": 1
    }

    def __post_init__(self):
        for k, v in self.voltage_divider.items():
            self.voltage_divider[k] = v * self.MULTIPLIER
        for k, v in self.collector_feedback.items():
            self.collector_feedback[k] = v * self.MULTIPLIER
