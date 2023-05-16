"""
Date: 2023-04-14
Description: This class provides an interface for plotting graph of Q point, filters etc.
"""
from abc import ABC, abstractmethod


class Plot(ABC):

    @abstractmethod
    def plot(self): pass
