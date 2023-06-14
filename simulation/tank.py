from dataclasses import dataclass
import json
from controller.PID_controller import PID_Params, control_action
from model.tank_model import Tank
import numpy as np
from scipy.integrate import odeint

default_data = "../data/thermal_model.json"


def load_params(file: str = default_data) -> PID_Params:
    with open(file, 'r') as f:
        data = json.load(f)
    params = PID_Params(**data['control'])
    return params


@dataclass
class Report:
    fluid_temperature: np.ndarray
    resistence_temperature: np.ndarray
    control_action: np.ndarray


class Simulator:
    def __init__(self):
        self.control_params = load_params()
        self.model = Tank()

    def simulate(self, horizon: int = 5, step_by_sampling: int=5) -> Report:
        error = self.control_params.SP - self.model.initial_values.T0
        last_error = self.control_params.SP - self.model.initial_values.T0
        current_action = self.model.initial_values.Q_bar.value
        last_I = 0

        T0 = self.model.initial_values.T0.value
        Tr0 = self.model.initial_values.Tr0.value

        current_time = 0
        end = horizon * self.control_params.dt
        registers = []
        control_actions = []
        while current_time < end:
            new_action = control_action(
                error=error,
                last_error=last_error,
                pid_params=self.control_params,
                last_I=last_I,
                current_action=current_action
            )
            end_interval = current_time + self.control_params.dt.value
            t = np.linspace(current_time, end_interval, num=step_by_sampling)
            M = odeint(self.model.measured_variable, [T0, Tr0], t, args=(new_action,))
            registers.append(M)
            control_actions.append(new_action)

            T0 = M[-1:, 0][0]
            Tr0 = M[-1:, 1][0]
            current_time += self.control_params.dt.value

        report = Report(
            fluid_temperature=M[:,0],
            resistence_temperature=M[:,1],
            control_action=control_actions
        )

        return report


if __name__ == "__main__":
    simulator = Simulator()
    report = simulator.simulate(horizon=1)
    print(report)





