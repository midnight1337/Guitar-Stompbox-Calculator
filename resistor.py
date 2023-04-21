"""
Resistor is initialised in Circuit class. It represents a resistors used in bias circuits.
ResistorMetaclass it's used as Singleton pattern, and to multiply resistor values by a multiplier.
"""


class ResistorMeta(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is not None:
            raise Exception("Only one Resistor object is allowed!")
        else:
            for k in kwargs:
                kwargs[k] = kwargs[k] * kwargs['multiplier']
            kwargs.pop('multiplier')
            return super().__call__(*args, **kwargs)


class Resistor(metaclass=ResistorMeta):
    def __init__(self, rb: float = None, rbc: float = None, rbe: float = None, rc: float = None, re: float = None, multiplier: int = 1):
        self.rb: float = rb
        self.rbc: float = rbc
        self.rbe: float = rbe
        self.rc: float = rc
        self.re: float = re

    def __call__(self):
        # resistors = {k: v * self.multiplier for k, v in self.__dict__.items() if v is not None}
        return self.__dict__.items()

    @property
    def resistors(self):
        """TODO: Propery vs __call__??"""
        return self.__dict__.items()

    def collector_feedback(self) -> dict[str, float]:
        return {"rb": self.rb, "rc": self.rc, "re": self.re}

    def voltage_divider(self) -> dict[str, float]:
        return {"rbc": self.rbc, "rbe": self.rbe, "rc": self.rc, "re": self.re}
