"""
Date: 2023-03-28
Description: This file provides a different levels of resistors abstraction.

Class: ResistorMeta
Description: It's a Singleton pattern class, which allows only ONE object creation of inherited classes.

Class: ResistorsAbstract
Description: It provides an interface for particular circuit's resistors.

Class: ResistorsCollectorFeedback
Description: Contains resistors needed for Collector Feedback circuit.

Class: ResistorsVoltageDivider
Description: Contains resistors needed for Voltage Divider circuit.

Class: Resistor
Description: It provides resistor values for desired bias circuit. It's Initialised in Circuit class.
"""
from abc import ABC, ABCMeta, abstractmethod
from parts import ResistorsBlueprint


class ResistorMeta(ABCMeta):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is not None:
            raise Exception(f"Only one {cls.__name__} object is allowed!")
        else:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance


class ResistorsAbstract(ABC, metaclass=ResistorMeta):
    @abstractmethod
    def __init__(self, rc: float, re: float):
        self.rc: float = rc
        self.re: float = re

    @property
    def resistors(self):
        return self.__dict__

    def __call__(self):
        return self.__class__.__name__


class ResistorsCollectorFeedback(ResistorsAbstract):
    def __init__(self, rb: float, rc: float, re: float):
        super().__init__(rc=rc, re=re)
        self.rb: float = rb


class ResistorsVoltageDivider(ResistorsAbstract):
    def __init__(self, rc: float, re: float, rbc: float, rbe: float):
        super().__init__(rc=rc, re=re)
        self.rbc: float = rbc
        self.rbe: float = rbe


class Resistor(object):
    def __init__(self, resistors_blueprint: type(ResistorsBlueprint)):
        """
        :param resistors_blueprint:
        """
        self.__resistors: ResistorsBlueprint = resistors_blueprint()
        self.__resistors_vd: ResistorsVoltageDivider = ResistorsVoltageDivider(**self.__resistors.voltage_divider)
        self.__resistors_cf: ResistorsCollectorFeedback = ResistorsCollectorFeedback(**self.__resistors.collector_feedback)

    @property
    def voltage_divider(self):
        return self.__resistors_vd.resistors

    @property
    def collector_feedback(self):
        return self.__resistors_cf.resistors
