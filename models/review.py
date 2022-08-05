#!/usr/bin/python3
"""This module defins a Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Defines a Review object"""

    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        """
        __init__ instantiates a Review object

        :param args(tuple): unused
        :param kwargs(dict): is a dict of key/value pairs to init the object
        """
        super().__init__(*args, **kwargs)
