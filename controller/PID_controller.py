import json
from dataclasses import dataclass, fields
from data.variable import Variable

default_data = "../data/thermal_model.json"


@dataclass
class PID_Params:
    Kc: Variable
    Taui: Variable
    Taud: Variable
    SP: Variable
    dt: Variable

    def __post_init__(self):
        for field in fields(self):
            data = getattr(self, field.name)
            setattr(self, field.name, Variable(**data))


def control_action(
        error,
        last_error,
        pid_params: PID_Params,
        last_I,
        current_action
):
    P = error
    I = error * pid_params.dt + last_I
    D = (error - last_error)/pid_params.dt.value

    # PID equation
    new_action = current_action + pid_params.Kc * (P + (1/pid_params.Taui.value)*I + pid_params.Taud.value*D)
    return new_action

