#!/usr/bin/python3
"""Defines the FileStorage class that handle persisting of objects
 to the disk"""

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import json


avaliable_classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review}


class FileStorage:
    """Creates a FileStorage object that persists objects to disk"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        all returns the private class attribute objects

        :return (dict): is a key value pair that maps object id to their
        respective objects
        """
        return FileStorage.__objects

    def new(self, obj: BaseModel):
        """
        new creates a new entry for the input obj in the private class
        attribute objects

        :param obj(BaseModel): new object to be added to the private class
        attribute objects
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        save stores the private class attribute objects to the file __file_path
        """
        with open(FileStorage.__file_path, "w", encoding="utf-8") as outfile:
            temp = FileStorage.__objects.copy()
            for key in temp:
                temp[key] = temp[key].to_dict()
            outfile.write(json.dumps(temp))

    def reload(self):
        """
        reload loads the file __file_path and deserialzes the json to __objects
        """
        try:
            with open(FileStorage.__file_path) as infile:
                json_data = json.load(infile)
                if isinstance(json_data, dict):
                    for key in json_data:
                        json_data[key] = avaliable_classes[json_data[key]
                                                           ["__class__"]](
                            **json_data[key])
                    FileStorage.__objects = json_data
        except BaseException:
            pass
