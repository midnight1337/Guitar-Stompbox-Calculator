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
from parts import CapacitorsBlueprint


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
    def __init__(self, ce: float, cc: float, cb: float):
        self.emitter_capacitor: float = ce
        self.collector_capacitor: float = cc
        self.base_capacitor: float = cb

    @property
    def emitter_capacitor(self) -> float:
        return self.emitter_capacitor

    @emitter_capacitor.setter
    def emitter_capacitor(self, capacitance: float):
        self.emitter_capacitor = capacitance

    @property
    def collector_capacitor(self) -> float:
        return self.emitter_capacitor

    @collector_capacitor.setter
    def collector_capacitor(self, capacitance: float):
        self.collector_capacitor.capacitance = capacitance

    @property
    def base_capacitor(self) -> float:
        return self.base_capacitor

    @base_capacitor.setter
    def base_capacitor(self, capacitance: float):
        self.base_capacitor.capacitance = capacitance

    @staticmethod
    def calculate_capacitance(frequency: int, reactance: float) -> float:
        """
        Calculate capacitor's value for given reactance and frequency
        :param frequency: Cutoff frequency
        :param reactance: Desired resistance at given frequency
        :return:
        """
        return 1 / (2 * pi * frequency * reactance)

    @staticmethod
    def calculate_reactance(frequency: int, capacitance: float) -> float:
        """
        Calculate capacitor's reactance at given frequency and capacitor's value
        :param frequency: Cutoff frequency
        :param capacitance: Capacitor's value
        :return:
        """
        if frequency == 0:
            return inf
        return 1 / (2 * pi * frequency * capacitance)


class CapacitorsVoltageDivider(CapacitorAbstract):
    def __init__(self, ce: float, cc: float, cb: float):
        super().__init__(ce=ce, cc=cc, cb=cb)


class CapacitorsCollectorFeedback(CapacitorAbstract):
    def __init__(self, ce: float, cc: float, cb: float):
        super().__init__(ce=ce, cc=cc, cb=cb)


class Capacitor:
    def __init__(self, capacitors_blueprint: type(CapacitorsBlueprint)):
        self.__capacitors: CapacitorsBlueprint = capacitors_blueprint()
        self.__capacitors_vd: CapacitorsVoltageDivider = CapacitorsVoltageDivider(**self.__capacitors.voltage_divider)
        self.__capacitors_cf: CapacitorsCollectorFeedback = CapacitorsCollectorFeedback(**self.__capacitors.collector_feedback)

    @property
    def voltage_divider(self):
        # return CapacitorsVoltageDivider(**self.__capacitors.voltage_divider)
        return self.__capacitors_vd

    @property
    def collector_feedback(self):
        return self.__capacitors_cf
