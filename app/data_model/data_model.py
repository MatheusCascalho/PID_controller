from app.data_model.variable_names import ModelVariableName, ControlVariableName, ThermalModel
from pydantic import BaseModel as PydanticBaseModel
from typing import Union, List, Optional


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class ModelVariable(BaseModel):
    model: ThermalModel
    name: ModelVariableName
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
                    "enum": [e.value for e in ModelVariableName],
                    "type": "string"
                },
            }
        }


class ModelVariableContainer(BaseModel):
    variables: List[ModelVariable]


class ControlVariable(BaseModel):
    name: ControlVariableName
    value: Union[float, int]
    last_value: Optional[Union[float]]

    class Config:
        schema_extra = {
            "definitions": {
                "name": {
                    "enum": [e.value for e in ControlVariableName],
                    "type": "string"
                },
            }
        }


class ControlVariableContainer(BaseModel):
    variables: List[ControlVariable]


