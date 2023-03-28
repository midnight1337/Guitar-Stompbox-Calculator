class Resistor(object):
    def __init__(self, rb: float = None, rbc: float = None, rbe: float = None, rc: float = None, re: float = None, multiplier: int = 1):
        self.rb: float = rb
        self.rbc: float = rbc
        self.rbe: float = rbe
        self.rc: float = rc
        self.re: float = re
        self.multiplier: int = multiplier

    def __call__(self):
        # resistors = {k: v * self.multiplier for k, v in self.__dict__.items() if v is not None}
        return self.__dict__.items()

    @property
    def resistors(self):
        """TODO: Propery vs __call__??"""
        return self.__dict__.items()

    def determine_resistance(self):
        print(self.__dict__)
        for k, v in self.__dict__.items():
            if k != 'multiplier':
                if v is not None:
                    self.__dict__[f"{k}"] = v * self.multiplier

    def collector_feedback(self):
        return {"rb": self.rb, "rc": self.rc, "re": self.re}

    def voltage_divider(self):
        return {"rbc": self.rbc, "rbe": self.rbe, "rc": self.rc, "re": self.re}
