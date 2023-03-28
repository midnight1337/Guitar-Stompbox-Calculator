"""
Transistor is initialised in Circuit class. It initialises and represents all transistors dataclasses(Bjt)
TransistorMeta is metaclass used to make sure, only one Transistor instance was initialised in Circuit.
"""
from bjt import Bjt


class TransistorMeta(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            raise Exception("Only one Transistor object is allowed!")


class Transistor(metaclass=TransistorMeta):
    def __init__(self):
        self.__transistors: dict = {}

    def __call__(self, model: str):
        """Can use object as function"""
        return self.__transistors[model]

    @property
    def transistor(self, model: str) -> dict:
        """TODO: Propery vs __call__??"""
        return self.__transistors[model]

    @property
    def transistors(self) -> dict:
        return self.__transistors

    def add_transistor(self, transistor: 'Bjt'):
        if transistor.model not in self.__transistors.keys():
            self.__transistors[transistor.model] = transistor

    def sort_transistors_by_name(self):
        # TODO: use some sorting algorithm (quick sort??)
        for model, transistor in self.__transistors:
            pass

    def sort_transistors_by_hfe(self):
        # TODO
        pass
