from app.data_model.data_model import (
    ModelVariableContainer,
    ControlVariableContainer,
    SimulationParameters
)
from datetime import datetime
from flask import Flask, request
from flask_pydantic_spec import (
    FlaskPydanticSpec,
    Response,
    Request
)
from simulation.tank import Report, Simulator
from typing import List
from tinydb import TinyDB
import json

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Controlador PID')
spec.register(server)
db_model_updates = TinyDB('model_updates.json')
db_control_updates = TinyDB('control_updates.json')


tank_model_data = '../data/thermal_model.json'
def save_model(data):
    with open(tank_model_data, 'w') as tank_model:
        json.dump(data, tank_model, ensure_ascii=False, indent=2)


@server.post('/update_model')
@spec.validate(body=Request(ModelVariableContainer), resp=Response(HTTP_200=ModelVariableContainer))
def update_model():
    body: ModelVariableContainer = request.context.body

    with open(tank_model_data, 'r') as tank_model:
        data = json.load(tank_model)
    full_model = data['model']
    for variable in body.variables:
        model = variable.model.value
        name = variable.name.value
        last_value = full_model[model][name]['value']
        setattr(variable, "last_value", last_value)
        full_model[model][name]['value'] = variable.value

    save_model(data)

    body = body.dict()
    body['time'] = str(datetime.now().date()) + ' ' + str(datetime.now().time())

    db_model_updates.insert(body)
    return body


@server.post('/update_control')
@spec.validate(body=Request(ControlVariableContainer), resp=Response(HTTP_200=ControlVariableContainer))
def update_control():
    body: ControlVariableContainer = request.context.body

    with open(tank_model_data, 'r') as tank_model:
        data = json.load(tank_model)
    control = data['control']

    for variable in body.variables:
        name = variable.name.value
        last_value = control[name]['value']
        setattr(variable, "last_value", last_value)
        control[name]['value'] = variable.value

    save_model(data)

    body = body.dict()
    body['time'] = str(datetime.now().date()) + ' ' + str(datetime.now().time())

    db_control_updates.insert(body)
    return body


@server.post('/simulate')
@spec.validate(body=Request(SimulationParameters), resp=Response(HTTP_200=Report))
def simulate():
    params: SimulationParameters = request.context.body
    simulator = Simulator()
    report = simulator.simulate(horizon=params.horizon, step_by_sampling=params.step_by_sampling)
    return report.dict()


if __name__ == "__main__":
    server.run()
