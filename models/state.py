#!/usr/bin/python3
"""This module define a State class"""
from models.base_model import BaseModel


class State(BaseModel):
    """Defines a State object"""
    name = ""

    def __init__(self, *args, **kwargs):
        """
        __init__ instantiates a State object

        :param args(tuple): unused
        :param kwargs(dict): is a dict of key/value pairs to init the object
        """
        super().__init__(*args, **kwargs)
