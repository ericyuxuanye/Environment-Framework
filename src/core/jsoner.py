from dataclasses import dataclass
from datetime import datetime
import json
import os
import pickle

from src.core.car import *
from src.core.track import *
from src.core.race import *

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

    type_registry['MarkLine'] = MarkLine
    type_registry['TrackInfo'] = TrackInfo
    type_registry['ModelInfo'] = ModelInfo
    type_registry['RaceInfo'] = RaceInfo
    type_registry['ActionCarState'] = ActionCarState

    @classmethod
    def to_json(cls, input: object, indent=None) ->str :
        return json.dumps(input, default=lambda o: o.__dict__, indent=indent)
    
    @classmethod
    def to_json_file(cls, input: object, file_path:str, indent=None) ->None :
        with open(file_path, 'w') as f:
            json.dump(input, f, default=lambda o: o.__dict__, indent=indent)
    
    @classmethod
    def from_json_dict(cls, json_dict: dict):
        return cls.json_to_object(json_dict, cls.type_registry)
    
    @classmethod
    def from_json_str(cls, json_str: str):
        json_dict = json.loads(json_str)
        return cls.json_to_object(json_dict, cls.type_registry)

    @classmethod
    def dict_from_json_file(cls, file_path:str) -> dict:
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @classmethod
    def object_from_json_file(cls, file_path:str):
        with open(file_path, 'r') as f:
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
        

class RaceDataSaver:

    @classmethod
    def save(cls, race_data: RaceData, folder: str):
        directory = os.path.join(folder, race_data.race_info.id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        info_file = 'info.json'
        info_path = os.path.join(directory, info_file)
        with open(info_path, 'w') as infofile:
            info_json = Jsoner.to_json(race_data.race_info, indent=4)
            # print('race_json', info_json)
            infofile.write(info_json)

        step_path = os.path.join(directory, 'action_state.log')
        with open(step_path, 'w') as logfile:
            for step in race_data.steps: 
                step_json = Jsoner.to_json(step)
                # print(step_json)
                logfile.write(step_json + '\n')
    
    @classmethod
    def load(cls, directory: str) -> RaceData:
        if not os.path.exists(directory):
            return None, None
        
        info_file = 'info.json'
        info_path = os.path.join(directory, info_file)
        race_info = Jsoner.object_from_json_file(info_path)
        #  print('race_info_read : ', race_info)

        
        steps: list[ActionCarState] = []
        step_path = os.path.join(directory, 'action_state.log')
        with open(step_path, 'r') as logfile:
            Lines = logfile.readlines()
            for line in Lines:
                steps.append(Jsoner.from_json_str(line))

        # print('steps: ', steps)
        return RaceData(race_info, steps)


class TrackFieldSaver:

    @classmethod
    def save(cls, track_field: TrackField, folder: str):
        directory = os.path.join(folder, track_field.track_info.name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        info_file = 'info.json'
        info_path = os.path.join(directory, info_file)
        with open(info_path, 'w') as infofile:
            info_json = Jsoner.to_json(track_field.track_info, indent=4)
            # print('race_json', info_json)
            infofile.write(info_json)
        
        field_path = os.path.join(directory, 'field')
        with open(field_path, 'wb') as field_file:
            pickle.dump(track_field.field, field_file)
        
    
    @classmethod
    def load(cls, directory: str) -> TrackField:
        if not os.path.exists(directory):
            return None, None
        
        info_file = 'info.json'
        info_path = os.path.join(directory, info_file)
        track_info = Jsoner.object_from_json_file(info_path)
        tf = TrackField(track_info)

        field_path = os.path.join(directory, 'field')
        with open(field_path, 'rb') as field_file:
            tf.field = pickle.load(field_file)
    
        return tf
