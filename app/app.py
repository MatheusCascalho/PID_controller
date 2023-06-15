from app.data_model.data_model import ModelVariableContainer, ControlVariable
from datetime import datetime
from flask import Flask, request
from flask_pydantic_spec import (
    FlaskPydanticSpec,
    Response,
    Request
)
from typing import List
from tinydb import TinyDB
import json

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Controlador PID')
spec.register(server)
database = TinyDB('model_updates.json')

tank_model_data = '../data/thermal_model.json'


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

    with open(tank_model_data, 'w') as tank_model:
        json.dump(data, tank_model, ensure_ascii=False, indent=2)

    body = body.dict()
    body['time'] = str(datetime.now().date()) + ' ' + str(datetime.now().time())

    database.insert(body)
    return body


server.run()
