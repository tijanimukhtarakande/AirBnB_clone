#!/usr/bin/python3
"""This module defines an Amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Defines an Amenity object"""
    name = ""

    def __init__(self, *args, **kwargs):
        """
        __init__ instantiates a Amenity object

        :param args(tuple): unused
        :param kwargs(dict): is a dict of key/value pairs to init the object
        """
        super().__init__(*args, **kwargs)
