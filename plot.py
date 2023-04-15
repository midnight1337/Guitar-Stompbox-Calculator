from abc import ABC, abstractmethod
"""
Description: This class provides an interface for plotting graph of Q point
"""


class Plot(ABC):

    @abstractmethod
    def plot(self): pass
