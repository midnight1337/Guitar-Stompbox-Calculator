import dataclasses


# order=True enables sorting objects by any value defined in __post_init__ assigned to sort_index
# frozen=True, read-only. It allows to make sure data is not changed anywhere in code
@dataclasses.dataclass(order=True, frozen=True)
class Bjt:
    # use it just as field for sorting, so you don't need to initialise it in object creation
    sort_index: int = dataclasses.field(init=False, repr=False)
    model: str
    hfe: int
    Vbe: float = 0.7

    def __post_init__(self):
        # self.sort_index = self.hfe      # can't assign it directly with frozen=True (it's 'read only
        object.__setattr__(self, 'sort_index', self.hfe)

    def __str__(self) -> str:
        return f"model: {self.model}, hfe: {self.hfe}, Vbe: {self.Vbe}, memory: {id(self)}"
