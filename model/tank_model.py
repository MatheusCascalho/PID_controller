"""
Thermal model of a tank with a fluid and a resistance to control its temperature
"""

import json
from dataclasses import dataclass, fields

default_data = "../data/thermal_model.json"

@dataclass
class TemperatureRate:
    fluid: float
    resistence: float


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


@dataclass
class ResistenceModel:
    rho: Variable
    V: Variable
    cp: Variable
    hr: Variable
    Ar: Variable

    def __post_init__(self):
        for field in fields(self):
            data = getattr(self, field.name)
            setattr(self, field.name, Variable(**data))

    def heat_loss(self, T_diff):
        loss = self.hr * self.Ar * T_diff
        return loss

    def entropy(self):
        ent = self.rho * self.V * self.cp
        return ent


@dataclass
class FluidModel:
    rho: Variable
    V: Variable
    cp: Variable
    q: Variable
    T: Variable

    def __post_init__(self):
        for field in fields(self):
            data = getattr(self, field.name)
            setattr(self, field.name, Variable(**data))

    def enthalpy(self, T):
        ent = self.rho * self.q * self.cp * (self.T - T)
        return ent

    def entropy(self):
        ent = self.rho * self.V * self.cp
        return ent

@dataclass
class InitialValues:
    T0: Variable
    Tr0: Variable
    Q_bar: Variable

    def __post_init__(self):
        for field in fields(self):
            data = getattr(self, field.name)
            setattr(self, field.name, Variable(**data))


def load_model(file: str = default_data) -> tuple[FluidModel, ResistenceModel, InitialValues]:
    with open(file, 'r') as f:
        data = json.load(f)
    fluid = FluidModel(**data['model']['fluid'])
    resistence = ResistenceModel(**data['model']['resistence'])
    initial_values = InitialValues(**data['model']['initial_values'])
    return fluid, resistence, initial_values


def tank_temperature_rate(M, t) -> tuple[float, float]:
    T, Tr = M
    fluid, resistence, initial_values = load_model()
    T_diff = Tr - T
    dT_dt = (fluid.enthalpy(T) + resistence.heat_loss(T_diff))/fluid.entropy()
    dTr_dt = (initial_values.Q_bar - resistence.heat_loss(T_diff))/resistence.entropy()
    return dT_dt, dTr_dt


if __name__ == "__main__":
    import numpy as np
    from scipy.integrate import odeint
    data = load_model()
    initial_values = data[2]
    T0 = initial_values.T0.value
    Tr0 = initial_values.Tr0.value
    t = np.linspace(0, 100, num=100)
    M = odeint(tank_temperature_rate, [T0, Tr0], t)
