from dataclasses import dataclass


@dataclass
class Variable:
    unit: str
    value: float
    meaning: str

    def __mul__(self, other):
        return self.value * other.value

    def __rmul__(self, other):
        return self.value * other

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        if isinstance(other, Variable):
            return self.value - other.value
        return self.value - other
