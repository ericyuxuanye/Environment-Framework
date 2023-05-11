from dataclasses import dataclass
from datetime import datetime

from src.core.car import *


type_registry = {}
type_registry['Point2D'] = Point2D
type_registry['RotationFriction'] = RotationFriction
type_registry['MotionProfile'] = MotionProfile
type_registry['SlideFriction'] = SlideFriction
type_registry['CarConfig'] = CarConfig
type_registry['CarInfo'] = CarInfo
type_registry['CarState'] = CarState
type_registry['Action'] = Action


def json_to_object(json_obj, type_registry):
    if isinstance(json_obj, dict):
        obj_type = json_obj['type']
        del json_obj['type']
        ObjType = type_registry[obj_type]
        for key, value in json_obj.items():
            json_obj[key] = json_to_object(value, type_registry)
        return ObjType(**json_obj)
    elif isinstance(json_obj, list):
        return [json_to_object(elem, type_registry) for elem in json_obj]
    else:
        return json_obj
    
def from_json(json):
    return json_to_object(json, type_registry)