#!/usr/bin/python3
"""This module defines a BaseModel class"""
import uuid
import datetime
import models


class BaseModel:
    """Defines a BaseModel object"""

    def __init__(self, *args, **kwargs):
        """
        __init__ instantiates a BaseModel object

        :param args(tuple): unused
        :param kwargs(dict): is a dict of key/value pairs to init the object
        """
        if kwargs:
            for key, val in kwargs.items():
                if key == "__class__":
                    continue
                if key in ["created_at", "updated_at"]:
                    val = datetime.datetime.fromisoformat(val)
                setattr(self, key, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.today()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        __str__ return the string representation of this object

        :return (str): is the string representation of the object
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        save updates the object
        """
        self.updated_at = datetime.datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        to_dict returns the dictionary form of the object

        :return (dict): is the dictionary form of the object with created_at
        and updated_at as strings
        """
        dict_form = self.__dict__.copy()
        dict_form["__class__"] = self.__class__.__name__
        dict_form["created_at"] = datetime.datetime.isoformat(
            dict_form["created_at"])
        dict_form["updated_at"] = datetime.datetime.isoformat(
            dict_form["updated_at"])
        return dict_form
