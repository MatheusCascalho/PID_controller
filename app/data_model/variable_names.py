from enum import Enum


class Scope(str, Enum):
    CONTROL = "control"
    MODEL = "model"


class ThermalModel(str, Enum):
    FLUID = "fluid"
    RESISTANCE = "resistance"
    INITIAL_VALUES = "initial_values"


class ModelVariableName(str, Enum):
    DENSITY = "rho"
    FLOW = "q"
    SPECIFIC_HEAT = "cp"
    TEMPERATURE = "T"
    VOLUME = "V"
    CONVECTIVE_COEFFICIENT = "h"
    AREA = "A"
    INITIAL_TEMPERATURE = "T0"
    INITIAL_RESISTANCE_TEMPERATURE = "Tr0"
    INITIAL_ELECTRIC_POWER = "Q_bar"


class ControlVariableName(str, Enum):
    SET_POINT = "SP"
    TIME_INTERVAL = "dt"
    PROPORTIONAL_GAIN = "Kc"
    INTEGRATIVE_GAIN = "Taui"
    DERIVATIVE_GAIN = "Taud"
