from dataclasses import dataclass
from datetime import datetime
import json

from src.core.car import *


class Jsoner:

    type_registry = {}
    type_registry['Point2D'] = Point2D
    type_registry['RotationFriction'] = RotationFriction
    type_registry['MotionProfile'] = MotionProfile
    type_registry['SlideFriction'] = SlideFriction
    type_registry['CarConfig'] = CarConfig
    type_registry['CarInfo'] = CarInfo
    type_registry['CarState'] = CarState
    type_registry['Action'] = Action

    @classmethod
    def to_json(cls, input: object) ->str :
        return json.dumps(input, default=lambda o: o.__dict__, indent=4)
    
    @classmethod
    def to_json_file(cls, input: object, file_path:str) ->None :
        with open(file_path, 'w') as f:
            json.dump(input, f, default=lambda o: o.__dict__, indent=4)
    
    @classmethod
    def from_json(cls, json_dict: dict):
        return cls.json_to_object(json_dict, cls.type_registry)


    @classmethod
    def json_from_file(cls, file_path:str) -> dict:
        with open('data\carconfig\cc_1.json', 'r') as f:
            return json.load(f)
    
    @classmethod
    def from_json_file(cls, file_path:str):
        with open('data\carconfig\cc_1.json', 'r') as f:
            json_dict = json.load(f)
        return cls.json_to_object(json_dict, cls.type_registry)
    
    @classmethod
    def json_to_object(cls, json_dict: dict, type_registry):
        if isinstance(json_dict, dict):
            obj_type = json_dict['type']
            del json_dict['type']
            ObjType = type_registry[obj_type]
            for key, value in json_dict.items():
                json_dict[key] = cls.json_to_object(value, type_registry)
            return ObjType(**json_dict)
        elif isinstance(json_dict, list):
            return [cls.json_to_object(elem, type_registry) for elem in json_dict]
        else:
            return json_dict
        
