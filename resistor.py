class Resistor(object):
    def __init__(self, rb, rc, re, multiplier):
        self.rb = rb * multiplier
        self.rc = rc * multiplier
        self.re = re * multiplier

    def __call__(self):
        return {"rb": self.rb, "rc": self.rc, "re": self.re}

    @property
    def resistors(self):
        return {"rb": self.rb, "rc": self.rc, "re": self.re}
