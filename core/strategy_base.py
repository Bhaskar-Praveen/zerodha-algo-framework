from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def generate_signal(self, data):
        """
        Must return one of:
        BUY, SELL, HOLD
        """
        pass
