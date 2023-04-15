"""
Description: This class provides an smth, to be refactored
"""


class Description:
    def __init__(self):
        self.description = {}

    @property
    def description(self) -> dict:
        return self.description

    @description.setter
    def description(self, description):
        self.description = description

    def make_docs_more_readable(self, transistor: 'Transistor', ib: float, ic: float, ie: float, vb: float, vc: float, ve: float,
                            zin: float, av: float, q_point: dict):
        self.documentation = {
            "Transistor": transistor,
            "Ib [uA]": ib * 1000000,
            "Ic [mA]": ic * 1000,
            "Ie [mA]": ie * 1000,
            "Vb [V]": vb,
            "Vc [V]": vc,
            "Ve [V]": ve,
            "Zin [KOhm]": zin / 1000,
            "Av(gain) [V]": av,
            "Q_point": q_point
        }

        for k, v in self.documentation.items():
            if k == "Q_point" or type(v) is type(self.transistor):
                continue
            self.documentation[k] = round(v, 3)

        # self.documentation = {k: round(v, 3) for k, v in self.documentation.items()}
