"""
Resistor is initialised in Circuit class. It represents a resistors used in bias circuits.
ResistorMetaclass it's used as Singleton pattern, and to multiply resistor values by a multiplier.
"""
from abc import ABC, ABCMeta, abstractmethod
from parts import ResistorsBlueprint


class ResistorSingleton(ABCMeta):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is not None:
            raise Exception(f"Only one {cls.__name__} object is allowed!")
        else:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance


class ResistorsAbstract(ABC, metaclass=ResistorSingleton):

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
    """This class represents a callable resistors set, for desired circuit bias"""
    def __init__(self, resistors_blueprint: type(ResistorsBlueprint)):
        self.__resistors_blueprint: ResistorsBlueprint = resistors_blueprint()

    @property
    def voltage_divider_bias(self):
        """Return already created object which contains all resistors data"""
        return ResistorsVoltageDivider(**self.__resistors_blueprint.voltage_divider_bias).resistors

    @property
    def collector_feedback_bias(self):
        return ResistorsCollectorFeedback(**self.__resistors_blueprint.collector_feedback_bias).resistors
