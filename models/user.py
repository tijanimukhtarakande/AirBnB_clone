#!/usr/bin/python3
"""This module defines a User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Define a User object"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """
        __init__ instantiates a User object

        :param args(tuple): unused
        :param kwargs(dict): is a dict of key/value pairs to init the object
        """
        super().__init__(*args, **kwargs)
