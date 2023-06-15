from app.data_model.variable_names import VariableName, ThermalModel
from pydantic import BaseModel as PydanticBaseModel
from typing import Union, List, Optional


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class ModelVariable(BaseModel):
    model: ThermalModel
    name: VariableName
    value: Union[float, int]
    last_value: Optional[Union[float]]

    class Config:
        schema_extra = {
            "definitions": {
                "model": {
                    "enum": [e.value for e in ThermalModel],
                    "type": "string"
                },
                "name": {
                    "enum": [e.value for e in VariableName],
                    "type": "string"
                },
            }
        }


class ModelVariableContainer(BaseModel):
    variables: List[ModelVariable]


class ControlVariable(BaseModel):
    name: VariableName
    value: Union[int, float]

    class Config:
        schema_extra = {
            "definitions": {
                "name": {
                    "enum": [e.value for e in VariableName],
                    "type": "string"
                },
            }
        }


