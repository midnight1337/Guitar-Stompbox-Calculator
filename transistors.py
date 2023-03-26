class TransistorMeta(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance  # Bez tego obiekt Transistor jest NoneTyype, dlaczego??
        else:
            raise Exception("Only one Transistor object is allowed!")


class Transistor(metaclass=TransistorMeta):
    def __init__(self):
        self.__transistors: dict = {}

    def __call__(self, model: str):
        """Can use object as function"""
        return self.__transistors[model]

    @property
    def transistors(self) -> dict:
        return self.__transistors

    def add_transistor(self, transistor: 'Bjt'):
        if transistor.model not in self.__transistors.keys():
            self.__transistors[transistor.model] = transistor

    def sort_transistors_by_name(self):
        for model, transistor in self.__transistors:
            pass

    def sort_transistors_by_hfe(self):
        pass


# class BMeta(type):
#     __instance = None
#
#     def __call__(cls, *args, **kwargs):
#         if cls.__instance is None:
#             cls.__instance = super().__call__(*args, **kwargs)
#             return cls.__instance
#         else:
#             raise Exception("Only one object is allowed!")
#
#
# class A(metaclass=BMeta):
#     def __str__(self):
#         return str(type(self))
#
#
# a = A()
# print(a)
# Output gdy linijka 42 odkomentowana: <class '__main__.A'>
# Output gdy linijka 42 zakomentowana: None>
