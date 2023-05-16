"""
Date: 2023-05-16
Class: CapacitorMeta
Description: Singleton pattern, only one object creation allowed.

Date: 2023-05-16
Class: CapacitorAbstract
Description:

Date: 2023-05-16
Class: CapacitorEmitter, CapacitorCollector, CapacitorBase
Description: Class name speaks for itself

Date: 2023-05-16
Class: Capacitor
Description: TODO: might not be done, similar to filters
"""
from abc import ABC, ABCMeta, abstractmethod
from math import pi, inf


class CapacitorMeta(ABCMeta):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is not None:
            raise Exception(f"Only one {cls.__name__} object is allowed!")
        else:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance


class CapacitorAbstract(ABC, metaclass=CapacitorMeta):
    @abstractmethod
    def __init__(self, capacitance: float):
        self.capacitance: float = capacitance

    @property
    def capacitance(self) -> float:
        return self.capacitance

    @capacitance.setter
    def capacitance(self, capacitance: float):
        self.capacitance = capacitance

    def calculate_capacitance(self, frequency: int, reactance: float) -> float:
        """
        :param frequency: Cutoff frequency
        :param reactance: Desired resistance at given frequency
        :return:
        """
        return 1 / (2 * pi * frequency * reactance)

    def calculate_reactance(self, frequency: int) -> float:
        if frequency == 0:
            return inf
        return 1 / (2 * pi * frequency * self.capacitance)


class EmitterCapacitor(CapacitorAbstract):
    def __init__(self, capacitance: float):
        super().__init__(capacitance=capacitance)


class CollectorCapacitor(CapacitorAbstract):
    def __init__(self, capacitance: float):
        super().__init__(capacitance=capacitance)


class BaseCapacitor(CapacitorAbstract):
    def __init__(self, capacitance: float):
        super().__init__(capacitance=capacitance)


class Capacitor:
    def __init__(self):
        self.emitter_capacitor = EmitterCapacitor.__new__(EmitterCapacitor)
        self.collector_capacitor = CollectorCapacitor.__new__(CollectorCapacitor)
        self.base_capacitor = BaseCapacitor.__new__(BaseCapacitor)

    @property
    def emitter_capacitor(self):
        return self.emitter_capacitor

    @emitter_capacitor.setter
    def emitter_capacitor(self, capacitance: float):
        self.emitter_capacitor.capacitance = capacitance

    @property
    def collector_capacitor(self):
        return self.emitter_capacitor

    @collector_capacitor.setter
    def collector_capacitor(self, capacitance: float):
        self.collector_capacitor.capacitance = capacitance

    @property
    def base_capacitor(self):
        return self.base_capacitor

    @base_capacitor.setter
    def base_capacitor(self, capacitance: float):
        self.base_capacitor.capacitance = capacitance
