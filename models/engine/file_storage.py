#!/usr/bin/python3
"""Module for serializing and deserializing instances to/from JSON"""

import json


class FileStorage:
    """Manages storage of objects in JSON format"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        with open(FileStorage.__file_path, "w") as f:
            json.dump(
                {
                    key: obj.to_dict()
                    for key, obj in FileStorage.__objects.items()
                },
                f
            )

    def reload(self):
        """Deserializes the JSON file to __objects if it exists"""
        from models.base_model import BaseModel
        from models.user import User

        classes = {
            "BaseModel": BaseModel,
            "User": User
        }

        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    class_name = val["__class__"]
                    self.all()[key] = classes[class_name](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Retrieve one object by class and ID"""
        if cls is None or id is None:
            return None
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key, None)

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls is None:
            return len(self.__objects)
        return sum(1 for obj in self.__objects.values()
                   if isinstance(obj, cls))
