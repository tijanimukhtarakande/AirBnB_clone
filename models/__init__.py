#!/usr/bin/python3
"""This module declares the storage object"""
from models.engine import file_storage

storage = file_storage.FileStorage()
storage.reload()
