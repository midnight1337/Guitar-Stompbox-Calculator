"""
Resistor is initialised in Circuit class. It represents a resistors used in bias circuits.
ResistorMetaclass it's used as Singleton pattern, and to multiply resistor values by a multiplier.
"""
from abc import ABC, ABCMeta, abstractmethod


class ResistorSingleton(ABCMeta):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is not None:
            raise Exception(f"Only one {cls.__name__} object is allowed!")
        else:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance


class Resistor(ABC, metaclass=ResistorSingleton):

    @abstractmethod
    def __init__(self, rc: float, re: float):
        self.rc: float = rc
        self.re: float = re

    def __call__(self):
        return self.__class__.__name__

    @property
    def resistors(self):
        return self.__dict__


class ResistorsCollectorFeedback(Resistor):
    def __init__(self, rb: float, rc: float, re: float):
        super().__init__(rc=rc, re=re)
        self.rb = rb


class ResistorsVoltageDivider(Resistor):
    def __init__(self, rc: float, re: float, rbc: float, rbe: float):
        super().__init__(rc=rc, re=re)
        self.rbc: float = rbc
        self.rbe: float = rbe
