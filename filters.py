"""
Date: 2023-04-14
Description: This file provides classes responsible for filters calculation.
"""
from abc import ABC, abstractmethod
from plot import Plot
from math import pi


class FilterAbstract(ABC):
    @abstractmethod
    def __init__(self, cutoff_frequency):
        self.cutoff_frequency: int = cutoff_frequency

    def calculate_cutoff_frequency(self, capacitance, reactance):
        return 1 / (2 * pi * capacitance * reactance)

    def plot_cutoff_frequency(self): pass


class PassiveLowPassFilter(object):
    pass


class PassiveHighPassFilter(FilterAbstract):
    def __init__(self, cutoff_frequency):
        super().__init__(cutoff_frequency=cutoff_frequency)


class ActiveLowPassFilter:
    pass


class ActiveHighPassFilter:
    pass


class BaxandallFilter:
    pass


class JamesStackFilter:
    pass


class Filter:
    def __init__(self):
        self.passive_hp_filter = PassiveHighPassFilter.__new__(PassiveHighPassFilter)
