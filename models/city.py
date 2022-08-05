#!/usr/bin/python3
"""This module defines a City class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Defines a city Object"""

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """
        __init__ instantiates a City object

        :param args(tuple): unused
        :param kwargs(dict): is a dict of key/value pairs to init the object
        """
        super().__init__(*args, **kwargs)
